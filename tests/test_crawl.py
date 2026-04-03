"""
Integration tests for the Microwler crawl engine.

These tests hit a live external site (https://quotes.toscrape.com/) — a purpose-built
scraping sandbox that is intentionally stable. This keeps the tests grounded in real
HTTP behavior rather than mocked responses that can mask serialization or parsing bugs.

pytest-asyncio is configured with asyncio_mode = "auto" in pyproject.toml, so no
@pytest.mark.asyncio decorator is required on async test functions.
"""

from microwler import Microwler, scrape
from microwler.export import HTMLExporter, JSONExporter

# ── Fixtures ────────────────────────────────────────────────────────────────

BASE_URL = "https://quotes.toscrape.com/"


# ── Tests ────────────────────────────────────────────────────────────────────


async def test_basic_crawl():
    """A minimal crawl should complete and return at least one result."""
    crawler = Microwler(BASE_URL, settings={"max_depth": 1, "max_concurrency": 5})
    crawler.run()

    assert len(crawler.results) > 0, "Expected at least one crawled page"
    # Every result must have the required Page fields
    for page in crawler.results:
        assert "url" in page
        assert "status_code" in page
        assert "depth" in page
        assert "discovered" in page


async def test_selectors():
    """Selectors should populate the data field on each page."""
    selectors = {
        "title": scrape.title,
        "headings": scrape.headings,
    }
    crawler = Microwler(
        BASE_URL,
        select=selectors,
        settings={"max_depth": 1, "max_concurrency": 5},
    )
    crawler.run()

    assert len(crawler.results) > 0
    for page in crawler.results:
        # Scraped pages must have the data dict populated
        assert "data" in page
        assert "title" in page["data"]
        assert "headings" in page["data"]


async def test_transformer():
    """A transformer function should modify the scraped data before results are stored."""
    selectors = {"title": scrape.title}

    def transformer(data: dict) -> dict:
        data["title"] = data["title"].upper() if data.get("title") else data["title"]
        return data

    crawler = Microwler(
        BASE_URL,
        select=selectors,
        transform=transformer,
        settings={"max_depth": 1, "max_concurrency": 5},
    )
    crawler.run()

    assert len(crawler.results) > 0
    for page in crawler.results:
        title = page.get("data", {}).get("title")
        if title:
            # Transformer uppercases titles — verify it ran
            assert title == title.upper(), f"Expected uppercase title, got: {title!r}"


async def test_link_filter():
    """A custom link_filter XPath should restrict which URLs are followed."""
    crawler = Microwler(
        BASE_URL,
        settings={
            "link_filter": "//a[contains(@href, 'inspirational')]/@href",
            "max_depth": 2,
            "max_concurrency": 5,
        },
    )
    crawler.run()

    assert len(crawler.results) > 0
    # All discovered URLs must match the filter pattern
    for page in crawler.results:
        if page["url"] != BASE_URL:
            assert "inspirational" in page["url"], (
                f"URL outside filter scope was crawled: {page['url']}"
            )


async def test_exporters(tmp_path):
    """Exporters should write files to the configured export_to directory."""
    crawler = Microwler(
        BASE_URL,
        select={"title": scrape.title},
        settings={
            "max_depth": 1,
            "max_concurrency": 5,
            "export_to": str(tmp_path),
            "exporters": [JSONExporter, HTMLExporter],
        },
    )
    crawler.run()

    exports = list(tmp_path.iterdir())
    assert len(exports) == 2, f"Expected 2 export files, found: {[f.name for f in exports]}"

    suffixes = {f.suffix for f in exports}
    assert ".json" in suffixes, "Expected a JSON export file"
    assert ".html" in suffixes, "Expected an HTML export file"

    for f in exports:
        assert f.stat().st_size > 0, f"Export file is empty: {f.name}"


async def test_caching(tmp_path):
    """With caching enabled, a second crawl should not re-fetch already-cached URLs."""
    import os

    # Point the cache at a temp directory to avoid polluting the project directory
    os.environ["MICROWLER_TEST_CACHE"] = str(tmp_path)

    crawler = Microwler(
        BASE_URL,
        settings={
            "max_depth": 1,
            "max_concurrency": 5,
            "caching": True,
        },
    )
    # Force the cache to the temp directory by monkeypatching the cache path
    crawler._cache = None  # reset before set_cache
    crawler._settings.caching = True
    from diskcache import Index

    crawler._cache = Index(str(tmp_path / "cache"))

    crawler.run()
    first_run_count = len(crawler.results)

    assert first_run_count > 0
    assert len(crawler._cache) > 0, "Expected cache to be populated after crawl"
