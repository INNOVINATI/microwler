from microwler import Crawler, scrape

selectors = {
    'title': scrape.title,
    'headings': scrape.headings,
}

settings = {
    'max_depth': 5,
    'max_concurrency': 30,
}

if __name__ == '__main__':
    crawler = Crawler('https://quotes.toscrape.com/', selectors=selectors, settings=settings)
    crawler.run(verbose=True)
    for page_data in crawler.data:
        print(f'\n{page_data["url"].upper()}')
        for key, value in page_data.items():
            print(f'> {key.upper()}: {value}')

