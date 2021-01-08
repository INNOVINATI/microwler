<img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/logo.png" width="200px" alt="Microwler">

![PyPI - Status](https://img.shields.io/pypi/status/microwler)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/INNOVINATI/microwler/Run%20Test%20Cases/master)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/INNOVINATI/microwler)

**Microwler** is a micro-framework for asynchronous web crawling and scraping implemented in Python.
It is designed for *deep* crawls, i.e. retrieving every page of a specific website.
Per default, the crawler will attempt to visit each qualified link it can find and download the 
corresponding page until it reaches the depth limit or the whole site has been visited.

Optionally, you can also:
- **cache your results** on disk
- use **incremental crawling** mode (only crawl new pages)
- use **pre-built selectors** to scrape common data, i.e. `<meta>` or `<title>`
- easily define **custom selectors** using XPath & CSS
- define "transformers" to **manipulate scraped data** after crawling
- **export data** with pre-built plugins or build your own
- use the built-in **web service** to run crawlers and fetch data from a remote client

Sounds good? Head over to the [Getting Started guide](https://innovinati.github.io/microwler/getting-started) now!

If you're familiar with **Microwler**, you can install the package from PyPI using: `pip install microwler`.

## Inspiration
Many concepts were inspired by experience with `Scrapy`, the industry standard for web crawling with Python.
The idea was to design a very minimalistic framework for analysing specific websites.
We tried to focus on making things as simple as possible for developers.
With Microwler, you can build crawlers and extract relevant data in a breeze - and in a single file.

## Contributing
We're happy about every meaningful contribution to this project via pull requests.
If needed, we'll setup more precise guidelines on how to contribute at some point.

> Note: you'll need to install `pip install -r requirements-dev.txt` to include required
> dependencies for docs and tests.

## License
Copyright (c) 2020-2021 Maximilian Wolf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
