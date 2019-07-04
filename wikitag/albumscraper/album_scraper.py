# TODO: fix import syntax
from albumscraper.scrapymodules.albums_spider import AlbumsSpider
from scrapy.crawler import CrawlerProcess


class AlbumScraper:
    """The purpose of this class it provide a an easy-to-use API for people who have no knowledge of Scrapy. It also
    makes it possible to internally collect data extracted from Scrapy as opposed to having to save the data to
    physical files!

    WARNING: It's important to know that run() can only be used once due to the nature of the Scrapy framework!"""

    # allows users to decided which urls to request
    def __init__(self, urls):
        self._memory_link = []  # Takes advantage of call by sharing to retrieve parsed data.
        self._albums = []
        self._spider = AlbumsSpider(memory_link=self._memory_link)
        self.urls = urls

    @property
    def albums(self):
        return self.__dict__['_albums']

    @property
    def urls(self):
        return self.__dict__['_spider'].urls  # Just keep the URL stored in one place (inner class attribute)

    @urls.setter
    def urls(self, urls):
        """Simplifies the url-setting process"""

        # this class was designed to only handle one album: no other sequences/iterables should be allowed
        if isinstance(urls, str):
            self._spider.urls.append(urls)
        else:
            self._spider.urls.extend(urls)

    # Store the scraper's album data and flush the memory link
    def _flush_memory_link(self):
        self._albums = self._memory_link[0]  # without a copy some serious bugs would occur!
        self._memory_link.clear()

    def crawl(self):
        """Allow the Scraper's inner spider to crawl across Requests and store album data"""
        process = CrawlerProcess()  # no settings needed, they are defined in the Spider
        process.crawl(self._spider, self._memory_link)
        process.start()
        self._flush_memory_link()  # store the album data in the Scraper's album attribute and flush the link.


# TODO: need to make this be able to scrape multiple albums!!!!!!!!!!!
if __name__ == '__main__':
    album_url = 'https://en.wikipedia.org/wiki/Rodeo_(Travis_Scott_album)'
    hm = AlbumScraper(url=album_url)
    hm.crawl()
    print(hm.albums)
