from html_text import extract_text
from parsel import Selector as ParselSelector
from typing import Callable

from microwler.utils import remove_multi_whitespace


def title(dom: ParselSelector):
    """ Extract `<title>` tag """
    return dom.xpath('string(//title[1])').get()


def headings(dom: ParselSelector):
    """ Extract first 3 levels of heading tags: `<h1>`, `<h2>`, `<h3>` """
    return {
        'h1': remove_multi_whitespace(dom.xpath('string(//h1[1])').getall()),
        'h2': remove_multi_whitespace(dom.xpath('string(//h2[1])').getall()),
        'h3': remove_multi_whitespace(dom.xpath('string(//h3[1])').getall()),
    }


def paragraphs(dom: ParselSelector):
    """ Extract `<p>` tags """
    return dom.xpath('string(//p[1])').getall()


def text(dom: ParselSelector):
    """ Extract and clean text content """
    return extract_text(dom.xpath('//body').get())


def meta(dom: ParselSelector):
    """ Extract `<meta>` tags """
    tags = dom.xpath('//meta')
    return {tag.get('name'): tag.attrib['content'] for tag in tags}


def canonicals(dom: ParselSelector):
    """ Extract `<link rel='canonical'>` tags """
    return dom.xpath('//link[@rel="canonical"]/@href').getall()


def schemas(dom: ParselSelector):
    """ Extract itemtype schemas """
    schema_links = dom.xpath('//*[@itemtype]/@itemtype').getall()
    return [link.split('/')[-1] for link in schema_links]


def emails(dom: ParselSelector):
    """ Extract email addresses from `<a>` tags """
    hrefs = dom.xpath('//a[starts-with(@href, "mailto")]/@href').getall()
    return [href.strip('mailto:') for href in hrefs]


def images(dom: ParselSelector):
    """ Extract URLs from `<img>` tags """
    return dom.xpath('//img/@src').getall()


def selector(user_func: Callable[[ParselSelector, str], object]):
    """ Execute user-defined function on parsel.Selector """

    def wrapper(dom: ParselSelector):
        return user_func(dom)

    return wrapper
