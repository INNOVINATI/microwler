# Examples
> Before you start, you should read the [Getting Started](/getting-started) guide.

## Basic
Run the crawler with a `start_url` and no further configuration.
```python
from microwler import Crawler

crawler = Crawler('https://quotes.toscrape.com/')
crawler.run(verbose=True)
for page in crawler.pages:
    print(page.url, page.html)
```

## Intermediate
Add pre-defined selectors and some settings.

```python

from microwler import Crawler, scrape

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
```

## Advanced
Run the crawler with a fully configured pipeline:

1. Crawl every page
2. Sort results
3. Apply selectors
4. Apply transformer
5. Run exporters

```python
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


crawler = Crawler(
    'https://quotes.toscrape.com/',
    selectors=select,
    transformer=transform,
    settings=settings
)
crawler.run(verbose=True, sort_urls=True)
# use crawler.data or crawler.pages as shown above to interact with the results
```