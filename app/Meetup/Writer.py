# -*- coding: utf8 -*-
from os import path


class MeetupWriter:
    def __init__(self, base_path):
        self.__base_path__ = base_path

    def __get_file_handle__(self, filepath):
        return open(filepath, 'w')

    @property
    def base_path(self):
        return self.__base_path__

    def write(self, event):
        event_date = event.frontmatter['event_date']
        filename = "%s-%s.md" % (event_date.strftime('%Y-%m-%d'),
                                 event.frontmatter['meetup_event_id'])
        filepath = path.join(self.base_path, filename)
        with self.__get_file_handle__(filepath) as f:
            f.write(str(event))
