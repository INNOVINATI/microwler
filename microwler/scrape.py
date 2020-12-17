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
            return data[0] if len(data) == 1 else data
        raise ValueError(f'Selector <{func.__name__}> did not return anything. '
                         'Must be the result of either dom.xpath(..) or dom.css(...)')
    return select


@selector
def title(dom):
    return dom.xpath('//title/text()')


@selector
def headings(dom):
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
    return dom.xpath('//p/text()')


@selector
def emails(dom):
    return dom.xpath('//a[starts-with(@href, "mailto")]')
