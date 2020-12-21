<img src="https://github.com/INNOVINATI/microwler/blob/master/logo.png" width="200px" alt="Microwler">

![GitHub](https://img.shields.io/github/license/INNOVINATI/microwler)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/INNOVINATI/microwler)

Microwler is a micro-framework for asynchronous web crawling implemented in Python. 
It is designed for deep crawls, i.e. retrieving every page of a specific website. 
Per default, the crawler will attempt to visit each qualified link it can find and download the 
corresponding page until it reaches the depth limit or the whole site has been visited.

Optionally, you can also:
- use pre-built common selectors
- define custom selectors using XPath & CSS
- define "transformers" to manipulate scraped data after crawling
- use pre-built export plugins or build your own
- crawl dynamic pages (coming soon)

## Inspiration
Many concepts were inspired by experience with `Scrapy`, the industry standard for web crawling with Python.
The idea was to design a very minimalistic framework for analysing specific websites. We tried to focus on making things as simple as possible for developers.
With Microwler, you can build crawlers and extract relevant data in a breeze - and in a single file.

Built with:
- Python 3.9
- aiohttp & asyncio
- lxml



## Getting Started
coming soon...

## Usage
### Python script
```python
from microwler import Crawler, scrape

crawler = Crawler('https://quotes.toscrape.com/', selectors={'title': scrape.title})
crawler.run(verbose=True)
```
Take a look at `examples/` to find out more.

### Command line
coming soon...
## Contributing
coming soon...


## License

Copyright © 2020 Maximilian Wolf

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
