import scrapy

from albumscraper.datamanagement.data_extractors import *
from albumscraper.scrapymodules.album import Album


# Design a spider that is compatible with the Scrapy API (not reflective of this program's usage/behavior).
class AlbumsSpider(scrapy.Spider):
    name = "albums"
    custom_settings = {'ITEM_PIPELINES': {'albumscraper.scrapymodules.album_pipeline.AlbumPipeline': 0},
                       'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
    urls = []

    # needed to retrieve parsed results
    def __init__(self, memory_link):
        super().__init__()
        self.memory_link = memory_link  # Takes advantage of call by sharing to retrieve Albums from the AlbumPipeline

    # although unnecessary, this ensures the urls of multiple Spiders/Scrapers are not shared across instances
    def start_requests(self):
        """Returns an iterable of requests which the Spider will crawl from."""

        # no need to copy the URL's: they're not being modified
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        album = Album()
        extract_info(response, album)
        # extract_info(response, album)
        yield album  # send the Album to the AlbumPipeline

    # view settings for debugging
    def view_settings(self):
        print('Existing settings: {}'.format(self.settings.attributes.keys()))
