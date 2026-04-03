import logging
import os

LOG = logging.getLogger(__name__)


class Settings:
    """Holds configuration for a single Microwler crawler instance.

    All mutable attributes are instantiated per object rather than at the class level
    to prevent shared state between crawler instances running in the same process.
    Class-level mutable defaults in Python are shared across all instances — a subtle
    footgun that causes one crawler's configuration to bleed into another's.
    """

    def __init__(self, params: dict | None = None) -> None:
        # Defaults are set here, not at class level, to guarantee per-instance isolation
        self.link_filter: str = "//a/@href"
        self.max_depth: int = 10
        self.max_concurrency: int = 20
        self.dns_providers: list[str] = ["1.1.1.1", "8.8.8.8"]
        self.language: str = "en-us"
        self.caching: bool = False
        self.delta_crawl: bool = False
        self.export_to: str = os.path.join(os.getcwd(), "exports")
        self.exporters: list = []

        if params:
            for key, value in params.items():
                setattr(self, key, value)

            # delta_crawl requires caching to compare against the previous run
            if self.delta_crawl and not self.caching:
                self.caching = True
                LOG.info("Auto-enabled caching (required for delta_crawl)")
