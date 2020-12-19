import asyncio
import json
import logging
import time

import aiohttp
from urllib.parse import urlparse

import prettytable
from lxml import html as DOMParser

from microwler import scrape
from microwler.settings import Settings
from microwler.utils import get_headers, IGNORED_EXTENSIONS


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Crawler:

    def __init__(self, start_url, max_depth: int = 10, selectors: dict = None, settings: dict = None):
        self._start_url = start_url
        parsed = urlparse(start_url)
        self._domain = parsed.netloc
        self._base_url = f'{parsed.scheme}://{self._domain}/'
        self._max_depth = max_depth
        self._selectors = selectors
        self._settings = Settings(settings)
        self._seen_urls = set()
        self._session = aiohttp.ClientSession()
        self._limiter = asyncio.BoundedSemaphore(self._settings.max_concurrency)
        self._verbose = False
        self._results = []

    async def _get(self, url):
        if self._verbose:
            logging.info(f'Processing: {url}')
        async with self._limiter:
            try:
                async with self._session.get(url, timeout=20, headers=get_headers(self._settings.language)) as response:
                    html = await response.read()
                    return html
            except TimeoutError:
                logging.warning(f'Timeout error: {url}')

    async def _get_one(self, url):
        try:
            data = await self._get(url)
            found_urls = set()
            if data:
                for url in self._find_links(data):
                    found_urls.add(url)
            return url, data, sorted(found_urls)
        except Exception as e:
            logging.error(f'Processing error: {e} [{url}]')
            return url, e, None

    async def _get_batch(self, to_fetch):
        futures, results = [], []
        for url in to_fetch:
            if url in self._seen_urls:
                continue
            self._seen_urls.add(url)
            futures.append(self._get_one(url))

        for future in asyncio.as_completed(futures):
            try:
                results.append((await future))
            except Exception as e:
                logging.warning(f'Encountered exception: {e}')
        return results

    def _parse(self, html):
        dom = DOMParser.fromstring(html)
        # Selectors are either XPaths (strings) or lambdas
        data = {field: dom.xpath(selector) if (type(selector) == str) else selector(dom)
                for field, selector in self._selectors.items()}
        return data

    async def _crawl(self):
        pipeline = [self._start_url]
        results = []
        try:
            for depth in range(self._max_depth + 1):
                batch = await self._get_batch(pipeline)
                pipeline = []
                for url, data, links in batch:
                    # If links is None, there was an error
                    if links is not None:
                        # Queue the URLs found on this page
                        pipeline.extend(links)
                        # SELECTOR HOOK
                        if self._selectors:
                            data = self._parse(data)
                    # Append result object { URL, DEPTH, LINKS, DATA }
                    results.append({'url': url, 'depth': depth, 'links': links, 'data': data})
                # Set a delay between batch requests
                time.sleep(self._settings.download_delay)
        finally:
            await self._session.close()
            return results

    def _find_links(self, html):
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self._base_url)
        urls = {                                                                    # ignore local duplicates
            href for href in dom.xpath('//a/@href')
            if href not in self._seen_urls                                           # ignore global duplicates
            and href.startswith(self._base_url)                                      # stay on this website
            and not href.split('/')[-1].startswith('#')                             # ignore anchors on same page
            and not any([href.lower().endswith(e) for e in IGNORED_EXTENSIONS])     # ignore file extensions
        }
        return urls

    @property
    def data(self):
        return self._results

    def run(self, verbose=False, sort_urls=True):
        self._verbose = verbose
        self._results = None
        start = time.time()
        future = asyncio.Task(self._crawl())
        loop = asyncio.get_event_loop()
        logging.info(f'Crawler started [{self._start_url}]')
        loop.run_until_complete(future)
        loop.close()
        logging.info(f'Crawler stopped [{self._start_url}]')
        results = future.result()
        duration = time.time() - start
        if sort_urls:
            results.sort(key=lambda item: item['url'])
        self._results = results

        # INVOKE EXPORTERS
        for exporter_cls in self._settings.exporters:
            instance = exporter_cls(self._domain, self._results, self._settings)
            instance.export()

        table = prettytable.PrettyTable()
        table.add_column('Pages', [len(self._results)])
        table.add_column('Duration', [f'{round(duration, 2)}s'])
        table.add_column('Average', [f'{round(len(self._results)/duration, 2)} p/s'])
        print(table)



