import os

import mutagen

from albumscraper.album_scraper import AlbumScraper


class PathTypeError(TypeError):
    """Raised when a string isn't passed for an album directory path."""
    default_message = 'PathTypeError: album path should be string, bytes, os.PathLike or integer'

    def __init__(self):
        super().__init__(PathTypeError.default_message)


# TODO: should use a metaclass for similar custom exceptions
class AlbumNotFoundError(FileNotFoundError):
    """Raised when an album's folder path cannot be found."""
    default_message = 'AlbumNotFoundError: No such album directory: '

    def __init__(self, path):
        message = AlbumNotFoundError.default_message + ' ' + path
        super().__init__(message)


class TrackNotFoundError(FileNotFoundError):
    """Raised when an album's folder path cannot be found."""
    default_message = 'TrackNotFoundError: No such album directory: '

    def __init__(self, path):
        message = TrackNotFoundError.default_message + ' ' + path
        super().__init__(message)


class AlbumTagger:
    """WARNING: For now this is solely designed for FLAC files, but abstraction will be needed to support
    more tagging formats!"""

    # mapping used to find appropriate mutagen tag name from an AlbumScraper's field names
    # TODO: this may need to be updated for other formats (not needed since I only use FLAC)
    tag_map = {
               # album-level tags
               'artist': 'ARTIST',
               'album_artist': 'ALBUMARTIST',
               'album_title': 'ALBUM',
               'year': 'DATE',
               'genres': 'GENRE',

               # track-level tags
               'No': 'TRACKNUMBER',
               'Title': 'TITLE',
               'Writers': 'COMPOSER',
               'Producers': 'PRODUCER',  # this is a custom tag!
               'Length': 'LENGTH'}

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

        except TypeError:
            raise PathTypeError

        except FileNotFoundError:
            raise AlbumNotFoundError(path=path)

    @staticmethod
    def open_track(file_name):
        try:
            return mutagen.File(file_name)

        except TypeError:
            raise PathTypeError

        except FileNotFoundError:
            raise TrackNotFoundError(path=file_name)

    def scrape_album_info(self, album_url):
        """Scrapes and stores the album's wikipedia info."""
        scraper = AlbumScraper(url=album_url)
        scraper.crawl()
        self._album_info = scraper.album

    # TODO: album property to display album info

    @staticmethod
    def _tag_loop(mutagen_file, tag_mapping, save):
        """Tags a mutagen file by iterating over a mapping of tag info (keys are the tags)."""

        # need to handle the case where the mapping happens to be a namedtuple for track information
        try:
            items = tag_mapping.items()
        except AttributeError:
            items = tag_mapping._asdict().items()

        for field, value in items:

            # handles the case where an iterable is stored in an album's field
            if not isinstance(value, str):
                value = value[0]  # TODO: need to find a way for people to select the genre.

            mutagen_tag = AlbumTagger.tag_map[field]  # locate the name of the tag to write to
            AlbumTagger.set_tag(mutagen_file, mutagen_tag, value, save=save)

    @staticmethod
    def set_tag(track, tag, value, save=True):
        """Changes the value of a tag in an audio file and saves the file's tag info."""
        track.tags[tag] = value
        if save:
            track.save()

    @staticmethod
    def set_tags(mutagen_file, tag_data, track_index, save=True):
        # handle album-level data (data is stored in a dictionary/mapping)
        try:
            AlbumTagger._tag_loop(mutagen_file, tag_data, save=save)

        # handle track-level data (data is stored in a list etc.)
        except AttributeError:
            AlbumTagger._tag_loop(mutagen_file, tag_data[track_index], save=save)

    # TODO: decorator to first check if the album info was scraped
    def tag_tracks(self):
        """Iterates through the scraped album info and edits the tags of the album's files in-place."""
        # TODO: probably can use async to make this much more efficient!
        album_info = self._album_info
        album_data = {k: album_info[k] for k in album_info.keys() ^ {'tracks'}}
        track_data = album_info['tracks']

        # TODO: only iterate over files if it is a flac file!!!!!!
        # TODO: WARNING: files in directory must be in the correct order!
        files = sorted(os.listdir(path=self._album_path))
        for index, file in enumerate(files):
            mutagen_file = AlbumTagger.open_track(file_name=file)

            for data_map in (album_data, track_data):
                AlbumTagger.set_tags(mutagen_file, tag_data=data_map,
                                     track_index=index, save=False)  # tag album-level data
            mutagen_file.save()


# TODO: USE UNICODE OBJECTS!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':
    directory = '/home/george/projects/wiki-tag/wikitag/albumtagger/test_album'
    tagger = AlbumTagger(album_path=directory,
                         album_url='https://en.wikipedia.org/wiki/Rodeo_(Travis_Scott_album)')

    tagger.tag_tracks()

    # test scraping
    print('HERE IS ALBUM PRINT\n\n\n\n')
