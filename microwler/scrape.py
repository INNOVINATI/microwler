import logging

from html_text import extract_text
from lxml.etree import ParserError
from lxml import html as DOMParser


class Page(object):
    """
    Represents a crawled page.
    Arguments:
        url: the URL of this page
        status_code: the request's status code
        depth: the depth at which this page was crawled
        links: list of internal links found on this page
        data: HTML body OR data dictionary (if [selectors](#selectors)) are defined
    """

    def __init__(self, url: str, status_code: int, depth: int, links: list = None, data: dict = None):
        self.url = url
        self.status_code = status_code
        self.depth = depth
        self.links = links
        self.data = data

    def scrape(self, selectors: dict):
        """
        Extracts data using the given selectors. Selectors are either `XPaths` (strings) or callables.
        If a callable is given, it will receive the parsed DOM as only argument,
        which is an [lxml.html.HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html) instance. This means you can apply dom.xpath(...) or dom.css(...)
        from `lxml.etree._Element` and return whatever you want.
        """
        try:
            dom = DOMParser.fromstring(self.data)
            self.data = {field: dom.xpath(selector) if (type(selector) == str) else selector(dom)
                         for field, selector in selectors.items()}
        except ParserError as e:
            logging.warning(f'Parsing error: {e}')


def title(dom):
    """ Extract <title> tag """
    return dom.xpath('//title//text()')


def headings(dom):
    """ Extract heading tags, i.e. <h1>, <h2>, ... """
    return {
        'h1': dom.xpath('//h1//text()'),
        'h2': dom.xpath('//h2//text()'),
        'h3': dom.xpath('//h3//text()'),
        'h4': dom.xpath('//h4//text()'),
        'h5': dom.xpath('//h5//text()'),
        'h6': dom.xpath('//h6//text()')
    }


def paragraphs(dom):
    """ Extract <p> tags """
    return dom.xpath('//p/text()')


def text(dom):
    """ Extract and clean text content """
    return extract_text(str(dom))


def meta(dom):
    """ Extract <meta> tags """
    tags = dom.xpath('//meta')
    return {tag.get('name'): tag.get('content') for tag in tags}


def canonicals(dom):
    """ Extract <link rel='canonical'> tags """
    return dom.xpath('//link[@rel=’canonical’]/@href')


def schemas(dom):
    """ Extract itemtype schemas """
    schema_links = dom.xpath('//*[@itemtype]/@itemtype')
    return [link.split('/')[-1] for link in schema_links]


def emails(dom):
    """ Extract email addresses from <a> tags """
    hrefs = dom.xpath('//a[starts-with(@href, "mailto")]/@href')
    return [href.strip('mailto:') for href in hrefs]


def images(dom):
    """ Extract URLs from <img> tags """
    return dom.xpath('//img/@src')
