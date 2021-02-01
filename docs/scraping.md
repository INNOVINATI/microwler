# Scraping Data
Before diving into the actual scraping process, let's take a look at how **Microwler** represents
the data it's working with.

::: microwler.page.Page
    rendering:
        show_root_heading: true

## Selectors
In most cases, you'll want to extract or calculate some data based on the HTML documents you crawl.
For this scenario, **Microwler** allows you to define *selectors*, which can extract data using
`XPath` or `CSS` expressions - or use the ones we already built for you.

### Generic
If you're really lazy, use the built-in selectors:

```python
from microwler import scrape

selectors = {
    'title': scrape.title,
    'headings': scrape.headings,
    'text': scrape.text
}
```

> Note: You can manipulate data after crawling is finished by  defining a `transformer` function.

The generic selectors will return a single element whenever it makes sense, i.e. `scrape.title` would
give you the text content of the `<title>` tag as a string.
Check all available selectors in the [source file](https://github.com/INNOVINATI/microwler/blob/master/microwler/scrape.py).


### Custom
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

In case you want to do something more complex, you can also choose to *define 
selectors as callables*, i.e. lambda expressions or regular functions, 
which is what the crawler does when using generic seletors. 
In this case, **Microwler** will inject the current HTML document as [`parsel.Selector`](https://parsel.readthedocs.io/en/latest/parsel.html#parsel.selector.Selector):

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
it also allows you to *chain selectors* and/or use regex expressions.
> For more info read the Parsel docs: https://parsel.readthedocs.io/en/latest/usage.html
