import re
from collections import namedtuple


class TrackCleaner:

    _field_name_regex = re.compile(r'[.()]')  # removes invalid namedtuple field characters
    _field_text_regex = re.compile(r'<.*?>')  # extracts all the text for a track field
    _field_regex = re.compile(r'<td.*?>.*?<\/td>')  # extracts the fields from a track

    _good_title_spans = tuple('feat')  # used to check if span text should be concatenated with a song title
    _bad_text = ('"', '[a]', '[b]', '[c]')  # remove individual text components that should never be concatenated

    def __init__(self, field_string):
        field_string = TrackCleaner._field_name_regex.sub('', field_string)
        self._fields = field_string.split()  # store string of named tuple fields as a list
        self.Track = namedtuple('Track', field_string)  # TODO: this should be more consistent

        # TODO: find a way to make this a class attribute (better for memory)
        self._dispatch_map = {'No': self.clean_no,
                              'Title': self.clean_title,
                              'Writers': self.clean_contributors,
                              'Producers': self.clean_contributors,
                              'Length': self.standard_clean}

    @staticmethod
    def _pre_filter(field):
        """filters out empty strings from a field's list as well as text that should
        never be concatenated"""
        filtered_list = list(filter(None, TrackCleaner._field_text_regex.split(field)))
        return [item.strip() for item in filtered_list if item.strip() not in TrackCleaner._bad_text]

    @staticmethod
    def _join_components(field, separator=''):
        """condenses a list of field components into a character representation of the field"""
        return separator.join(field)

    @staticmethod
    def _format_span(span_components):
        """determines where to append spaces to each span component to ensure proper concatenation."""
        components = list(span_components)  # copy to avoid bugs
        if components[0][-1] != ')':  # if there isn't a closing parentheses, then concatenation must be handled

            # determine at which component to stop concatenating spaces, and perform all string manipulations
            space_stop = len(components) - 2  # TODO: this might not always hold keep an eye out
            for comp_index in range(space_stop):
                components[comp_index] = components[comp_index] + ' '

        return ''.join(components)

    def clean_no(self, field):
        """cleans the track's number by simply removing the period."""
        return self._join_components(self._pre_filter(field)).replace('.', '')

    def clean_title(self, field):
        """cleans the track title by removing quotes and concatenating appropriate <span>'s"""
        title_components = self._pre_filter(field)
        track_title = title_components[0].strip('"')  # remove quotation marks (Wikipedia convention)

        # handle <span> text (song features, extra info etc.)
        if '</span>' in field:
            span_text = TrackCleaner._format_span(title_components[1:])

            # return the song title concatenated with the span text if the span text is relevant
            if any(item for item in self._good_title_spans if item in span_text):
                return track_title + ' ' + span_text
            else:                                     # otherwise simply return the song title
                return track_title
        else:
            return track_title  # return the track title if there is no span text

    def clean_contributors(self, field):
        """Concatenates the names for contributor-related fields (composer/producer etc.)"""
        contributors = self._pre_filter(field)
        return self._join_components(contributors, separator='/')

    def standard_clean(self, field):
        """Cleans any fields that don't need any special treatment (text data is good to go)."""
        return self._join_components(self._pre_filter(field))

    def _dispatch(self, field_name, field_data):
        """Utilizes the descriptor protocol to avoid writing a dispatch map for every instance.

        NOTE: The descriptor protocol is used because the dispatch_map is planned to be implemented as a class
        attribute in the future."""
        return self._dispatch_map[field_name].__get__(self, type(self))(field_data)

    def _run_dispatch_map(self, field_list):
        """Generator that iterates through all of a track's fields and generates the cleansed info."""
        for field_name, field_data in zip(self._fields, field_list):
            try:
                yield self._dispatch(field_name, field_data)
            except KeyError:
                yield field_data  # fields that don't need to be cleaned will cause KeyErrors

    def run_dispatch(self, track_list):
        for track in track_list:
            field_list = TrackCleaner._field_regex.findall(track)
            wtf = list(self._run_dispatch_map(field_list))
            yield self.Track(*wtf)

    # TODO: replace len(list) logic with any!!!!
