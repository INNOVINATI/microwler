import asyncio
import json
import logging
import time
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

import completely
import prettytable
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from diskcache import Index
from lxml import html as DOMParser
from parsel import Selector

from microwler import utils
from microwler.page import Page
from microwler.settings import Settings

LOG = logging.getLogger(__name__)

type SelectorFunc = Callable[[Selector], Any]
type SelectorMap = dict[str, str | SelectorFunc]
type TransformFunc = Callable[[dict[str, Any]], dict[str, Any]]
type CrawlResult = tuple[str, int, str, list[str]]


class Microwler:
    """
    Each `Microwler` targets exactly one domain/website.
    """

    def __init__(
        self,
        start_url: str,
        select: SelectorMap | None = None,
        transform: TransformFunc | None = None,
        settings: dict[str, Any] | None = None,
    ):
        """
        Setup a new `Microwler` instance.

        Arguments:
            start_url: the URL to start crawling
            select: a dict of named selectors — XPath strings or callables that receive
                    a Parsel Selector and return any Python value
            transform: optional function applied to each page's scraped data dict after crawling
            settings: configuration dict; see Settings for available keys
        """
        self.start_url = start_url
        parsed = urlparse(start_url)
        self._domain = parsed.netloc
        self._base_url = f"{parsed.scheme}://{self._domain}{parsed.path}"
        self._selectors = select
        self._transformer = transform
        self._settings = Settings(settings)
        self._seen_urls: set[str] = set()
        self._session: ClientSession | None = None
        self._limiter = asyncio.BoundedSemaphore(self._settings.max_concurrency)
        self._verbose = False
        self._errors: dict[str, str] = {}
        self._results: dict[str, Page] = {}
        self.set_cache()

    def set_cache(self, force: bool = False) -> None:
        if self._settings.caching or force:
            self._cache: Index | None = Index(f"./.microwler/cache/{self._domain}")
        else:
            self._cache = None

    def _reset_runtime_state(self) -> None:
        self._seen_urls.clear()
        self._errors.clear()
        self._results.clear()

    async def _get(self, url: str) -> tuple[str, int] | None:
        session = self._session
        if session is None:
            raise RuntimeError("Crawler session is not initialized")

        async with self._limiter:
            try:
                heads = utils.get_headers(self._settings.language)
                async with session.get(url, timeout=15, headers=heads) as response:
                    text = await response.text()
                    if self._verbose:
                        LOG.info(f"Processed: {url} [{response.status}]")
                    return text, response.status
            except TimeoutError:
                if self._verbose:
                    LOG.warning(f"Timeout error: {url}")
                return None

    def _find_links(self, html: str) -> list[str]:
        """Extract same-domain links from an HTML document, filtering binary file extensions."""
        dom = DOMParser.fromstring(html)
        dom.make_links_absolute(self._base_url)
        links = {
            link
            for link in dom.xpath(self._settings.link_filter)
            if link.startswith(self._base_url)  # stay on this domain
            if link not in self._seen_urls  # skip already-queued URLs to avoid redundant batches
            and not any(
                link.lower().endswith(e) for e in utils.IGNORED_EXTENSIONS
            )  # skip non-HTML resources
        }
        return list(links)

    async def _get_one(self, url: str) -> CrawlResult | None:
        try:
            response = await self._get(url)
            if response is None:
                self._errors[url] = "Timeout Error"
                return None

            text, status = response
            links = self._find_links(text)
            return url, status, text, links
        except Exception as e:
            if self._verbose:
                LOG.error(f"Download error: {e} [{url}]")
            self._errors[url] = str(e)
            return None

    async def _get_batch(self, to_fetch: list[str]) -> list[CrawlResult]:
        futures: list[asyncio.Future[CrawlResult | None] | asyncio.Task[CrawlResult | None]] = []
        results: list[CrawlResult] = []
        cache = self._cache

        for url in to_fetch:
            normalized_url = utils.norm_url(url)
            if normalized_url in self._seen_urls:
                continue
            if self._settings.delta_crawl and cache is not None and normalized_url in cache:
                if self._verbose:
                    LOG.info(f"Dropped pre-cached URL [{normalized_url}]")
                continue

            self._seen_urls.add(normalized_url)
            futures.append(asyncio.create_task(self._get_one(normalized_url)))

        for future in asyncio.as_completed(futures):
            try:
                result = await future
                if result is not None:
                    results.append(result)
            except Exception as e:
                LOG.error(f"Error while crawling: {e}")
                exit(1)
        return results

    async def _crawl(self) -> None:
        """Run the full crawl loop.

        Uses a plain ClientSession without the deprecated loop= parameter, which was
        removed in aiohttp 3.9. The event loop is managed by the caller (asyncio.run
        for synchronous entry, or an existing loop when awaited from async code).
        """
        self._reset_runtime_state()
        LOG.info(f"Crawler started [{self._domain}]")
        resolver = AsyncResolver(nameservers=self._settings.dns_providers)
        tcpc = TCPConnector(resolver=resolver)
        # No loop= argument — aiohttp infers the running loop automatically
        session = ClientSession(connector=tcpc)
        self._session = session
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
            await session.close()
            self._session = None
            LOG.info(f"Crawler stopped [{self._domain}]")

    def _process(self, sort_urls: bool = False, keep_source: bool = False) -> None:
        if sort_urls:
            LOG.info(f"Sorting results ... [{self._domain}]")
            self._results = {url: self._results[url] for url in sorted(self._results)}

        if self._selectors:
            LOG.info(f"Extracting data ... [{self._domain}]")
            for url, page in self._results.items():
                processed_page = page.scrape(self._selectors, keep_source=keep_source)
                if self._transformer is not None:
                    processed_page = processed_page.transform(self._transformer)
                self._results[url] = processed_page
        count = len(self._settings.exporters)
        if count:
            LOG.info(f"Exporting to {count} destinations... [{self._domain}]")
            for exporter_cls in self._settings.exporters:
                instance = exporter_cls(self._domain, list(self._results.values()), self._settings)
                instance.export()

        if self._cache is not None:
            LOG.info(f"Caching results ... [{self._domain}]")
            for page in self._results.values():
                if page.url not in self._errors:
                    self._cache[page.url] = page.__dict__

    def run(
        self, verbose: bool = False, sort_urls: bool = False, keep_source: bool = False
    ) -> None:
        """
        Start the crawler synchronously. Results are available via `.results` and `.errors`.

        Arguments:
            verbose: stream progress to stdout via the logger
            sort_urls: sort results alphabetically by URL before processing
            keep_source: retain raw HTML on each Page after scraping (discarded by default)
        """
        self._verbose = verbose
        start = time.time()
        LOG.info("Starting engine ...")

        # asyncio.run() creates a fresh event loop, runs the coroutine to completion,
        # and closes the loop — the correct pattern since Python 3.7 and mandatory in
        # 3.10+ where get_event_loop() emits DeprecationWarning outside a running loop.
        asyncio.run(self._crawl())
        crawl_time = time.time() - start

        if len(self._results):
            self._process(sort_urls=sort_urls, keep_source=keep_source)
            total_time = time.time() - start
            table = prettytable.PrettyTable()
            table.add_column("Pages", [len(self._results)])
            table.add_column("Crawl Time", [f"{round(crawl_time, 2)}s"])
            table.add_column("Crawl Speed", [f"{round(len(self._results) / crawl_time, 2)} p/s"])
            table.add_column("Errors", [len(self._errors)])
            if len(self._results):
                table.add_column("Processing Time", [f"{round(total_time - crawl_time, 2)}s"])
                if self._selectors:
                    table.add_column(
                        "Data Completeness", [f"{int(completely.measure(self.results) * 100)}%"]
                    )
            table.add_column("Total Time", [f"{round(total_time, 2)}s"])
            print(table)

    async def run_async(self, sort_urls: bool = False, keep_source: bool = False) -> None:
        """
        Run the crawler from within an existing async application (e.g. a Quart route handler).

        The caller's event loop owns the scheduling context — simply awaiting this coroutine
        is the correct pattern. The event_loop parameter has been removed because passing a
        loop object into aiohttp was deprecated in 3.8 and removed in 3.9.

        Arguments:
            sort_urls: sort results alphabetically by URL before processing
            keep_source: retain raw HTML on each Page after scraping (discarded by default)
        """
        self._verbose = False
        await self._crawl()
        if len(self._results):
            self._process(sort_urls=sort_urls, keep_source=keep_source)

    @property
    def results(self) -> list[dict[str, Any]]:
        return [page.__dict__ for page in self._results.values()]

    @property
    def errors(self) -> dict[str, str]:
        return self._errors

    @property
    def cache(self) -> list[dict[str, Any]]:
        if self._cache is not None:
            return list(self._cache.values())
        raise ValueError("Cache is disabled")

    def clear_cache(self) -> None:
        if self._cache is not None:
            size = len(self._cache)
            self._cache.clear()
            LOG.info(f"Removed {size} items from cache")
            return
        raise ValueError("Cache is disabled")

    def dump_cache(self, path: str | None = None) -> None:
        if self._cache is None:
            raise ValueError("Cache is disabled")

        path = path or f"./dump-{self._domain}.json"
        with open(path, "w") as file:
            file.write(json.dumps(list(self._cache.values())))


if __name__ == "__main__":
    c = Microwler("https://quotes.toscrape.com/")
    c.run(verbose=True)
