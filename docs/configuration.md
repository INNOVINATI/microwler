# Configuration
Per default, the crawler will visit every qualified link it can find at retrieve the corresponding page content.
Of course, you can customize and extend this behaviour.

::: microwler.crawler.Microwler
    rendering:
      show_root_heading: true

## Settings
You can further tune your crawler using the `settings` parameter. It holds various configurations
for the crawler itself, but also for any extensions/plugins you might want to use or build.

> Note: You don't need to create a `Settings` object. Just put your settings in a `dict`.

### Crawler settings

#### `settings.link_filter`
Exclusively extract and follow (internal) links matching this XPath expression.
Use this setting to limit which links will be visited. For instance, using `link_filter: "//a[contains(@href, 'blog')]/@href"`
will only select URLs containing the string `blog` such as `https://example.com/blog/page-1`.
> Default: '//a/@href'

#### `settings.max_depth`
The depth limit at which to stop crawling
> Default: 10

#### `settings.max_concurrency`
Maximum number of concurrent requests
> Default: 20


#### `settings.language`
Will be used to in the `Accept-Language` header
> Default: 'en-us'


#### `settings.caching`
Persist results using `diskcache`
> Default: `False`

#### `settings.delta_crawl`
Incremental crawling mode: drop URLs which have been seen in earlier runs
> Default: `False`

### Export settings

#### `settings.export_to`
The folder in which you want to save exported data files
> Default: `${CWD}/projects`

#### `settings.exporters`
A list of export plugins inheriting from [microwler.export.BaseExporter][].
> Default: `[]`

