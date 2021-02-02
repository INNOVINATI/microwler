import datetime
import logging

from lxml.etree import ParserError
from parsel import Selector

from microwler.utils import get_first_or_list


LOG = logging.getLogger(__name__)


class Page(object):
    """
    Internal representation of a webpage

    > The methods `scrape()` and `transform()` will be called by the crawler instance
    > if selectors and a corresponding transformer function are defined.
    """

    def __init__(self, url: str, status_code: int, depth: int, links: list = None, html: bytes = None):
        """
        Arguments:
            url: the URL of this page
            status_code: the request's getStatus code
            depth: the depth at which this page was crawled
            links: list of internal links found on this page
            html: HTML body
        """
        self.url = url
        self.discovered = datetime.date.today().strftime('%Y-%m-%d')
        self.status_code = status_code
        self.depth = depth
        self.links = links
        self.html = html
        self.data = {}

    def scrape(self, selectors: dict, keep_source=False):
        """
        Extracts data using the given selectors. Selectors are either `XPaths` (strings) or callables.
        If a callable is given, it will receive the parsed DOM as only argument,
        which is a [Parsel selector](https://parsel.readthedocs.io/en/latest/usage.html#using-selectors) instance.
        This means you can apply `dom.xpath(...)` or `dom.css(...)` and return any native Python datatype you want.

        > Note: The selected data items will be stored in `Page.data`, which is a Python `dict`
        """

        try:
            dom = Selector(text=self.html)
            for field, selector in selectors.items():
                if type(selector) == str:
                    self.data[field] = get_first_or_list(dom.xpath(selector))
                else:
                    self.data[field] = selector(dom)
        except ParserError as e:
            LOG.warning(f'Parsing error: {e}')

        if not keep_source:
            del self.html

        return self

    def transform(self, func):
        """
        Applies a given function to this page's data.
        Recommended usage of transformers is to manipulate the input (`self.data`)
        and return the whole thing. If nothing is returned, the page's data property
        will be set to None.

        Arguments:
            func: a Python callable
        """
        if len(self.data):
            try:
                self.data = func(self.data)
                return self
            except Exception as e:
                LOG.warning(f'Transformer error: {e}')
                return self
        raise ValueError('You need to provide selectors in order to use a transformer')
