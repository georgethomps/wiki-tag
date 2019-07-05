# TODO: fix import syntax
from albumscraper.scrapymodules.albums_spider import AlbumsSpider
from scrapy.crawler import CrawlerProcess


class AlbumScraper:
    """The purpose of this class it provide a an easy-to-use API for people who have no knowledge of Scrapy. It also
    makes it possible to internally collect data extracted from Scrapy as opposed to having to save the data to
    physical files!

    WARNING: It's important to know that run() can only be used once due to the nature of the Scrapy framework!
    Furthermore, only one AlbumScraper can be implemented in one's code."""

    # allows users to decided which urls to request
    def __init__(self, urls):
        self._albums = []  # Takes advantage of call by sharing to retrieve parsed data.
        self.urls = urls

    @property
    def albums(self):
        return self.__dict__['_albums']

    @property
    def urls(self):
        return AlbumsSpider.urls  # Just keep the URL stored in one place (inner class attribute)

    @urls.setter
    def urls(self, urls):
        """Simplifies the url-setting process by properly appending sequences or strings"""
        if isinstance(urls, str):
            AlbumsSpider.urls.append(urls)
        else:
            AlbumsSpider.urls.extend(urls)

    # TODO: needs more intelligible name
    def crawl(self):
        """Allow the Scraper's inner spider to crawl across Requests and store album data"""
        process = CrawlerProcess()  # no settings needed, they are defined in the Spider
        process.crawl(AlbumsSpider, self._albums)
        process.start()


# TODO: need to make this be able to scrape multiple albums!!!!!!!!!!!
if __name__ == '__main__':
    album_url = ['https://en.wikipedia.org/wiki/Rodeo_(Travis_Scott_album)', 'https://en.wikipedia.org/wiki/Rap_or_Go_to_the_League']
    hm = AlbumScraper(urls=album_url)
    wtf = hm.urls
    hm.crawl()
    print(hm.albums[1])
