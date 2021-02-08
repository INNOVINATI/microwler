import asyncio
import json
import logging
import time
from typing import Callable, List, Dict, Any, Union

from urllib.parse import urlparse

import prettytable
import completely
from aiohttp import AsyncResolver, TCPConnector, ClientSession
from diskcache import Index
from lxml import html as DOMParser
from parsel import Selector

from microwler.page import Page
from microwler.settings import Settings
from microwler import utils

LOG = logging.getLogger(__name__)


class Microwler:
    """
    Each `Microwler` targets exactly one domain/website.
    """

    def __init__(self,
                 start_url: str,
                 select: Dict[str, Union[str, Callable[[Selector], Any]]] = None,
                 transform: Callable[[dict], dict] = None,
                 settings: dict = None):
        """
        Setup a new `Microwler` instance
        Arguments:
            start_url: the URL to start crawling
            select: A `dict` with *selectors* [(read more)](/microwler/scraping/#selectors)
            transform: Function to transform scraped data after crawling ([read more](/microwler/faq/#what-are-transformers))
            settings: A `dict` with configuration parameters for the crawler [(read more)](/microwler/configuration/#settings)
        """
        self.start_url = start_url
        parsed = urlparse(start_url)
        self._domain = parsed.netloc
        self._base_url = f'{parsed.scheme}://{self._domain}{parsed.path}'
        self._selectors = select
        self._transformer = transform
        self._settings = Settings(settings)
        self._seen_urls = set()
        self._session: Union[ClientSession, None] = None
        self._limiter = asyncio.BoundedSemaphore(self._settings.max_concurrency)
        self._verbose = False
        self._errors = dict()
        self._results = dict()
        self.set_cache()

    def set_cache(self, force=False):
        if self._settings.caching or force:
            self._cache = Index(f'./.microwler/cache/{self._domain}')
        else:
            self._cache = None

    async def _get(self, url):
        async with self._limiter:
            try:
                heads = utils.get_headers(self._settings.language)
                async with self._session.get(url, timeout=15, headers=heads) as response:
                    text = await response.text()
                    if self._verbose:
                        LOG.info(f'Processed: {url} [{response.status}]')
                    return text, response.status
            except TimeoutError:
                if self._verbose:
                    LOG.warning(f'Timeout error: {url}')
                return None, None

    def _find_links(self, html):
        """ Extract relevant links from an HTML document """
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self._base_url)
        links = {
            link for link in dom.xpath(self._settings.link_filter)
            if link.startswith(self._base_url)  # stay on this website
            if link not in self._results  # try to filter global duplicates in order to avoid extra loop steps later
            and not any([link.lower().endswith(e) for e in utils.IGNORED_EXTENSIONS])  # ignore file extensions
        }
        return list(links)

    async def _get_one(self, url):
        try:
            text, status = await self._get(url)
            if text is None and status is None:
                self._errors[url] = 'Timeout Error'
            else:
                links = self._find_links(text)
                return url, status, text, links
        except Exception as e:
            if self._verbose:
                LOG.error(f'Download error: {e} [{url}]')
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
                    if self._verbose:
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
                LOG.error(f'Error while crawling: {e}')
                exit(1)
        return results

    async def _crawl(self, loop):
        LOG.info(f'Crawler started [{self._domain}]')
        resolver = AsyncResolver(nameservers=self._settings.dns_providers)
        tcpc = TCPConnector(resolver=resolver)
        self._session = ClientSession(loop=loop, connector=tcpc)
        pipeline = [self.start_url]
        try:
            for depth in range(self._settings.max_depth + 1):
                batch = await self._get_batch(pipeline)
                pipeline = []
                for url, status, text, links in batch:
                    pipeline.extend(links)
                    page = Page(url, status, depth, links, text)
                    self._results[url] = page
        finally:
            await self._session.close()
            LOG.info(f'Crawler stopped [{self._domain}]')

    def _process(self, sort_urls=False, keep_source=False):
        if sort_urls:
            LOG.info(f'Sorting results ... [{self._domain}]')
            self._results = {url: self._results[url] for url in sorted(self._results)}

        if self._selectors:
            LOG.info(f'Extracting data ... [{self._domain}]')
            for url, page in self._results.items():
                self._results[url] = page.scrape(self._selectors, keep_source=keep_source)

                if self._transformer is not None:
                    self._results[url] = page.transform(self._transformer)
        count = len(self._settings.exporters)
        if count:
            LOG.info(f'Exporting to {count} destinations... [{self._domain}]')
            for exporter_cls in self._settings.exporters:
                instance = exporter_cls(self._domain, list(self._results.values()), self._settings)
                instance.export()

        if self._cache is not None:
            LOG.info(f'Caching results ... [{self._domain}]')
            for page in self._results.values():
                if page.url not in self._errors:
                    self._cache[page.url] = page.__dict__

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
        future = asyncio.Task(self._crawl(loop=loop))
        loop.run_until_complete(future)
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
                    table.add_column('Data Completeness', [f'{int(completely.measure(self.results) * 100)}%'])
            table.add_column('Total Time', [f'{round(total_time, 2)}s'])
            print(table)

    async def run_async(self, event_loop, sort_urls: bool = False, keep_source: bool = False):
        """
        For running the crawler from another `asyncio` app, which has an existing event loop, i.e. Quart.
        Arguments:
             event_loop: existing event loop, i.e. as a result of asyncio.get_event_loop()
             sort_urls: sort results alphabetically by URL
             keep_source: per default, if selectors are defined, the HTML source will be discarded
        """
        await event_loop.create_task(self._crawl(event_loop))
        if len(self._results):
            self._process(sort_urls=sort_urls, keep_source=keep_source)

    @property
    def results(self) -> [dict]:
        return [page.__dict__ for page in self._results.values()]

    @property
    def errors(self) -> dict:
        return self._errors

    @property
    def cache(self):
        if self._cache is not None:
            return list(self._cache.values())
        raise ValueError('Cache is disabled')

    def clear_cache(self):
        if self._cache is not None:
            size = len(self._cache)
            self._cache.clear()
            LOG.info(f'Removed {size} items from cache')
        raise ValueError('Cache is disabled')

    def dump_cache(self, path: str = None):
        path = path or f'./dump-{self._domain}.json'
        with open(path, 'w') as file:
            file.write(json.dumps([page.__dict__ for page in self._cache.values()]))


if __name__ == '__main__':
    c = Microwler('https://quotes.toscrape.com/')
    c.run(verbose=True)
