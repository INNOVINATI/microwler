import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Callable, Dict, Any, Union

from urllib.parse import urlparse

import prettytable
from aiohttp import AsyncResolver, TCPConnector, ClientSession
from diskcache import Index
from lxml import html as DOMParser
from parsel import Selector

from microwler.page import Page
from microwler.settings import Settings
from microwler import utils

LOG = logging.getLogger(__name__)


class Microwler:

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

    async def _http_get(self, url):
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
                return

    def _extract_links(self, html):
        """ Extract relevant links from an HTML document """
        f = self._settings.link_filter
        if type(f == str):
            dom = DOMParser.fromstring(html)
            dom.make_links_absolute(self.start_url)
            ls = dom.xpath(f)
        else:
            ls = f(html)
        return list({
            link for link in ls
            if self._domain in link or link.startswith(self.start_url)
            if link not in self._results  # filter duplicates in order to avoid extra loop steps later
            and not any([link.lower().endswith(e) for e in utils.IGNORED_EXTENSIONS])  # ignore file extensions
        })

    async def _handle_response(self, url):
        try:
            result = await self._http_get(url)
            if not result:
                self._errors[url] = 'Timeout Error'
                return

            text, status = result
            links = self._extract_links(text)
            return url, status, text, links

        except Exception as e:
            if self._verbose:
                LOG.error(f'Download error: {e} [{url}]')
            self._errors[url] = str(e)
            return

    async def _deep_crawl(self, url: str, depth: int = 0, keep_source=False):
        if depth > self._settings.max_depth:
            return

        normalized_url = utils.norm_url(url)
        if normalized_url in self._results:
            return
        if self._settings.delta_crawl:
            if normalized_url in self._cache:
                if self._verbose:
                    LOG.info(f'Dropped pre-cached URL [{normalized_url}]')
                return

        # Set a dummy for each result, so filter_links() can detect the duplicates via dict keys
        self._results[normalized_url] = None

        result = await self._handle_response(normalized_url)
        if not result:
            return

        url, status, text, links = result
        self._results[url] = Page(url, status, depth, links, text)

        if depth+1 > self._settings.max_depth:
            return
        await asyncio.gather(*(self._deep_crawl(link, depth+1, keep_source=keep_source) for link in links))

    async def _crawl(self, keep_source=False):
        LOG.info(f'Crawler started [{self._domain}]')
        resolver = AsyncResolver(nameservers=self._settings.dns_providers)
        tcpc = TCPConnector(resolver=resolver)
        self._session = ClientSession(loop=asyncio.get_event_loop(), connector=tcpc)
        try:
            await self._deep_crawl(self.start_url, depth=0, keep_source=keep_source)
        finally:
            await self._session.close()
            LOG.info(f'Crawler stopped [{self._domain}]')

        self._process(keep_source=keep_source)

    def _process(self, keep_source=False):
        # Extraction
        if self._selectors:
            LOG.info(f'Extracting data ... [{self._domain}]')
            for url, page in self._results.items():
                if page is None:
                    continue

                self._results[url] = page.scrape(self._selectors, keep_source=keep_source)

                if self._transformer is not None:
                    self._results[url] = page.transform(self._transformer)
        # Exports
        if count := len(self._settings.exporters):
            LOG.info(f'Exporting to {count} destinations... [{self._domain}]')
            for exporter_cls in self._settings.exporters:
                instance = exporter_cls(self._domain, list(self._results.values()), self._settings)
                instance.export()
        # Caching
        if self._cache is not None:
            LOG.info(f'Caching results ... [{self._domain}]')
            for page in self._results.values():
                if page is None:
                    continue
                if page.url not in self._errors:
                    self._cache[page.url] = page.__dict__

    def run(self, verbose: bool = False, keep_source: bool = False):
        """
        Starts the crawler instance. You can retrieve the results using the `crawler.results` property.
        Arguments:
            verbose: log progress to `stdout` while crawling
            keep_source: per default, the page content will be after scraping
        """

        self._verbose = verbose
        start = time.time()
        LOG.info('Starting engine ...')
        loop = asyncio.get_event_loop()
        if loop.is_running():
            task_name = f'[{datetime.now()}] {self.start_url}'
            return loop.create_task(self._crawl(keep_source=keep_source), name=task_name)
        loop.run_until_complete(self._crawl(keep_source=keep_source))
        loop.close()
        duration = time.time() - start

        if len(self._results):
            table = prettytable.PrettyTable()
            table.add_column('Pages', [len(self._results)])
            table.add_column('Duration', [f'{round(duration, 2)}s'])
            table.add_column('Performance', [f'{round(len(self._results) / duration, 2)} p/s'])
            table.add_column('Errors', [len(self._errors)])
            print(table)

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
