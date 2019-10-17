# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re
import os
import yaml


class FileDB:
    FM_BOUNDARY = re.compile(r'^-{3,}$', re.MULTILINE)

    def __init__(self, base_path):
        self.__base_path__ = base_path
        self.build_index()

    @property
    def base_path(self):
        return self.__base_path__

    def build_index(self):
        self.__index__ = {}
        filenames = [f for f in os.listdir(self.base_path)
                     if os.path.isfile(os.path.join(self.base_path, f))
                     and f.endswith('.md')]
        for filename in filenames:
            filepath = os.path.join(self.base_path, filename)
            with open(filepath, 'r') as f:
                text = f.read()
                _, fm, _ = self.FM_BOUNDARY.split(text, 2)

            metadata = yaml.load(fm, Loader=yaml.FullLoader)
            if 'meetup_event_id' in metadata:
                self.__index__[metadata['meetup_event_id']] = {
                    'title': metadata['title'],
                    'filename': filename
                }

    def find_event(self, meetup_id):
        return self.__index__.get(meetup_id)
