from html_text import extract_text

from microwler.utils import remove_multi_whitespace


def title(dom):
    """ Extract <title> tag """
    return dom.xpath('string(//title[1])').get()


def headings(dom):
    """ Extract heading tags, i.e. <h1>, <h2>, ... """
    return {
        'h1': remove_multi_whitespace(dom.xpath('string(//h1[1])').getall()),
        'h2': remove_multi_whitespace(dom.xpath('string(//h2[1])').getall()),
        'h3': remove_multi_whitespace(dom.xpath('string(//h3[1])').getall()),
        'h4': remove_multi_whitespace(dom.xpath('string(//h4[1])').getall()),
        'h5': remove_multi_whitespace(dom.xpath('string(//h5[1])').getall()),
        'h6': remove_multi_whitespace(dom.xpath('string(//h6[1])').getall())
    }


def paragraphs(dom):
    """ Extract <p> tags """
    return dom.xpath('string(//p[1])').getall()


def text(dom):
    """ Extract and clean text content """
    return extract_text(str(dom))


def meta(dom):
    """ Extract <meta> tags """
    tags = dom.xpath('//meta')
    return {tag.get('name'): tag.attrib['content'] for tag in tags}


def canonicals(dom):
    """ Extract <link rel='canonical'> tags """
    return dom.xpath('//link[@rel=’canonical’]/@href').getall()


def schemas(dom):
    """ Extract itemtype schemas """
    schema_links = dom.xpath('//*[@itemtype]/@itemtype').getall()
    return [link.split('/')[-1] for link in schema_links]


def emails(dom):
    """ Extract email addresses from <a> tags """
    hrefs = dom.xpath('//a[starts-with(@href, "mailto")]/@href').getall()
    return [href.strip('mailto:') for href in hrefs]


def images(dom):
    """ Extract URLs from <img> tags """
    return dom.xpath('//img/@src').getall()
