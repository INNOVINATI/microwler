from microwler import Crawler, scrape

selectors = {
    'title': scrape.title,
    'headings': scrape.headings,
}

settings = {
    'max_depth': 5,
    'max_concurrency': 50,
    'download_delay': 1
}

if __name__ == '__main__':
    crawler = Crawler('https://quotes.toscrape.com/', selectors=selectors, settings=settings)
    crawler.run(verbose=True)
    print(len(crawler.data))
