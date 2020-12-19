import functools
from lxml.html import HtmlElement


def selector(func):
    """
    Wrapper for injecting the current page into selector functions
    The wrapped function MUST return the result of either dom.xpath(..) or dom.css(...)
    """
    @functools.wraps(func)
    def select(dom: HtmlElement):
        data = func(dom)
        if data is not None:
            # We always receive lists, so let's handle that nicely
            return data[0] if len(data) == 1 else data
        # Force return value
        raise ValueError(f'Selector <{func.__name__}> did not return anything.')
    return select


@selector
def title(dom):
    """ Extract <title> tag """
    return dom.xpath('//title/text()')


@selector
def headings(dom):
    """ Extract heading tags, i.e. <h1>, <h2>, ... """
    return {
        'h1': dom.xpath('//h1/text()'),
        'h2': dom.xpath('//h2/text()'),
        'h3': dom.xpath('//h3/text()'),
        'h4': dom.xpath('//h4/text()'),
        'h5': dom.xpath('//h5/text()'),
        'h6': dom.xpath('//h6/text()')
    }


@selector
def paragraphs(dom):
    """ Extract <p> tags """
    return dom.xpath('//p/text()')


@selector
def meta(dom):
    """ Extract <meta> tags """
    tags = dom.xpath('//meta')
    return {tag.get('name'): tag.get('content') for tag in tags}


@selector
def canonicals(dom):
    """ Extract <link rel='canonical'> tags """
    return dom.xpath('//link[@rel=’canonical’]/@href')


@selector
def schemas(dom):
    """ Extract itemtype schemas """
    schema_links = dom.xpath('//*[@itemtype]/@itemtype')
    return [link.split('/')[-1] for link in schema_links]


@selector
def emails(dom):
    """ Extract email addresses from <a> tags """
    hrefs = dom.xpath('//a[starts-with(@href, "mailto")]/@href')
    return [href.strip('mailto:') for href in hrefs]
