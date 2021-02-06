# FAQs

#### How fast is **Microwler**?
Hard to say. Without having tested it much (yet), the crawler seems to be performing
at 10-100 pages per second, depending on its setup, the responding web 
server and the internet connection between them.

#### How does it work internally?
Microwler tries to keep things simple for you. Thus, most of its features are entirely optional.
It uses various battle-tested libraries to achieve different things like asynchronous crawling, data
extraction, caching and so on. Check the [requirements file](https://github.com/INNOVINATI/microwler/blob/master/requirements.txt) 
to find out more about which libraries are being used internally.
The following image should give you a brief overview of how/when certain features are used.

<img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/workflow.png" width="600px" alt="Microwler Workflow">


#### How can I access scraped data directly, i.e. without running any exporters?
Currently, there are two different ways to do this directly:

1. Use `crawler.results` to obtain a list of result `dict`s (obviously *after* crawling)
3. Use `crawler.cache` to obtain a list of cached pages (after initializing the crawler)

Alternatively, you can pull data via CLI & HTTP and it's advised to do so:

- CLI: `crawler <project_name> dumpcache`
    - Exports the cache to your local filesystem as JSON
- API: `/data/<project_name>`
    - Returns the cache as JSON

#### What are *transformers*?
It sounds more complex than it really is: a *transformer* is any Python callable
which works on a data dictionary. Microwler will inject every crawled page's `data`
into a given transformer function in order to manipulate it after scraping, 
i.e. do some text processing. [Example](https://github.com/INNOVINATI/microwler/blob/master/test_cases.py#L54)

#### Can I persist results, i.e. in a database?
Yes. In fact, Microwler comes with a built-in caching system for storing results on-disk.
You can enable this feature via the `caching` setting. Per default caches will be stored in `${CWD}/.microwler/cache`. 

Optionally, you can activate *incremental crawling* using the `delta_crawl` setting.

Under the hood, Microwler uses [diskcache](https://pypi.org/project/diskcache/) to store results on disk.

#### What's the roadmap for this project?
Microwler is a very young project (started 12/2020) and currently maintained by only one person.
Nevertheless, there *is* a list of features to implement eventually:

- Handle dynamic content / JS-generated sites
- Provide more plug-and-play selectors
- Implement a hook/plugin system with more flexibility (tbd)