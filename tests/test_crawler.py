# TODO
import os

from diskcache import Cache

from microwler import Microwler
from microwler.export import JSONExporter, HTMLExporter, CSVExporter


class TestHTTP:
    pass


class TestLinkFilter:
    pass


class TestScraping:
    pass


class TestSettings:
    pass


class TestCache:
    crawler = Microwler('http://example.com/')
    path = os.path.join(os.getcwd(), '.microwler', 'cache')

    def test_set_cache(self):
        if os.path.isdir(self.path):
            os.remove(self.path)
        assert self.crawler._cache is None
        self.crawler.set_cache()
        assert self.crawler._cache is None
        self.crawler.set_cache(force=True)
        assert isinstance(self.crawler._cache, Cache)
        assert os.path.isdir(os.path.join(self.path, 'example.com'))

    def test_to_cache(self):
        self.crawler.run()
        assert len(self.crawler.cache) == 1

    def test_from_cache(self):
        self.crawler = Microwler('http://example.com/')
        assert len(self.crawler.cache) == 1
        os.remove(self.path)


class TestExport:
    crawler = Microwler('http://example.com/', settings={'exporters:' [JSONExporter, HTMLExporter, CSVExporter]})
    path = os.path.join(os.getcwd(), 'export')





