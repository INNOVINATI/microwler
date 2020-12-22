# Scraping Data
Before diving into the actual scraping process, let's take a look at how **Microwler** represents
the data it's working with.

::: microwler.scrape.Page
    rendering:
        show_root_heading: true
        show_source: True

## Selectors
In most cases, you'll want to extract or calculate some data based on the HTML documents you crawl.
For this scenario, **Microwler** allows you to define *selectors*, which can extract data using
the powerful `XPath` language and/or the `lxml` package.

### Custom

If you're really lazy, just provide an `XPath` string and a field name
and you'll be good to go:

```python
selectors = {
    'title': '//title//text()',
    'h1': '//h1//text()'
}
```

 In case you want to do something more complex, you can also choose to *define 
selectors as callables*, i.e. lambda expressions or regular functions. In this case, **Microwler** will
inject the current HTML document into every selector:

```python
selectors = {
    'title': lambda dom: dom.xpath('//title//text()'),
    'h1': lambda dom: dom.css('h1::text')
}
```

> **Note**: you can use every feature of the [lxml.html.HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html) class,
> but you should always return something!

### Generic

**Microwler** comes with a set of pre-built selectors to save you some time and effort.
You can check them out in the [source file](https://github.com/INNOVINATI/microwler/blob/master/microwler/scrape.py).
Some examples are:

- `<title>` tags: `scrape.title`
- `<hX>` heading tags: `scrape.headings`
- `<p>` tags: `scrape.paragraphs`
- Cleaned text: `scrape.text`
- `<meta>` tags: `scrape.meta`
- ...
