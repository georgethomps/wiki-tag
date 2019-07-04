import os

from albumscraper.album_scraper import AlbumScraper
from albumtagger.tagger_helpers.tagger_mixin import *


class AlbumTagger(TaggerMixin):
    """WARNING: For now this is solely designed for FLAC files, but more audio formats will be implemented through
    the tag_map module in the tagger_helpers package."""

    def __init__(self, album_path=None, album_url=None):
        # handle the tagger's album path
        if album_path:
            self.open_album(path=album_path)
        else:
            self._album_path = None

        # handle scraping the album's info from the web
        if album_url:
            self.scrape_album_info(album_url=album_url)
        else:
            self._album_info = None

    def open_album(self, path):
        """Sets the AlbumTagger's album path to a provided path and sets the path as the working directory."""
        try:
            self._album_path = path
            os.chdir(path=path)

        except TypeError as e:
            raise PathTypeError

        except FileNotFoundError:
            raise AlbumNotFoundError(path=path)

    def scrape_album_info(self, album_url):
        """Scrapes and stores the album's wikipedia info."""
        scraper = AlbumScraper(url=album_url)
        scraper.crawl()
        self._album_info = scraper.album

    # TODO: album property to display album info

    # TODO: decorator check if the album info was scraped
    def tag_tracks(self, print_untagged=True):
        """Iterates through the scraped album info and edits the tags of the album's files in-place."""
        # TODO: probably can use async to make this much more efficient!

        untagged = []  # save untagged files to report to the user
        # TODO: create a named tuple to provide reasons for why files/folders weren't tagged

        album_info = self._album_info
        album_data = {k: album_info[k] for k in album_info.keys() ^ {'tracks'}}
        track_data = album_info['tracks']

        # TODO: only iterate over files if it is a flac file!!!!!!  duck typing
        # TODO: WARNING: files in directory must be in the correct order!
        files = sorted(os.listdir(path=self._album_path))
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


# TODO: USE UNICODE OBJECTS!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':
    directory = '/home/george/projects/wiki-tag/wikitag/albumtagger/test_album'
    tagger = AlbumTagger(album_path=directory,
                         album_url='https://en.wikipedia.org/wiki/Rodeo_(Travis_Scott_album)')

    tagger.tag_tracks()

    # test scraping
    print('HERE IS ALBUM PRINT\n\n\n\n')
