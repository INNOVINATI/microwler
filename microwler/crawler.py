import asyncio
import json
import logging
import time

import aiohttp
from urllib.parse import urlparse

import prettytable
from lxml import html as DOMParser

from microwler.scrape import title
from microwler.utils import get_headers, IGNORED_EXTENSIONS


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s : %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')


class Crawler:

    def __init__(self, start_url, max_depth, max_concurrency=200, selectors: dict = None, lang: str = 'en-us'):
        self.start_url = start_url
        parsed = urlparse(self.start_url)
        self.domain = parsed.netloc
        self.base_url = f'{parsed.scheme}://{self.domain}/'
        self.max_depth = max_depth
        self.seen_urls = set()
        self.session = aiohttp.ClientSession()
        self.limiter = asyncio.BoundedSemaphore(max_concurrency)
        self.language = lang
        self.selectors = selectors
        self.results = []
        self.verbose = True

    async def _get(self, url):
        if self.verbose:
            logging.info(f'Processing: {url}')
        async with self.limiter:
            try:
                async with self.session.get(url, timeout=10, headers=get_headers(self.language)) as response:
                    html = await response.read()
                    return html, response.status
            except Exception as e:
                logging.warning(f'Exception: {e}')

    async def _get_one(self, url):
        data, http_status = await self._get(url)
        if http_status != 200:
            logging.info(f'Page returned with Status {http_status}: {url}')
        found_urls = set()
        if data:
            for url in self._find_links(data):
                found_urls.add(url)
        return url, data, sorted(found_urls)

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
        for depth in range(self.max_depth + 1):
            batch = await self._get_batch(pipeline)
            pipeline = []
            for url, data, links in batch:
                # Extract data if selectors are defined, else keep html body
                if self.selectors:
                    data = self._parse(data)
                results.append({'url': url, 'depth': depth, 'data': data})
                pipeline.extend(links)
        await self.session.close()
        return results

    def _find_links(self, html):
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self.base_url)
        urls = [
            href for href in dom.xpath('//a/@href')
            if href not in self.seen_urls                                   # no duplicates
            and href.startswith(self.base_url)                              # stay on this website
            and not href.split('/')[-1].startswith('#')                     # ignore anchors on same page
            and not any([href.endswith(e) for e in IGNORED_EXTENSIONS])     # ignore file extensions
        ]
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
        results = future.result()
        duration = time.time() - start
        if export:
            with open(f'{self.domain}.json', 'w') as file:
                file.write(json.dumps(results))
        table = prettytable.PrettyTable()
        table.add_column('Pages', [len(results)])
        table.add_column('Duration', [f'{round(duration, 2)}s'])
        table.add_column('Average', [f'{round(len(results)/duration, 2)} p/s'])
        print(table)
        self.results = results


if __name__ == '__main__':
    crawler = Crawler(
        'https://quotes.toscrape.com/',
        max_depth=10,
        selectors={'title': title, 'p_count': lambda dom: len(dom.xpath('//p'))},
        lang='en-us'
    )
    crawler.run(verbose=False, export=True)