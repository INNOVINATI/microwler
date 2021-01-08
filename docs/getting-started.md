# Getting Started

## Installation
Before you start, create a workspace/folder for **Microwler** projects and enter it:
```bash
mkdir microwler && cd $_
```

Now, create a virtual environment using Python 3.7 or higher and activate it:
```bash
virtualenv venv -p python3.x && source venv/bin/activate
```

Install `microwler` from PyPI:
```bash
pip install microwler
```

## Usage
### CLI (recommended)
> Recommended since v0.1.2

Before you start, create a workspace as suggested in the [setup guide](#installation)
and activate its virtual environment.

Within this folder, **create a new project** providing the URL to start
crawling with:
```bash
new https://quotes.toscrape.com/
```
**Microwler** will create a `projects/` folder in your current working directory and place
a file called `quotes_toscrape_com.py` within it. This file contains your crawler definition.

To **run this project**, execute the following command:
```bash
crawler quotes_toscrape_com run
```
> Note: this will most likely create a `.microwler` folder in your workspace
> where internal stuff like caches will be stored. Mess with it at your own risk!

You can **check available commands** with:
```bash
microwler
```

### Script
Simply create a [microwler.core.crawler.Crawler][] instance and `run` it:

```python
from microwler import Microwler

crawler = Microwler('https://quotes.toscrape.com/')
crawler.run(verbose=True)
for page in crawler.pages:
    print(page.url, page.html)
```
Without any further configuration, the crawler will try to visit every qualified link it can find and download
every page's content. For more advanced scenarios, check out the rest of this documentation.

> Note: If you're planning on using the webservice or the "project" system in general, you should use the CLI
as recommended above.