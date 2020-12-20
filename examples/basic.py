from microwler import Crawler

if __name__ == '__main__':
    crawler = Crawler('https://quotes.toscrape.com/')
    crawler.run(verbose=True)
    print(len(crawler.data))
