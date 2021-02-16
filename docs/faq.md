# FAQs

#### How fast is **Microwler**?
Hard to say. Without having tested it much (yet), the crawler seems to be performing
at 10-100 pages per second, depending on its setup, the responding web 
server and the internet connection between them.


#### How can I persist results?
Microwler comes with a built-in caching system for storing results on-disk.
You can enable this feature via the `caching` setting. Per default caches will be stored in `${CWD}/.microwler/cache`. 

Optionally, you can activate *incremental crawling* using the `delta_crawl` setting.

Under the hood, Microwler uses [diskcache](https://pypi.org/project/diskcache/) to store results on disk.


#### How can I run the crawler within an existing event loop?
As of v0.2.0, Microwler will detect if a loop exists and is running. If so, it will
start the crawler and return an `Awaitable`. Here's an example showing you how to load a project, run its crawler
and retrieve the results:

````python
import asyncio
from microwler.utils import load_project

# create an event loop
loop = asyncio.get_event_loop()
# load the project
project = load_project('project_name', '/path/to/projects/folder')
# run the crawler
await project.crawler.run(verbose=True)
print(project.crawler.results)
````

#### How can I access scraped data directly, i.e. without running any exporters?
Currently, there are two different ways to do this directly:

1. Use `crawler.results` to obtain a list of result `dict`s (obviously *after* crawling)
3. Use `crawler.cache` to obtain a list of cached pages 

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


#### What's the roadmap for this project?
Microwler is a very young project (started 12/2020) and currently maintained by only one person.
Nevertheless, there *is* a list of features to implement eventually:

- Handle dynamic content / JS-generated sites
- Provide more plug-and-play selectors
- Implement a hook/plugin system with more flexibility (tbd)