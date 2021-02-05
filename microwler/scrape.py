from html_text import extract_text
import parsel

from microwler.utils import remove_multi_whitespace


def title(dom: parsel.Selector):
    """ Extract `<title>` tag """
    return dom.xpath('string(//title[1])').get()


def headings(dom: parsel.Selector):
    """ Extract first 3 levels of heading tags: `<h1>`, `<h2>`, `<h3>` """
    return {
        'h1': remove_multi_whitespace(dom.xpath('string(//h1[1])').getall()),
        'h2': remove_multi_whitespace(dom.xpath('string(//h2[1])').getall()),
        'h3': remove_multi_whitespace(dom.xpath('string(//h3[1])').getall()),
    }


def paragraphs(dom: parsel.Selector):
    """ Extract `<p>` tags """
    return dom.xpath('string(//p[1])').getall()


def text(dom: parsel.Selector):
    """ Extract and clean text content """
    return extract_text(dom.xpath('//body').get())


def meta(dom: parsel.Selector):
    """ Extract `<meta>` tags """
    tags = dom.xpath('//meta')
    return {tag.get('name'): tag.attrib['content'] for tag in tags}


def canonicals(dom: parsel.Selector):
    """ Extract `<link rel='canonical'>` tags """
    return dom.xpath('//link[@rel="canonical"]/@href').getall()


def schemas(dom: parsel.Selector):
    """ Extract itemtype schemas """
    schema_links = dom.xpath('//*[@itemtype]/@itemtype').getall()
    return [link.split('/')[-1] for link in schema_links]


def emails(dom: parsel.Selector):
    """ Extract email addresses from `<a>` tags """
    hrefs = dom.xpath('//a[starts-with(@href, "mailto")]/@href').getall()
    return [href.strip('mailto:') for href in hrefs]


def images(dom: parsel.Selector):
    """ Extract URLs from `<img>` tags """
    return dom.xpath('//img/@src').getall()
