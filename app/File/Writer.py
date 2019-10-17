# -*- coding: utf8 -*-
from datetime import date
from inflection import parameterize
import os


class FileWriter:
    @classmethod
    def create_filename(cls, date, title):
        """
        Constructs a filename based on the provided date and title.
        :param date: Date object to base the filename on
        :param title: String to base the filename on
        :returns: The appropriate filename as a string
        """
        return '%s-%s.md' % (
            date.strftime('%Y-%m-%d'), parameterize(str(title)))

    @classmethod
    def split_filename(cls, filename):
        """
        Returns the date and title components of an event filename. An event
        filename is of the form 'yyyy-mm-dd-a-title.md'.
        :param filename: The filename to split.
        :returns: A tuple of (date, title). date will be a Date object, title
                  will be a dasherized string.
        """
        if filename.endswith('.md'):
            filename = filename[:-3]
        (year, month, day, title) = filename.split('-', 3)
        return (date(int(year), int(month), int(day)), title)

    def __init__(self, base_path):
        self.__base_path__ = base_path

    def __get_file_handle__(self, filepath):
        return open(filepath, 'w')

    @property
    def base_path(self):
        return self.__base_path__

    def write(self, event, filename):
        filepath = os.path.join(self.base_path, filename)
        with self.__get_file_handle__(filepath) as f:
            f.write(str(event))

    def delete(self, filename):
        filepath = os.path.join(self.base_path, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
