import os

import pytest

from microwler import Microwler, scrape
from microwler.export import JSONExporter, HTMLExporter


class TestCrawler:

    @classmethod
    @pytest.mark.asyncio
    def setup_class(cls):
        cls.selectors = {
            'title': scrape.title,
            'headings': scrape.headings,
            'paragraphs': scrape.paragraphs,
            # Define custom selectors using Parsel
            'images': lambda dom: [img.attrib['src'] for img in dom.css('img').getall()]
        }

        cls.settings = {
            'max_depth': 5,
            'max_concurrency': 15,
            'exporters': [JSONExporter, HTMLExporter],
            'caching': True,
        }

        def transformer(data: dict):
            """ Define a transformer to manipulate your scraped data """
            data['title'] = data['title'].upper()
            data['paragraphs'] = len(data['paragraphs'])
            return data

        cls.crawler = Microwler(
            'https://quotes.toscrape.com/',
            select=cls.selectors,
            transform=transformer,
            settings=cls.settings
        )

    @pytest.mark.asyncio
    def test_run(self):
        self.crawler.run()
        assert len(self.crawler.results) > 0

    def test_cache(self):
        assert len(self.crawler.cache) > 0

    def test_selectors(self):
        assert all([all([key in page['data'].keys() for key in self.selectors.keys()]) for page in self.crawler.results])

    def test_transformer(self):
        assert all([page['data']['title'].isupper() for page in self.crawler.results])

    def test_exporters(self):
        path = os.path.join(os.getcwd(), 'exports')
        assert os.path.exists(path)
        assert len(os.listdir(path)) == 2
