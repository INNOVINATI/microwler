# Configuration
**Microwler** projects can be written in a single Python module using a declarative approach. 
Per default, the crawler will visit every qualified link it can find and retrieve the corresponding page content.
Of course, you can customize and extend this behaviour. Here's an example:

````python
from microwler import Microwler, scrape, export

selectors = {
    # Using custom XPath expressions:
    'field': '//some/xpath',
    # Using built-in selectors:
    'title': scrape.title,
    # Using Parsel selectors:
    'complex': lambda dom: dom.css('img').xpath('/@src').getall()
}

settings = {
    'exporters': [export.JSONExporter],
    'max_depth': 5
}

def transformer(data: dict):
    # Do something here, i.e. modify/add fields defined in selectors
    return data

crawler = Microwler(
    'START_URL',
    select=selectors,
    transform=transformer,
    settings=settings
)
````

> **Create a new project with this template:** 
> `new <PROJECT_NAME> <START_URL>`

You'll find out more about *selectors* and *transformers* in the next chapter(s). For now, let's focus
on the various settings of the crawler itself.

## Settings
You can change your crawler's behaviour using the `settings` parameter. It holds various configurations
for the crawler itself but also for handling exports and such.

| Setting | Default | Description |
| :------------- | :-------------: | -----------: |
| link_filter | `//a/@href` | XPath for link extraction, i.e. <br> `//a[contains(@href, 'blog')]/@href`
| max_depth | 10 | The depth limit at which to stop crawling |
| max_concurrency | 20 | Maximum number of concurrent requests |
| dns_providers | `['1.1.1.1', '8.8.8.8']` | DNS server addresses, i.e. Cloudflare or Google |
| language | 'en-us' | Will be used to in the `Accept-Language` header |
| caching | `False` | Persist results using `diskcache` |
| delta_crawl | `False` | Drop URLs which have been seen in earlier runs |
| export_to | `${CWD}/projects` | The folder in which you want to save exported data files |
| exporters | `[]` | A list of export plugins inheriting from [microwler.export.BaseExporter][] |
