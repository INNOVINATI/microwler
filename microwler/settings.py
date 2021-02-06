import logging
import os

LOG = logging.getLogger(__name__)


class Settings(object):
    link_filter: str = '//a/@href'
    max_depth: int = 10
    max_concurrency: int = 20
    dns_providers: list = ['1.1.1.1', '8.8.8.8']
    language: str = 'en-us'
    caching: bool = False
    delta_crawl: bool = False
    export_to = os.path.join(os.getcwd(), 'exports')
    exporters: list = []

    def __init__(self, params: dict):
        if params:
            for key, value in params.items():
                setattr(self, key, value)

            if self.delta_crawl and not self.caching:
                self.caching = True
                LOG.info('Auto-enabled caching (required for delta_crawl)')
