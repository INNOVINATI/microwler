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
Copyright 2020-2021 Maximilian Wolf

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
