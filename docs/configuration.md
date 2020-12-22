# Configuration
Per default, the crawler will visit every qualified link it can find at retrieve the corresponding page content.
Of course, you can customize and extend this behaviour.

::: microwler.crawler.Crawler
    rendering:
      show_root_heading: true



## Settings
You can further tune your crawler using the `settings` parameter. It holds various configurations
for the crawler itself, but also for any extensions/plugins you might want to use or build.

### Crawler settings

#### `settings.max_depth`
The depth limit at which to stop crawling
> Default: 10

#### `settings.max_concurrency`
Maximimum number of concurrent requests
> Default: 20


#### `settings.language`
Will be used to in the `Accept-Language` header
> Default: 'en-us'


### Export settings

#### `settings.export_to`
The folder in which you want to save exported data files
> Default: ${CWD}/projects

#### `settings.exporters`
A list of export plugins inheriting from [microwler.export.BaseExporter]().
> Default: [ ]

### Extensions / Plugins
*coming soon*...