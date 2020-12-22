# Examples
> Before you start, you should read the [Getting Started](/getting-started) guide.

## Basic
Run the crawler with a `start_url` and no further configuration.
```python
from microwler import Crawler

crawler = Crawler('https://quotes.toscrape.com/')
crawler.run(verbose=True)   # results can be retrieved with crawler.data
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
    'max_concurrency': 50,
}

crawler = Crawler('https://quotes.toscrape.com/', selectors=selectors, settings=settings)
crawler.run(verbose=True)   # results can be retrieved with crawler.data
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

selectors = {
    'title': scrape.title,
    'headings': scrape.headings,
    'p_count': lambda dom: len(dom.xpath('//p'))    # Provide custom selectors with callables
}

settings = {
    'max_depth': 5,
    'max_concurrency': 50,
    'export_to': './export/project_folder',
    'exporters': [JSONExporter, HTMLExporter]
}


def transform(page: dict):
    """ Define a transformer to manipulate your scraped data """
    page['data']['title'] = page['data']['title'].upper()
    return page


crawler = Crawler(
    'https://saaris.de/',
    selectors=selectors,
    transformer=transform,
    settings=settings
)
crawler.run(verbose=True, sort_urls=True)   # results can be retrieved with crawler.data
```