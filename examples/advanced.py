from microwler import Crawler, scrape
from microwler.export import JSONExporter, HTMLExporter

selectors = {
    'title': scrape.title,
    'headings': scrape.headings,
    'p_count': lambda dom: len(dom.xpath('//p'))    # Provide custom selectors with callables
}

settings = {
    'max_depth': 5,
    'max_concurrency': 50,
    'download_delay': 1,
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
        selectors=selectors,
        transformer=transform,
        settings=settings
    )
    crawler.run(verbose=True, sort_urls=True)
    print(len(crawler.data))
