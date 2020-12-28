# Documentation

<img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/logo.png" width="200px" alt="Microwler">

![GitHub](https://img.shields.io/github/license/INNOVINATI/microwler)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/INNOVINATI/microwler)

**Microwler** is a micro-framework for asynchronous web crawling and scraping implemented in Python. 
It is designed for deep crawls, i.e. retrieving every page of a specific website. 
Per default, the crawler will attempt to visit each qualified link it can find and download the 
corresponding page until it reaches the depth limit or the whole site has been visited.
Optionally, you can also:

- use pre-built common selectors
- define custom selectors using XPath & CSS
- define "transformers" to manipulate scraped data after crawling
- use pre-built export plugins or build your own
- crawl dynamic pages (coming soon)

Turn any website into an API within a breeze - and a single file.