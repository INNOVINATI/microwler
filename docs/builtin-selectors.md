
Use these selectors for common scraping tasks, for instance:

```
selectors = {
    'title': scrape.title,
    'text': scrape.text,
}
```

> Note: you must not call the selector functions! The `dom` argument
> will be auto-injected by every `Page` object and represents a `parsel.Selector`
> of the whole HTML document.

::: microwler.scrape
    rendering:
      show_root_heading: true
      show_source: true
