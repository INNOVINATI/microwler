# Getting Started

## Installation
<div id="termynal1" data-termynal>
    <span data-ty="input">mkdir microwler && cd $_</span>
    <span data-ty="input">virtualenv venv -p python3</span>
    <span data-ty="input">source venv/bin/activate</span>
    <span data-ty="input">pip install microwler</span>
    <span data-ty="progress"></span>
    <span data-ty>Successfully installed Microwler</span>
</div>

## Usage
### CLI (recommended)
#### Create a project and run it
> Make sure you created a workspace as suggested above [previous section](#installation). 

<div id="termynal2" data-termynal>
    <span data-ty="input">new quotes https://quotes.toscrape.com/</span>
    <span data-ty data-ty-delay="250" style="color: green">Created new project: /Users/max/microwler/projects/quotes.py</span>
    <span data-ty="input">crawler quotes run</span>
    <span data-ty data-ty-delay="50">[INFO] Starting engine ...</span>
    <span data-ty data-ty-delay="50">[INFO] Crawler started [quotes.toscrape.com]</span>
    <span data-ty="progress"></span>
    <span data-ty>[INFO] Crawler stopped [quotes.toscrape.com]</span>
</div>

Microwler will create a `projects/` folder in your current working directory and place
a file called `quotes.py` within it. This file contains your [crawler configuration](/microwler/configuration).

Depending on your setup, this will also create a `.microwler` folder in your workspace
where internal stuff like caches will be stored. Mess with it at your own risk!

#### Check available commands
You can check available commands with:
```bash
microwler
```

### Script
> **Important**: If you're planning on using the webservice or the "project" system in general, you should use the CLI
as recommended above. It will create an optimized workspace in which you can develop and run your projects.

#### Run directly

Simply create a crawler instance and `run` it:

```python
from microwler import Microwler

crawler = Microwler('https://quotes.toscrape.com/')
crawler.run(verbose=True)
for page in crawler.results:
    print(page)
```

#### Run from asyncio app

If you want to start your crawler from an application that is already running an `asyncio` event loop,
you should use `Microwler.run_async(loop)`. Here's a simple example:

```python
...
crawler = Microwler(...)
loop = asyncio.get_event_loop()
await crawler.run_async(event_loop=loop)
print(crawler.results)
```


<script src="/js/termynal.js" data-termynal-container="#termynal1|#termynal2"></script>
