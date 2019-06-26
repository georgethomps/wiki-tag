from albumscraper.datamanagement.track_cleaner import TrackCleaner


# Return a mapping of all album-related info (album artist, album name, etc.)
def _extract_album_info(response, item):
    """Populates an Album item in-place when parsing album-level data. Making copies of items when parsing data in
    the context of this program is wasteful.

    NOTE: Don't worry about the xpath expressions; pay attention to the keys of the data."""

    # ".fromkeys" uses less code to assign the same value to two keys
    # item.fromkeys(['artist', 'album_artist'], response.xpath('//*[@class="contributor"]//a/text()').get())
    item['artist'] = response.xpath('//*[@class="contributor"]//a/text()').get()
    item['album_artist'] = response.xpath('//*[@class="contributor"]//a/text()').get()

    # Key, Value mappings for all album data (at least the information I generally care for).
    # It's best to use xpaths: they're more powerful and less wasteful (Scrapy converts css selectors to xpath).
    item['album_title'] = response.xpath('//*[@id="firstHeading"]//i/text()').get()
    item['year'] = response.xpath('//*[@class="published"]/text()').get()[-4:]
    item['genres'] = tuple(g.title() for g in response.xpath('//*[@class="category hlist"]//a[@title]/text()').getall())


def _extract_track_info(response, item):
    """Extracts the track information from a Scrapy response and populates an Album's tracks with this information
    in-place."""

    # Xpaths to extract the track metadata (headers) and data (rows)
    col_headers = ' '.join(response.xpath('//*[@class="tracklist"]//*[@scope="col"]//text()').getall())
    track_rows = response.xpath('//*[@class="tracklist"]//tr[@style]').getall()

    # TrackCleaner to facilitate data cleansing
    cleaner = TrackCleaner(field_string=col_headers)
    item['tracks'] = list(cleaner.run_dispatch(track_rows))


# Extract all album and item-related information
# TODO: implement asyncio for efficiency
def extract_info(response, item):
    _extract_album_info(response=response, item=item)
    _extract_track_info(response=response, item=item)
