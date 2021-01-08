# Documentation

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

If you're familiar with **Microwler**, you can install the package directly from PyPI using:<br> 
`pip install microwler`

<hr>

<small>
**Copyright (C) 2021 Maximilian Wolf**

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
</small>