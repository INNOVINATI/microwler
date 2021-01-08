import logging
import os
from urllib.parse import urlparse

LOG = logging.getLogger(__name__)


class Settings(object):
    base_path: str = '/'
    max_depth: int = 10
    max_concurrency: int = 20
    language: str = 'en-us'
    caching: bool = False
    delta_crawl: bool = False
    export_to = os.path.join(os.getcwd(), 'exports')
    exporters: list = []

    def __init__(self, start_url, params: dict):
        if params:
            for key, value in params.items():
                setattr(self, key, value)

            if urlparse(start_url) != self.base_path:
                LOG.warning('Starting crawler on non-root path without "base_path" setting')

            if self.delta_crawl and not self.caching:
                self.caching = True
                LOG.info('Auto-enabled caching (required for delta_crawl)')
