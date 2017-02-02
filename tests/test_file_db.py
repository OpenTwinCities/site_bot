# -*- coding: utf8 -*-
from __future__ import absolute_import
import os
import shutil
import tempfile
from site_bot_test_helper import SiteBotTestCase
from File.DB import FileDB


class FileDBTest(SiteBotTestCase):
    def setUp(self):
        super(FileDBTest, self).setUp()
        self.test_dir = tempfile.mkdtemp()
        self.test_yaml = {}
        for i in range(10):
            self.test_yaml[i] = """---
title: Some Event
meetup_event_id: %s
foo: bar
---
""" % i

        self.test_yaml[10] = """---
title: Not on Meetup
foo: bar
---
"""

        for key in self.test_yaml:
            file_name = os.path.join(self.test_dir, "%s.md" % key)
            with open(file_name, 'w') as f:
                f.write(self.test_yaml[key])

        self.subject = FileDB(self.test_dir)

    def tearDown(self):
        super(FileDBTest, self).tearDown()
        shutil.rmtree(self.test_dir)

    def test_base_path(self):
        self.assertEqual(self.subject.base_path, self.test_dir)

    def test_find_event(self):
        for i in range(10):
            self.assertItemsEqual(self.subject.find_event(i),
                                  {'title': 'Some Event',
                                   'filename': '%s.md' % i})

    def test_find_event_nonexistant_id(self):
        self.assertIsNone(self.subject.find_event(1000000000))

    def test_index_only_meetup_files(self):
        self.assertEqual(len(self.subject.__index__), 10)
        for key in self.subject.__index__:
            self.assertFalse(
                self.subject.__index__[key]['filename'] == '10.md')
