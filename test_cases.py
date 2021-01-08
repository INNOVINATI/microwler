"""
As of v0.1.3, this file holds some more or less naive test cases,
which can also be used as examples for using the framework.

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
    for page in crawler.pages:
        print(page.url, page.html)


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
    for page_data in crawler.data:
        print(f'\n{page_data["url"].upper()}')
        for key, value in page_data.items():
            print(f'> {key.upper()}: {value}')


@pytest.mark.asyncio
def test_advanced():
    select = {
        'title': scrape.title,
        'headings': scrape.headings,
        # Define custom selectors as lambdas or functions (Microwler will inject the page as lxml.html.HtmlElement)
        'p_count': lambda dom: len(dom.xpath('//p'))
    }

    settings = {
        'max_depth': 10,
        'max_concurrency': 15,
        'export_to': './export/project_folder',
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

