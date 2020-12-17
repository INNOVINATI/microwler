import asyncio
import json
import logging
import os
import time

import aiohttp
from urllib.parse import urlparse

import prettytable
from lxml import html as DOMParser

from microwler import scrape
from microwler.utils import get_headers, IGNORED_EXTENSIONS


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Crawler:

    def __init__(self,
                 start_url,
                 max_depth: int = 10,
                 max_concurrency: int = 100,
                 selectors: dict = None,
                 lang: str = 'en-us',
                 download_delay: int = 3):
        self.start_url = start_url
        parsed = urlparse(self.start_url)
        self.domain = parsed.netloc
        self.base_url = f'{parsed.scheme}://{self.domain}/'
        self.max_depth = max_depth
        self.download_delay = download_delay
        self.seen_urls = set()
        self.session = aiohttp.ClientSession()
        self.limiter = asyncio.BoundedSemaphore(max_concurrency)
        self.language = lang
        self.selectors = selectors
        self.results = []
        self.verbose = False

    async def _get(self, url):
        if self.verbose:
            logging.info(f'Processing: {url}')
        async with self.limiter:
            try:
                async with self.session.get(url, timeout=20, headers=get_headers(self.language)) as response:
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
            if url in self.seen_urls:
                continue
            self.seen_urls.add(url)
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
                for field, selector in self.selectors.items()}
        return data

    async def _crawl(self):
        pipeline = [self.start_url]
        results = []
        try:
            for depth in range(self.max_depth + 1):
                batch = await self._get_batch(pipeline)
                time.sleep(self.download_delay)
                pipeline = []
                for url, data, links in batch:
                    # If links is None, there was an error
                    if links is not None:
                        # Queue the URLs found on this page
                        pipeline.extend(links)
                        # Extract data if selectors are defined, else keep html body
                        if self.selectors:
                            data = self._parse(data)
                    results.append({'url': url, 'depth': depth, 'links': links, 'data': data})
        finally:
            await self.session.close()
            return results

    def _find_links(self, html):
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self.base_url)
        urls = {                                                                    # ignore local duplicates
            href for href in dom.xpath('//a/@href')
            if href not in self.seen_urls                                           # ignore global duplicates
            and href.startswith(self.base_url)                                      # stay on this website
            and not href.split('/')[-1].startswith('#')                             # ignore anchors on same page
            and not any([href.lower().endswith(e) for e in IGNORED_EXTENSIONS])     # ignore file extensions
        }
        return urls

    def run(self, verbose=False, export=False):
        self.verbose = verbose
        self.results = None
        start = time.time()
        future = asyncio.Task(self._crawl())
        loop = asyncio.get_event_loop()
        logging.info(f'Crawler started [{self.start_url}]')
        loop.run_until_complete(future)
        loop.close()
        logging.info(f'Crawler stopped [{self.start_url}]')
        results = future.result()
        duration = time.time() - start
        if export:
            try:
                path = os.path.join(os.getcwd(), f'{self.domain}.json')
                with open(path, 'w') as file:
                    file.write(json.dumps(results))
                logging.info(f'Exported results to {path}')
            except Exception as e:
                logging.error(f'Failed to export: {e}')
        table = prettytable.PrettyTable()
        table.add_column('Pages', [len(results)])
        table.add_column('Duration', [f'{round(duration, 2)}s'])
        table.add_column('Average', [f'{round(len(results)/duration, 2)} p/s'])
        self.results = results
        print(table)


if __name__ == '__main__':
    crawler = Crawler(
        'https://quotes.toscrape.com/',
        max_depth=10,
        selectors={'title': scrape.title, 'p_count': lambda dom: len(dom.xpath('//p'))},
        lang='en-us'
    )
    crawler.run(verbose=True, export=True)