# TODO: fix import syntax
from albumscraper.scrapymodules.albums_spider import AlbumsSpider
from scrapy.crawler import CrawlerProcess


class AlbumScraper:
    """This class's purpose is to unify the scraping process and provide an API that is more appropriate for wiki-tag's
    intended usage (some Scrapy conventions don't make sense but need to be implemented)."""

    # allows users to decided which urls to request
    def __init__(self, url):
        self._memory_link = []  # Takes advantage of call by sharing to retrieve parsed data.
        self._album = None
        self._Spider = AlbumsSpider
        self.url = url

    @property
    def album(self):
        return self.__dict__['_album']

    @property
    def url(self):
        return self.__dict__['Spider'].urls  # Just keep the URL stored in one place (inner class attribute)

    @url.setter
    def url(self, url):
        """Manages the url-setting process. This is needed because Spiders are designed to handle multiple
        URL's but this class was designed to only accept one."""
        if len(self._Spider.urls):
            self._Spider.urls.clear()  # ensures there aren't accidentally multiple URL's

        # this class was designed to only handle one album: no other sequences/iterables should be allowed
        if isinstance(url, str):
            self._Spider.urls.append(url)
        else:
            raise TypeError('Only one URL can be passed: no sequences allowed!')  # TODO: try to find a message example

    # Store the scraper's album data and flush the memory link
    def _flush_memory_link(self):
        self._album = self._memory_link[0]  # without a copy some serious bugs would occur!
        self._memory_link.clear()

    def crawl(self):
        """Allow the Scraper's inner spider to crawl across Requests and store album data"""
        process = CrawlerProcess()  # no settings needed, they are defined in the Spider
        process.crawl(self._Spider, self._memory_link)
        process.start()
        self._flush_memory_link()  # store the album data in the Scraper's album attribute and flush the link.


if __name__ == '__main__':
    album_url = 'https://en.wikipedia.org/wiki/Rodeo_(Travis_Scott_album)'
    hm = AlbumScraper(url=album_url)
    hm.crawl()
    print(hm.album)
