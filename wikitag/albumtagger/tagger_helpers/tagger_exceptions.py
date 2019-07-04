# TODO: should use a metaclass for similar custom exceptions
class PathTypeError(TypeError):
    """Raised when a string isn't passed for an album directory path."""
    default_message = 'album path should be string, bytes, os.PathLike or integer'

    def __init__(self):
        super().__init__(PathTypeError.default_message)


class AlbumNotFoundError(FileNotFoundError):
    """Raised when an album's folder path cannot be found."""
    default_message = 'No such album directory: '

    def __init__(self, path):
        message = AlbumNotFoundError.default_message + ' ' + path
        super().__init__(message)


class TrackNotFoundError(FileNotFoundError):
    """Raised when an album's folder path cannot be found."""
    default_message = 'No such album directory: '

    def __init__(self, path):
        message = TrackNotFoundError.default_message + ' ' + path
        super().__init__(message)


class AudioTypeError(TypeError):
    """Raised when an unsupported audio format or non-audio file is opened as a track."""
    default_message = 'The file is not a supported audio format'

    def __init__(self):
        super().__init__(AudioTypeError.default_message)
