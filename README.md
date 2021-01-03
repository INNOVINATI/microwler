<img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/logo.png" width="200px" alt="Microwler">

![PyPI - Status](https://img.shields.io/pypi/status/microwler)
![GitHub](https://img.shields.io/github/license/INNOVINATI/microwler)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/INNOVINATI/microwler)

Microwler is a micro-framework for asynchronous web crawling and scraping implemented in Python.
It is designed for *deep* crawls, i.e. retrieving every page of a specific website.
Per default, the crawler will attempt to visit each qualified link it can find and download the 
corresponding page until it reaches the depth limit or the whole site has been visited.

Optionally, you can also:
- cache your results on disk
- use *incremental crawling mode* (only crawl new pages)
- use pre-built common selectors to scrape data
- define custom selectors using XPath & CSS
- define "transformers" to manipulate scraped data after crawling
- use pre-built export plugins or build your own
- crawl dynamic pages (coming soon)

Take a look at `examples/` to find out more or read the [Getting Started guide](https://innovinati.github.io/microwler/getting-started).


## Inspiration
Many concepts were inspired by experience with `Scrapy`, the industry standard for web crawling with Python.
The idea was to design a very minimalistic framework for analysing specific websites.
We tried to focus on making things as simple as possible for developers.
With Microwler, you can build crawlers and extract relevant data in a breeze - and in a single file.

## Contributing
We're happy about every meaningful contribution to this project via pull requests.
If needed, we'll setup more precise guidelines on how to contribute at some point.
