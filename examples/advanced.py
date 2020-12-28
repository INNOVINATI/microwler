from microwler import Crawler, scrape
from microwler.export import JSONExporter, HTMLExporter


select = {
    'title': scrape.title,
    'headings': scrape.headings,
    # Define custom selectors as lambdas or functions (Microwler will inject the page as lxml.html.HtmlElement)
    'p_count': lambda dom: len(dom.xpath('//p'))
}

settings = {
    'max_depth': 10,
    'max_concurrency': 15,
    'export_to': './export/project_folder',
    'exporters': [JSONExporter, HTMLExporter]
}


def transform(data: dict):
    """ Define a transformer to manipulate your scraped data """
    data['title'] = data['title'].upper()
    return data


if __name__ == '__main__':
    crawler = Crawler(
        'https://quotes.toscrape.com/',
        selectors=select,
        transformer=transform,
        settings=settings
    )
    crawler.run(verbose=True, sort_urls=True)
