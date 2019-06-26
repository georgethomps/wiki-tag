import scrapy.item


class Album(scrapy.Item):
    artist = scrapy.Field()
    album_artist = scrapy.Field()
    album_title = scrapy.Field()
    year = scrapy.Field()
    genres = scrapy.Field()
    tracks = scrapy.Field()
