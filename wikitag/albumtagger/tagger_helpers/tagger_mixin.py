import mutagen

from albumtagger.tagger_helpers.tagger_exceptions import *
from albumtagger.tagger_helpers.tag_map import tag_map


class TaggerMixin:
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
            TaggerMixin._tag_loop(mutagen_file, tag_data, save=save)

        # handle track-level data (data is stored in a list etc.)
        except AttributeError:
            TaggerMixin._tag_loop(mutagen_file, tag_data[track_index], save=save)

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

            mutagen_tag = tag_map[field]  # locate the name of the tag to write to
            TaggerMixin.set_tag(mutagen_file, mutagen_tag, value, save=save)

    @staticmethod
    def open_track(file_name):
        try:
            file = mutagen.File(file_name)

        except TypeError as e:
            if not isinstance(e, AudioTypeError):  # Prevents redundant error raise
                return
            raise PathTypeError

        except FileNotFoundError:
            raise TrackNotFoundError(path=file_name)

        # Mutagen does not raise an error if the file isn't an audio file but stores it as None!
        if file is None:
            raise AudioTypeError()
        else:
            return file
