"""
This file will be discarded in v0.2.0 in favor of a fully implemented test suite located in tests/
"""
import pytest

from microwler import Microwler, scrape
from microwler.export import JSONExporter, HTMLExporter


@pytest.mark.asyncio
def test_basic():
    crawler = Microwler('https://quotes.toscrape.com/')
    crawler.run()


@pytest.mark.asyncio
def test_intermediate():
    selectors = {
        'title': scrape.title,
        'headings': scrape.headings,
    }

    settings = {
        'max_depth': 5,
        'max_concurrency': 30,
    }

    crawler = Microwler('https://quotes.toscrape.com/', select=selectors, settings=settings)
    crawler.run()


@pytest.mark.asyncio
def test_advanced():
    selectors = {
        'title': scrape.title,
        'headings': scrape.headings,
        'paragraphs': scrape.paragraphs,
        # Define custom selectors using Parsel
        'images': lambda dom: [img.attrib['src'] for img in dom.css('img').getall()]
    }

    settings = {
        'link_filter': "//a[contains(@href, 'inspirational')]/@href",
        'max_depth': 10,
        'max_concurrency': 15,
        'export_to': './tests/exports',
        'exporters': [JSONExporter, HTMLExporter],
        'caching': True,
    }

    def transformer(data: dict):
        """ Define a transformer to manipulate your scraped data """
        data['title'] = data['title'].upper()
        data['paragraphs'] = len(data['paragraphs'])
        return data

    crawler = Microwler(
        'https://quotes.toscrape.com/',
        select=selectors,
        transform=transformer,
        settings=settings
    )
    crawler.run()

    # Test components
    for page in crawler.results:
        if page['url'] != crawler.start_url:
            # Test link_filter
            assert('inspirational' in page['url'])

        # Test selectors
        assert(all([key in page['data'] and page['data'][key] is not None for key in selectors.keys()]))
        # Test transformer
        assert(type(page['data']['title']) == str and page['data']['title'].isupper())
        # Test cache
        assert(len(crawler._cache) > 0)


