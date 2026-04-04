from urllib.parse import urljoin

from diskcache import Index

from microwler import Microwler, scrape
from microwler.export import HTMLExporter, JSONExporter


def test_basic_crawl(crawl_site) -> None:
    """A minimal crawl should complete and return the first layer of internal pages."""
    crawler = Microwler(crawl_site.base_url, settings={"max_depth": 1, "max_concurrency": 5})
    crawler.run()

    urls = {page["url"] for page in crawler.results}
    assert urls == {
        crawl_site.base_url,
        urljoin(crawl_site.base_url, "inspirational"),
        urljoin(crawl_site.base_url, "plain"),
    }

    for page in crawler.results:
        assert "url" in page
        assert "status_code" in page
        assert "depth" in page
        assert "discovered" in page


def test_selectors(crawl_site) -> None:
    """Selectors should populate the data field on each page."""
    crawler = Microwler(
        crawl_site.base_url,
        select={
            "title": scrape.title,
            "headings": scrape.headings,
            "meta": scrape.meta,
        },
        settings={"max_depth": 1, "max_concurrency": 5},
    )
    crawler.run()

    assert len(crawler.results) == 3
    root_page = next(page for page in crawler.results if page["url"] == crawl_site.base_url)
    assert root_page["data"]["title"] == "Microwler Test Root"
    assert root_page["data"]["headings"]["h1"] == ["Microwler Test Root"]
    assert root_page["data"]["meta"] == {"description": "Root page for crawler tests"}


def test_transformer(crawl_site) -> None:
    """A transformer should modify scraped data before results are stored."""

    def transformer(data: dict[str, object]) -> dict[str, object]:
        title = data.get("title")
        if isinstance(title, str):
            data["title"] = title.upper()
        return data

    crawler = Microwler(
        crawl_site.base_url,
        select={"title": scrape.title},
        transform=transformer,
        settings={"max_depth": 1, "max_concurrency": 5},
    )
    crawler.run()

    for page in crawler.results:
        title = page.get("data", {}).get("title")
        if isinstance(title, str):
            assert title == title.upper()


def test_link_filter(crawl_site) -> None:
    """A custom link filter should restrict the pages that get followed."""
    crawler = Microwler(
        crawl_site.base_url,
        settings={
            "link_filter": "//a[contains(@href, 'inspirational')]/@href",
            "max_depth": 2,
            "max_concurrency": 5,
        },
    )
    crawler.run()

    urls = {page["url"] for page in crawler.results}
    assert urls == {
        crawl_site.base_url,
        urljoin(crawl_site.base_url, "inspirational"),
        urljoin(crawl_site.base_url, "inspirational/deeper"),
    }


def test_exporters(crawl_site, tmp_path) -> None:
    """Exporters should write files to the configured export directory."""
    crawler = Microwler(
        crawl_site.base_url,
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
    assert len(exports) == 2
    assert {file.suffix for file in exports} == {".json", ".html"}
    assert all(file.stat().st_size > 0 for file in exports)


def test_delta_crawl_uses_cache(crawl_site, tmp_path) -> None:
    """A delta crawl should skip URLs that are already cached."""
    cache_dir = tmp_path / "cache"

    first_crawler = Microwler(
        crawl_site.base_url,
        settings={"max_depth": 1, "max_concurrency": 5, "delta_crawl": True},
    )
    first_crawler._cache = Index(str(cache_dir))
    first_crawler.run()

    requests_after_first_run = crawl_site.request_counts.copy()
    assert len(first_crawler.cache) == 3

    second_crawler = Microwler(
        crawl_site.base_url,
        settings={"max_depth": 1, "max_concurrency": 5, "delta_crawl": True},
    )
    second_crawler._cache = Index(str(cache_dir))
    second_crawler.run()

    assert crawl_site.request_counts == requests_after_first_run
