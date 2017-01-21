# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.Writer import MeetupWriter
from datetime import datetime
from os import path
import shutil
import tempfile

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


class MeetupWriterTest(SiteBotTestCase):
    def setUp(self):
        super(MeetupWriterTest, self).setUp()
        self.test_dir = tempfile.mkdtemp()
        self.subject = MeetupWriter(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_base_path(self):
        self.assertEqual(self.subject.base_path, self.test_dir)

    def test_write(self):
        event = FakeEvent()
        event.frontmatter['event_date'] = datetime.now()
        event.frontmatter['meetup_event_id'] = '1a2b'
        expected_file = ("%s-%s.md" %
                         (event.frontmatter['event_date'].strftime('%Y-%m-%d'),
                          event.frontmatter['meetup_event_id']))
        self.subject.write(event)
        written = open(path.join(self.test_dir, expected_file))
        self.assertEqual(written.read(), 'event_text')
        written.close()
