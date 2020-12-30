# FAQs

#### How can I access scraped data directly, i.e. without running any exporters?
Currently, there are two ways to do this:

1. Use `crawler.data` to obtain a list of either data dictionaries if `selectors` are defined or the HTML documents
2. Use `crawler.pages` to get the results as list of [Page](/microwler/scraping#microwler.scrape.Page) objects

#### What's the roadmap for this project?
Microwler is a very young project (started 12/2020) and currently maintained by only one person.
Nevertheless, there *is* a list of features to implement eventually:

- Provide more plug-and-play selectors
- Implement a hook/plugin system with more flexibility (tbd)