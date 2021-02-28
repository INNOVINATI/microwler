import logging
import os
from typing import Union, Callable

LOG = logging.getLogger(__name__)


class Settings(object):
    def __init__(self,
                 link_filter: Union[Callable[[str], bool], str] = '//a/@href',
                 max_depth: int = 10,
                 max_concurrency: int = 10,
                 dns_providers: list = ['1.1.1.1', '8.8.8.8'],
                 language: str = 'en-us',
                 caching: bool = False,
                 delta_crawl: bool = False,
                 export_to=os.path.join(os.getcwd(), 'exports'),
                 exporters: list = [],
                 **kwargs
                ):
        if kwargs:
            print(f"invalid settings: {kwargs}")
            print(f"Please see docs at: https://innovinati.github.io/microwler/configuration/#settings")
            exit(1)

        self.link_filter = link_filter
        self.max_depth = max_depth
        self.max_concurrency = max_concurrency
        self.dns_providers = dns_providers
        self.language = language
        self.caching = caching
        self.delta_crawl = delta_crawl
        self.export_to = export_to
        self.exporters = exporters

        if self.delta_crawl and not self.caching:
            self.caching = True
            LOG.info('Auto-enabled caching (required for delta_crawl)')
