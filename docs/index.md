# Documentation

<img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/logo.png" width="200px" alt="Microwler">

![PyPI - Status](https://img.shields.io/pypi/status/microwler)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/INNOVINATI/microwler)

**Microwler** is a micro-framework for asynchronous web crawling and scraping implemented in Python. 
It is designed for deep crawls, i.e. retrieving every page of a specific website. 
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

<hr>

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
