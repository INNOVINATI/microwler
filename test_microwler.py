from microwler import Crawler
from microwler.core import scrape
from microwler.core.export import JSONExporter, HTMLExporter


class TestSuite:
    # TODO: FIX

    def test_basic(self):
        crawler = Crawler('https://quotes.toscrape.com/')
        crawler.run(verbose=True)
        for page in crawler.pages:
            print(page.url, page.html)

    def test_intermediate(self):
        selectors = {
            'title': scrape.title,
            'headings': scrape.headings,
        }

        settings = {
            'max_depth': 5,
            'max_concurrency': 30,
        }

        crawler = Crawler('https://quotes.toscrape.com/', selectors=selectors, settings=settings)
        crawler.run(verbose=True)
        for page_data in crawler.data:
            print(f'\n{page_data["url"].upper()}')
            for key, value in page_data.items():
                print(f'> {key.upper()}: {value}')

    def test_advanced(self):
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
            'exporters': [JSONExporter, HTMLExporter],
            'caching': True,
        }

        def transform(data: dict):
            """ Define a transformer to manipulate your scraped data """
            data['title'] = data['title'].upper()
            return data

        crawler = Crawler(
            'https://quotes.toscrape.com/',
            selectors=select,
            transformer=transform,
            settings=settings
        )
        crawler.run(verbose=True, sort_urls=True)
