from html_text import extract_text


def title(dom):
    """ Extract <title> tag """
    return dom.xpath('//title//text()').getall()


def headings(dom):
    """ Extract heading tags, i.e. <h1>, <h2>, ... """
    return {
        'h1': dom.xpath('//h1//text()').getall(),
        'h2': dom.xpath('//h2//text()').getall(),
        'h3': dom.xpath('//h3//text()').getall(),
        'h4': dom.xpath('//h4//text()').getall(),
        'h5': dom.xpath('//h5//text()').getall(),
        'h6': dom.xpath('//h6//text()').getall()
    }


def paragraphs(dom):
    """ Extract <p> tags """
    return dom.xpath('//p//text()').getall()


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
