import asyncio
from asyncio.tasks import create_task
import json
import logging
import time
from datetime import datetime
from typing import Callable, Dict, Any, Union

from urllib.parse import urlparse, urljoin

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

        parsed = urlparse(start_url)
        if not parsed.scheme:
            raise ValueError('Invalid start_url: missing scheme')

        self.start_url = utils.norm_url(start_url, no_query=True)
        self._domain = parsed.netloc
        self._selectors = select
        self._transformer = transform
        self._settings = Settings(settings)
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

    def _seen_url(self, url):
        return url in self._results or url in self._errors

    async def _request(self, url):
        async with self._limiter:
            try:
                heads = utils.get_headers(self._settings.language)
                async with self._session.get(url, timeout=15, headers=heads) as response:
                    if self._verbose:
                        LOG.info(f'Processed: {url} [{response.status}]')
                    text = await response.text()
                    return response.status, text
            except Exception as e:
                self._errors[url] = str(e)
                if self._verbose:
                    LOG.warning(f'Timeout error: {url}')
                return

    def _extract_links(self, url, html):
        """ Extract relevant links from an HTML document """

        lfilter = self._settings.link_filter

        # Parse html
        dom = DOMParser.fromstring(html)

        # Default xpath link filter
        link_xpath = '//a/@href'

        if isinstance(lfilter, str):
            # Use user-defined xpath link filter
            link_xpath = lfilter

        # Extract links
        ls = dom.xpath(link_xpath)

        # Ignore certain file extensions
        ls = (l for l in ls if l.lower().partition('.')[-1] not in utils.IGNORED_EXTENSIONS)

        # Remove duplicates
        ls = sorted(set(ls))

        # Make links absolute
        ls = (urljoin(url, l) for l in ls)

        if callable(lfilter):
            # Invoke user-defined link filter
            ls = lfilter(ls)

        # Normalize urls
        ls = (utils.norm_url(l) for l in ls)

        return ls

    async def _deep_crawl(self, url: str, depth: int = 0, keep_source=False):
        if depth > self._settings.max_depth:
            return

        # Filter previously seen URLs
        if self._seen_url(url):
            return

        if self._settings.delta_crawl:
            if url in self._cache and url != self.start_url:
                if self._verbose:
                    LOG.info(f'Dropped pre-cached URL [{url}]')
                return

        # Set a dummy for each result, so duplicate links can be detected via dict keys
        self._results[url] = None

        result = await self._request(url)
        if not result:
            # self._errors has an entry for normalized_url
            del self._results[url]
            return

        status, text = result

        links = []
        tasks = []
        for link in self._extract_links(url, text):
            links.append(link)
            # respect depth limit
            if depth+1 > self._settings.max_depth:
                continue
            # deep crawling
            if urlparse(link).netloc != self._domain:
                continue
            # drop known urls
            if self._seen_url(link):
                continue
            tasks.append(asyncio.create_task(self._deep_crawl(link, depth+1, keep_source=keep_source)))

        page = Page(url, status, depth, links, text)

        # Scraping & Transformation
        if self._selectors:
            page = page.scrape(self._selectors, keep_source=keep_source)

            if self._transformer is not None:
                page = page.transform(self._transformer)

            self._results[url] = page

        if tasks:
            await asyncio.wait(tasks)

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

        # Exports
        if count := len(self._settings.exporters):
            LOG.info(f'Exporting to {count} destinations... [{self._domain}]')
            for exporter_cls in self._settings.exporters:
                instance = exporter_cls(self._domain, sorted(self._results.values()), self._settings)
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
        LOG.info('Starting engine ...')
        loop = asyncio.get_event_loop()
        start = time.time()
        if loop.is_running():
            task_name = f'[{datetime.now()}] {self.start_url}'
            return loop.create_task(self._crawl(keep_source=keep_source), name=task_name)
        loop.run_until_complete(self._crawl(keep_source=keep_source))
        duration = time.time() - start
        loop.close()

        if len(self._results):
            if self._verbose:
                table = prettytable.PrettyTable()
                table.add_column('Pages', [len(self._results)])
                table.add_column('Duration', [f'{round(duration, 2)}s'])
                table.add_column('Performance', [f'{round(len(self._results) / duration, 2)} p/s'])
                table.add_column('Errors', [len(self._errors)])
                print(table)
            else:
                LOG.info(f'Processed {len(self._results)} pages in {round(duration, 2)} seconds [{self._domain}]')
        if len(self._errors):
            table = prettytable.PrettyTable()
            table.add_column('URL', list(self._errors.keys()))
            table.add_column('Error', list(self._errors.values()))

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