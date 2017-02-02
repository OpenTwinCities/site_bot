# -*- coding: utf8 -*-
from __future__ import absolute_import
from datetime import date
from os import path
import shutil
import tempfile
from site_bot_test_helper import SiteBotTestCase
from File.Writer import FileWriter

###############################################################################
# Content and format are defined and tested in MeetupEvent. These tests ensure
# that content is written in the correct place.
###############################################################################


class FakeEvent:
    def __init__(self):
        self.metadata = {}
        self.frontmatter = {}

    def __str__(self):
        return 'event_text'


class FileWriterTest(SiteBotTestCase):
    def setUp(self):
        super(FileWriterTest, self).setUp()
        self.test_dir = tempfile.mkdtemp()
        self.subject = FileWriter(self.test_dir)

    def tearDown(self):
        super(FileWriterTest, self).tearDown()
        shutil.rmtree(self.test_dir)

    def test_create_filename(self):
        file_date = date(2017, 01, 20)
        file_title = 'A Test'
        self.assertEqual(FileWriter.create_filename(file_date, file_title),
                         '2017-01-20-a-test.md')

    def test_split_filename(self):
        self.assertEqual(
            FileWriter.split_filename('2017-01-30-another-event.md'),
            (date(2017, 01, 30), 'another-event'))

    def test_base_path(self):
        self.assertEqual(self.subject.base_path, self.test_dir)

    def test_write(self):
        event = FakeEvent()
        expected_file = '2017-01-01-the-event.md'
        self.subject.write(event, expected_file)
        written = open(path.join(self.test_dir, expected_file))
        self.assertEqual(written.read(), 'event_text')
        written.close()

    def test_delete(self):
        doomed_file_name = '2017-01-01-doomed.md'
        with open(path.join(self.test_dir, doomed_file_name), 'w') as f:
            f.write('Doomed')

        self.assertTrue(
            path.exists(path.join(self.test_dir, doomed_file_name)))
        self.subject.delete(doomed_file_name)
        self.assertFalse(
            path.exists(path.join(self.test_dir, doomed_file_name)))

    def test_delete_nonexistant_file(self):
        doomed_file_name = '2017-01-01-doomed-ghost.md'
        self.assertFalse(
            path.exists(path.join(self.test_dir, doomed_file_name)))
        try:
            self.subject.delete(doomed_file_name)
        except:
            self.fail('attempting to delete a nonexistant file should not '
                      + 'raise an exception')
