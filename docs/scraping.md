# Scraping Data
**Microwler** provides several ways of extracting data from web pages by defining *selectors*. 
If you're familiar with Scrapy selectors, you will notice a strong similarity - 
because both use the excellent `Parsel` library. This allows you to [build
complex selectors](#parsel) with XPath, CSS and RegEx, even offering the possibility to chain selectors. 
Alternatively, you can use the [generic selectors](#generic) that are built-in or use simple [XPath strings](#xpath). 
Let's check it out!

## Selectors

### Generic
If you're really lazy, just use the *built-in selectors*. For instance:

```python
from microwler import scrape

selectors = {
    'title': scrape.title,
    'headings': scrape.headings,
    'text': scrape.text
}
```

These generic selectors will return a single element whenever it makes sense, i.e. `scrape.title` would
give you the text content of the `<title>` tag as a string. 
You can find all currently available selectors in the [microwler.scrape][] module.


### Custom
#### XPath
If you want more control over the scraping process, you
can simply provide XPaths. **Microwler** will return a single element if there
was only one match or return the whole result list.

```python
from microwler import scrape

selectors = {
    'title': '//title//text()',
    'h1': '//h1//text()',
    'text': scrape.text
}
```

#### Parsel
In case you want to do something more complex, you can also choose to *define 
selectors as callables*, i.e. lambda expressions or regular functions, 
which is what the crawler does when using generic selectors. 
In this case, the current HTML document will be injected as only argument 
in the form of a [parsel.Selector](https://parsel.readthedocs.io/en/latest/parsel.html#parsel.selector.Selector):

```python
def headings(dom):
    hs = ['h1', 'h2', 'h3', 'h4']
    return {h: dom.css(h).getall() for h in hs}


selectors = {
    'title': lambda dom: ' '.join(dom.xpath('//title//text()').getall()),
    'headings': lambda dom: headings(dom)
}
```

These examples are very basic and do not show the full power of `Parsel`. For instance,
it also allows you to *chain selectors* and/or use regex expressions. For more info 
read the [Parsel documentation](https://parsel.readthedocs.io/en/latest/usage.html).


## Data format
Internally, an HTML document is represented as `Page`. Here's a JSON representation of what this could look like, which corresponds to the output of 
[this source code](https://github.com/INNOVINATI/microwler/blob/master/test_cases.py#L37).

```json
{
  --- Common Page attributes ---
  "url": "https://quotes.toscrape.com/",
  "status_code": 200,
  "discovered": "2021-01-13",
  "depth": 0,
  "links": [
    "https://quotes.toscrape.com/tag/inspirational/",
    "https://quotes.toscrape.com/tag/inspirational/page/1/"
  ],
  --- Custom data fields defined by selectors (and/or transformer function) ---
  "data": {
    "title": "QUOTES TO SCRAPE",
    "headings": {
      "h1": [
        "Quotes to Scrape"
      ],
      "h2": [
        "Top Ten tags"
      ],
      ...
    },
    "paragraphs": 1,
    "images": []
  }
}
```

Retrieve data after running the crawler (i.e. directly from a script) with `crawler.results`

If you want to retrieve a list of cached pages you can use `crawler.cache`