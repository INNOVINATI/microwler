import parsel
from html_text import extract_text

from microwler.utils import remove_multi_whitespace


def title(dom: parsel.Selector) -> str | None:
    """Extract `<title>` tag"""
    return dom.xpath("string(//title[1])").get()


def headings(dom: parsel.Selector) -> dict[str, str | list[str]]:
    """Extract first 3 levels of heading tags: `<h1>`, `<h2>`, `<h3>`"""
    return {
        "h1": remove_multi_whitespace(dom.xpath("string(//h1[1])").getall()),
        "h2": remove_multi_whitespace(dom.xpath("string(//h2[1])").getall()),
        "h3": remove_multi_whitespace(dom.xpath("string(//h3[1])").getall()),
    }


def paragraphs(dom: parsel.Selector) -> list[str]:
    """Extract `<p>` tags"""
    return dom.xpath("string(//p[1])").getall()


def text(dom: parsel.Selector) -> str:
    """Extract and clean text content"""
    return extract_text(dom.xpath("//body").get() or "")


def meta(dom: parsel.Selector) -> dict[str, str]:
    """Extract `<meta>` tags"""
    tags = dom.xpath("//meta")
    return {
        name: content
        for tag in tags
        if (name := tag.attrib.get("name")) is not None
        if (content := tag.attrib.get("content")) is not None
    }


def canonicals(dom: parsel.Selector) -> list[str]:
    """Extract `<link rel='canonical'>` tags"""
    return dom.xpath('//link[@rel="canonical"]/@href').getall()


def schemas(dom: parsel.Selector) -> list[str]:
    """Extract itemtype schemas"""
    schema_links = dom.xpath("//*[@itemtype]/@itemtype").getall()
    return [link.split("/")[-1] for link in schema_links]


def emails(dom: parsel.Selector) -> list[str]:
    """Extract email addresses from `<a>` tags"""
    hrefs = dom.xpath('//a[starts-with(@href, "mailto")]/@href').getall()
    return [href.strip("mailto:") for href in hrefs]


def images(dom: parsel.Selector) -> list[str]:
    """Extract URLs from `<img>` tags"""
    return dom.xpath("//img/@src").getall()
