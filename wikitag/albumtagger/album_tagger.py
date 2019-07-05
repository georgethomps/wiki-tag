import os
from collections import namedtuple
from itertools import repeat

from albumscraper.album_scraper import AlbumScraper
from albumtagger.tagger_helpers.tagger_mixin import *


# TODO: USE UNICODE OBJECTS!!!!!!!!!!!!!!!!!!!!!
class AlbumTagger(TaggerMixin):
    """WARNING: For now this is solely designed for FLAC files, but more audio formats will be implemented through
    the tag_map module in the tagger_helpers package.

    WARNING: It's also important to note that an AlbumTagger can only scrape album data once!

    WARNING: Files in the directory must be sorted in the correct track order!"""

    album = namedtuple('Album', ['path', 'url', 'data_map'])  # helps organize the albums' data

    def __init__(self, album_paths=None, album_urls=None):
        # Require users to provide an album path and album url when adding an album
        if not album_paths and not album_urls:
            self.albums = None

        # handle strings
        elif isinstance(album_paths, str) and isinstance(album_urls, str):
            # TODO: what is this syntax?!
            self.albums = []
            self.albums.append(AlbumTagger.album(path=album_paths, url=album_urls, data_map='No Scraped Info'))
            self.scrape_albums()

        # handle sequences
        elif len(album_paths) == len(album_urls):
            self.albums = list(AlbumTagger.album(*items) for items in
                               zip(album_paths, album_urls, repeat('No Scraped Info', len(album_paths))))
            self.scrape_albums()

        # unequal number of album paths and album urls
        else:
            raise AlbumDataError

    @property
    def _album_paths(self):
        return [album_path for album_path, album_url, album_map in self.albums]

    @property
    def _album_urls(self):
        return [album_url for album_path, album_url, album_map in self.albums]

    def add_album(self, album_path, album_url):
        try:
            self.albums.append(AlbumTagger.album(path=album_path, url=album_url, data_map='No Scraped Info'))
        except TypeError:
            raise AlbumDataError

    @staticmethod
    def open_album(album_path):
        """Sets the AlbumTagger's album path to a provided path and sets the path as the working directory."""
        # TODO: issue with relative paths!
        try:
            os.chdir(path=album_path)

        except TypeError:
            raise PathTypeError

        except FileNotFoundError:
            raise AlbumNotFoundError(path=album_path)

    # TODO: processing to check if data was scraped
    def scrape_albums(self):
        """Scrapes and stores the album's Wikipedia info."""
        urls = self._album_urls
        # TODO: handle bad links!!!!!!!!
        scraper = AlbumScraper(urls=urls)
        scraper.crawl()
        self._update_album_info(scraper.albums)

    def _update_album_info(self, info_maps):
        """Recreate the albums attribute after scraping the albums' data (info map)"""
        for index, album in enumerate(self.albums):
            map_ = info_maps[index]
            self.albums[index] = AlbumTagger.album(path=album.path, url=album.url, data_map=map_)

    # TODO: albums property to display album info

    def tag_albums(self, print_untagged=True):
        for album in self.albums:
            AlbumTagger.tag_album(album_path=album.path, album_map=album.data_map, print_untagged=print_untagged)

    @staticmethod
    def tag_album(album_path, album_map, print_untagged=True):
        """Iterates through a dictionary of an album's scraped info and edits the tags of the album's files in-place."""
        # TODO: probably can use async to make this much more efficient!

        untagged = []  # save untagged files to report to the user
        # TODO: create a named tuple to provide reasons for why files/folders weren't tagged

        AlbumTagger.open_album(album_path=album_path)

        album_data = {k: album_map[k] for k in album_map.keys() ^ {'tracks'}}
        track_data = album_map['tracks']

        files = sorted(os.listdir(path=album_path))
        for index, file in enumerate(files):
            try:
                mutagen_file = AlbumTagger.open_track(file_name=file)

                for data_map in (album_data, track_data):
                    AlbumTagger.set_tags(mutagen_file, tag_data=data_map,
                                         track_index=index, save=False)  # tag album-level data
                mutagen_file.save()

            except IndexError:  # track is not a part of the scraped track list
                untagged.append(file)

            except AudioTypeError:
                untagged.append(file)
                continue

            except mutagen.MutagenError:  # Handles directory errors TODO: way to make this more specific?
                # TODO: recursively go through folder files
                untagged.append(file + ' (Is a Directory!)')  # TODO: remove this text when reasons are implemented
                continue

        if print_untagged:
            print('WARNING: The following files/folders could not be tagged:\n')
            print(*untagged, sep='\n')
            print()


if __name__ == '__main__':
    directory = '/home/george/projects/wiki-tag/wikitag/albumtagger/test_album'
    dir2 = '/home/george/projects/wiki-tag/wikitag/albumtagger/test2'
    tagger = AlbumTagger(album_paths=[directory, dir2],
                         album_urls=['https://en.wikipedia.org/wiki/Rodeo_(Travis_Scott_album)',
                                     'https://en.wikipedia.org/wiki/Rap_or_Go_to_the_League'])

    tagger.tag_albums()

    # test scraping
    print('HERE IS ALBUM PRINT\n\n\n\n')
