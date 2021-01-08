import asyncio
import json
import logging
import time
from typing import Callable

import aiohttp
from urllib.parse import urlparse

import prettytable
import completely
from diskcache import Index
from lxml import html as DOMParser

from microwler.scrape import Page
from microwler.settings import Settings
from microwler import utils

LOG = logging.getLogger(__name__)


class Microwler:
    """
    Each `Microwler` targets exactly one domain/website.
    """

    def __init__(self,
                 start_url: str,
                 selectors: dict = None,
                 transformer: Callable[[dict], dict] = None,
                 settings: dict = None):
        """
        Setup a new `Microwler` instance
        Arguments:
            start_url: the URL to start crawling
            selectors: A `dict` with *selectors* [(read more)](/microwler/scraping/#selectors)
            transformer: Function to transform scraped data after crawling ([read more](/microwler/faq/#what-are-transformers))
            settings: A `dict` with configuration parameters for the crawler [(read more)](/microwler/configuration/#settings)
        """
        self._start_url = start_url
        parsed = urlparse(start_url)
        self._domain = parsed.netloc
        self._base_url = f'{parsed.scheme}://{self._domain}{parsed.path}'
        self._selectors = selectors
        self._transformer = transformer
        self._settings = Settings(self._base_url, settings)
        self._seen_urls = set()
        self._session = None
        self._limiter = asyncio.BoundedSemaphore(self._settings.max_concurrency)
        self._verbose = False
        self._cache = Index(f'./.microwler/cache/{self._domain}') if self._settings.caching else None
        self._errors = dict()
        self._results = dict()

    async def _get(self, url):
        async with self._limiter:
            try:
                heads = utils.get_headers(self._settings.language)
                async with self._session.get(url, timeout=15, headers=heads) as response:
                    html = await response.text(encoding='utf-8')
                    if self._verbose:
                        LOG.info(f'Processed: {url} [{response.status}]')
                    return html, response.status
            except TimeoutError:
                LOG.warning(f'Timeout error: {url}')
                return None, None

    def _find_links(self, html):
        """ Extract relevant links from an HTML document """
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self._base_url)
        links = {
            # use set to ignore local duplicates
            link for link in dom.xpath('//a/@href')
            if link.startswith(self._base_url)  # stay on this website
            if urlparse(link).path.startswith(self._settings.base_path)
            if link not in self._results  # try to filter global duplicates in order to avoid extra loop steps later
            and not any([link.lower().endswith(e) for e in utils.IGNORED_EXTENSIONS])  # ignore file extensions
        }
        return list(links)

    async def _get_one(self, url):
        try:
            html, status = await self._get(url)
            if html and status:
                links = self._find_links(html)
                return url, status, html, links
            else:
                self._errors[url] = 'Timeout Error'
        except Exception as e:
            LOG.error(f'Processing error: {e} [{url}]')
            self._errors[url] = str(e)
        return None

    async def _get_batch(self, to_fetch):
        futures, results = [], []
        for url in to_fetch:
            normalized_url = utils.norm_url(url)
            if normalized_url in self._results:
                continue
            if self._settings.delta_crawl:
                if normalized_url in self._cache:
                    LOG.info(f'Dropped pre-cached URL [{normalized_url}]')
                    continue
            self._results[normalized_url] = None
            futures.append(self._get_one(normalized_url))

        for future in asyncio.as_completed(futures):
            try:
                result = (await future)
                if result is not None:
                    results.append(result)
            except Exception as e:
                LOG.warning(f'Exception: {e}')
        return results

    async def _crawl(self) -> [Page]:
        LOG.info(f'Crawler started [{self._domain}]')
        pipeline = [self._start_url]
        try:
            for depth in range(self._settings.max_depth + 1):
                batch = await self._get_batch(pipeline)
                pipeline = []
                for url, status, html, links in batch:
                    pipeline.extend(links)
                    page = Page(url, status, depth, links, html)
                    self._results[url] = page
        finally:
            await self._session.close()
            LOG.info(f'Crawler stopped [{self._domain}]')

    def _process(self, sort_urls=False, keep_source=False):

        if sort_urls:
            LOG.info(f'Sorting results ...')
            self._results = {url: self._results[url] for url in sorted(self._results)}

        if self._selectors:
            LOG.info('Processing data ...')
            for url, page in self._results.items():
                self._results[url] = page.scrape(self._selectors, keep_source=keep_source)

                if self._transformer is not None:
                    self._results[url] = page.transform(self._transformer)

        if len(self._settings.exporters):
            for exporter_cls in self._settings.exporters:
                instance = exporter_cls(self._domain, list(self._results.values()), self._settings)
                instance.export()

        if self._settings.caching:
            LOG.info('Caching results ...')
            for page in self.pages:
                self._cache[page.url] = page

    def run(self, verbose: bool = False, sort_urls: bool = False, keep_source: bool = False):
        """
        Starts the crawler instance. You can retrieve the results using the `crawler.data` or `crawler.pages` properties.
        Arguments:
            verbose: log progress to `stdout` while crawling
            sort_urls: sort result list by URL
            keep_source: per default, the page content will be after scraping
        """
        self._verbose = verbose
        start = time.time()
        LOG.info('Starting engine ...')
        loop = asyncio.get_event_loop()
        try:
            self._session = aiohttp.ClientSession(loop=loop)
            future = asyncio.Task(self._crawl())
            loop.run_until_complete(future)
        finally:
            loop.close()
        crawl_time = time.time() - start

        if len(self._results):
            self._process(sort_urls=sort_urls, keep_source=keep_source)
            total_time = time.time() - start
            table = prettytable.PrettyTable()
            table.add_column('Pages', [len(self._results)])
            table.add_column('Crawl Time', [f'{round(crawl_time, 2)}s'])
            table.add_column('Crawl Speed', [f'{round(len(self._results) / crawl_time, 2)} p/s'])
            table.add_column('Errors', [len(self._errors)])
            if len(self._results):
                table.add_column('Processing Time', [f'{round(total_time - crawl_time, 2)}s'])
                if self._selectors:
                    table.add_column('Data Completeness', [f'{int(completely.measure(self.data)*100)}%'])
            table.add_column('Total Time', [f'{round(total_time, 2)}s'])
            print(table)

    @property
    def data(self) -> [dict]:
        return [{'url': page.url, 'data': page.data if self._selectors else page.html} for page in self._results.values()]

    @property
    def pages(self) -> [Page]:
        return list(self._results.values())

    @property
    def errors(self) -> dict:
        return self._errors

    @property
    def cache(self):
        if self._settings.caching:
            return list(self._cache.values())
        raise ValueError('Cache is disabled')

    def clear_cache(self):
        if self._settings.caching:
            size = len(self._cache)
            self._cache.clear()
            LOG.info(f'Removed {size} items from cache')
        raise ValueError('Cache is disabled')

    def dump_cache(self, path: str = None):
        path = path or f'./dump-{self._domain}.json'
        with open(path, 'w') as file:
            file.write(json.dumps([page.__dict__ for page in self._cache.values()]))

if __name__ == '__main__':
    c = Microwler(
        'https://cispa.de/'
    )
    c.run(verbose=True)