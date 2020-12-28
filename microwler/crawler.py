import asyncio
import logging
import time
from typing import Callable

import aiohttp
from urllib.parse import urlparse, urlencode, parse_qsl

import prettytable
from lxml import html as DOMParser

from microwler.scrape import Page
from microwler.settings import Settings
from microwler import utils

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Crawler:
    """
    Every crawl will be executed by a single Crawler instance.
    """

    def __init__(self,
                 start_url: str,
                 selectors: dict = None,
                 transformer: Callable[[dict], dict] = None,
                 settings: dict = None):
        """
        Setup a new Crawler instance
        Arguments:
            start_url: the URL to start crawling
            selectors: A `dict` with *selectors* [(read more)](scraping/#selectors)
            transformer: Function to transform scraped data after crawling (check out [an example](examples/#advanced))
            settings: A `dict` with configuration parameters for the crawler [(read more)](#settings)
        """
        self._start_url = start_url
        parsed = urlparse(start_url)
        self._domain = parsed.netloc
        self._base_url = f'{parsed.scheme}://{self._domain}/'
        self._selectors = selectors
        self._transformer = transformer
        self._settings = Settings(settings)
        self._seen_urls = set()
        self._session = aiohttp.ClientSession()
        self._limiter = asyncio.BoundedSemaphore(self._settings.max_concurrency)
        self._verbose = False
        self._results = []

    async def _get(self, url):
        async with self._limiter:
            try:
                heads = utils.get_headers(self._settings.language)
                async with self._session.get(url, timeout=15, headers=heads) as response:
                    html = await response.text(encoding='utf-8')
                    if self._verbose:
                        logging.info(f'Processed: {url} [{response.status}]')
                    return html, response.status
            except TimeoutError:
                logging.warning(f'Timeout error: {url}')
                return None

    def _find_links(self, html):
        """ Extract relevant links from an HTML document """
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self._base_url)
        links = {
            # use set to ignore local duplicates
            link for link in dom.xpath('//a/@href')
            if link.startswith(self._base_url)  # stay on this website
            if link not in self._seen_urls  # try to filter global duplicates in order to avoid extra loop steps later
            and not any([link.lower().endswith(e) for e in utils.IGNORED_EXTENSIONS])  # ignore file extensions
        }
        return list(links)

    async def _get_one(self, url):
        try:
            html, status = await self._get(url)
            links = []
            if html:
                # find internal links
                links.extend(self._find_links(html))
            return url, status, html, links
        except Exception as e:
            logging.error(f'Processing error: {e} [{url}]')
            return url, e, None

    async def _get_batch(self, to_fetch):
        futures, results = [], []
        for url in to_fetch:
            normalized_url = utils.norm_url(url)
            if normalized_url in self._seen_urls:
                continue
            self._seen_urls.add(normalized_url)
            futures.append(self._get_one(normalized_url))

        for future in asyncio.as_completed(futures):
            try:
                results.append((await future))
            except Exception as e:
                logging.warning(f'Encountered exception: {e}')
        return results

    async def _crawl(self) -> [Page]:
        pipeline = [self._start_url]
        pages = []
        try:
            for depth in range(self._settings.max_depth + 1):
                batch = await self._get_batch(pipeline)
                pipeline = []
                for url, status, html, links in batch:
                    # If links is None, there was an error
                    if links is not None:
                        # Queue the URLs found on this page
                        pipeline.extend(links)
                    # Append result object
                    obj = Page(url, status, depth, list(links), html)
                    pages.append(obj)
        finally:
            await self._session.close()
            return pages

    def run(self, verbose: bool = False, sort_urls: bool = False, keep_source: bool = False):
        """
        Starts the crawler instance. You can retrieve the results using the `crawler.data` or `crawler.pages` properties.
        Arguments:
            verbose: log progress to `stdout` while crawling
            sort_urls: sort result list by URL
            keep_source: per default, the page content will be after scraping
        """
        self._verbose = verbose
        self._results = None
        start = time.time()
        future = asyncio.Task(self._crawl())
        loop = asyncio.get_event_loop()
        logging.info(f'Crawler started [{self._start_url}]')
        loop.run_until_complete(future)
        loop.close()
        logging.info(f'Crawler stopped [{self._start_url}]')
        pages = future.result()
        duration = time.time() - start

        if len(pages):
            # SORT #
            if sort_urls:
                logging.info(f'Sorting results ...')
                pages.sort(key=lambda item: item.url)

            # SELECT #
            if self._selectors:
                logging.info(f'Scraping data ...')
                pages = [page.scrape(self._selectors, keep_source=keep_source) for page in pages]

                # TRANSFORM #
                if self._transformer is not None:
                    logging.info(f'Applying transformer ...')
                    pages = [page.transform(self._transformer) for page in pages]

            # EXPORT #
            if len(self._settings.exporters):
                logging.info('Running exporters ...')
                for exporter_cls in self._settings.exporters:
                    instance = exporter_cls(self._domain, pages, self._settings)
                    instance.export()

        self._results = pages

        table = prettytable.PrettyTable()
        table.add_column('Pages', [len(self._results)])
        table.add_column('Duration', [f'{round(duration, 2)}s'])
        table.add_column('Average', [f'{round(len(self._results) / duration, 2)} p/s'])
        print(table)

    @property
    def data(self) -> [dict]:
        return [{'url': page.url, 'data': page.data if self._selectors else page.html} for page in self._results]

    @property
    def pages(self) -> [Page]:
        return self._results
