# Microwler
As the name suggests, Microwler is a "micro" web crawling framework implemented in Python. It is designed for
deep crawls, i.e. retrieving every page of a specific website. Per default, the crawler will attempt
to visit each qualified link it can find and download the corresponding page until it reaches the depth limit or
the whole site has been visited.

Optionally, you can also:
- define selectors using `lxml` (XPath & CSS)
- cluster results by URL (coming soon)
- define custom export plugins (coming soon)
- crawl dynamic pages using `Selenium` (coming soon)

## Inspiration
We wanted to design a very minimalistic framework for analysing specific websites. Since this use case
doesn't require much scalability, we tried to instead focus on making things as simple as possible for developers.
With Microwler, you can build crawlers and extract relevant data in a breeze.

Built with:
- Python 3.9
- aiohttp & asyncio
- lxml

## Getting Started
coming soon...

## Usage
coming soon...

## Contributing
coming soon...


## License

Copyright © 2020 Maximilian Wolf

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.