"""
As of v0.1.3, this file holds some more or less naive test cases,
which can also be viewed as examples for using the framework.

Some future version will have a more sophisticated test suite, i.e.
by integrating tests for the webservice.
"""
import pytest

from microwler import Microwler, scrape
from microwler.export import JSONExporter, HTMLExporter


@pytest.mark.asyncio
def test_basic():
    crawler = Microwler('https://quotes.toscrape.com/')
    crawler.run(verbose=True)


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

    crawler = Microwler('https://quotes.toscrape.com/', selectors=selectors, settings=settings)
    crawler.run(verbose=True)


@pytest.mark.asyncio
def test_advanced():
    select = {
        'title': scrape.title,
        'headings': scrape.headings,
        # Define custom selectors as lambdas or functions using Parsel
        'p_count': lambda dom: len(dom.xpath('//p').getall()),
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

    def transform(data: dict):
        """ Define a transformer to manipulate your scraped data """
        data['title'] = data['title'].upper()
        return data

    crawler = Microwler(
        'https://quotes.toscrape.com/',
        selectors=select,
        transformer=transform,
        settings=settings
    )
    crawler.run(verbose=True, sort_urls=True)

