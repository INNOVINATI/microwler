# Getting Started

## Installation
Before you start, create a folder for Microwler projects and enter it:
```bash
mkdir microwler && cd $_
```

Now, create a virtual environment using Python 3.6 or higher and activate it:
```bash
virtualenv venv -p python3.x && source venv/bin/activate
```

Install `microwler` from PyPI:
```bash
pip install microwler
```

## Python script
The recommended way of using **Microwler** is in a regular Python script. Simply create a [microwler.crawler.Crawler][]
instance and `run` it:

```python
from microwler import Crawler

crawler = Crawler('https://quotes.toscrape.com/')
crawler.run(verbose=True)
for page in crawler.pages:
    print(page.url, page.html)
```
Without any further configuration, the crawler will try to visit every qualified link it can find and download
every page's content. For more advanced scenarios, check out the rest of this documentation or take a look at the
[examples in our GitHub repository]('https://github.com/INNOVINATI/microwler/tree/master/examples').

## Command line
coming soon...