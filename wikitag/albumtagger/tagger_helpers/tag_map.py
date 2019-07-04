"""Stores all of target mutagen tag names for certain audio files"""

# TODO: multiple maps for different audio files will need to be implemented
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
