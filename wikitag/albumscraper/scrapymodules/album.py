import scrapy.item


# TODO: needs to be aligned with the tag_map implementation!!!!
class Album(scrapy.Item):
    artist = scrapy.Field()
    album_artist = scrapy.Field()  # TODO: this should be removed!
    album_title = scrapy.Field()
    year = scrapy.Field()
    genres = scrapy.Field()  # TODO: make a genre field!
    tracks = scrapy.Field()
