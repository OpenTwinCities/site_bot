# -*- coding: utf8 -*-
from __future__ import absolute_import
import datetime
import mock
import os
import tempfile
from site_bot_test_helper import SiteBotTestCase
from File.Writer import FileWriter
from Meetup.Event import MeetupEvent
from app import App


class AppTest(SiteBotTestCase):
    def setUp(self):
        super(AppTest, self).setUp()
        self.test_dir = tempfile.mkdtemp()
        self.test_posts_dir = os.path.join(self.test_dir, 'posts')
        os.makedirs(self.test_posts_dir)
        self.subject = App({
            'REPO_PATH': self.test_dir,
            'REPO_AUTHOR_NAME': 'Tester',
            'REPO_AUTHOR_EMAIL': 'tester@example.com',
            'MEETUP_GROUP_NAME': 'TestGroup',
            'MEETUP_API_KEY': '123',
            'EVENT_POSTS_DIR': self.test_posts_dir,
            'ENVIRONMENT': 'test'
        })

    def test_sync_event_file_excerpt_update(self):
        # Build an event and establish that it has already been observed and
        # written
        event = self.fake_event()
        mock_created = datetime.date.today() - datetime.timedelta(days=7)
        mock_filename = FileWriter.create_filename(mock_created,
                                                   event['name'])
        mock_file_info = {
            'title': event['name'],
            'filename': mock_filename
        }
        prep_writer = FileWriter(self.test_posts_dir)
        prep_writer.write(MeetupEvent(event), mock_filename)

        # Modify event content that will become excerpt
        event['description'] = "<p>This is new</p>" + event['description']
        expected_transformed_event = MeetupEvent(event)

        # Verify that
        # 1. writer.write is going to write content that includes the updated
        #    excerpt
        # 2. writer.write is going to write to the already existing file
        with mock.patch.object(self.subject.writer, 'write') as mock_write,\
            mock.patch.object(self.subject.db, 'find_event') as\
                mock_find_event:
            mock_find_event.return_value = mock_file_info
            self.subject.sync_event_file(event)
            self.assertEqual(str(mock_write.call_args[0][0]),
                             str(expected_transformed_event))
            self.assertEqual(mock_write.call_args[0][1], mock_filename)

    def test_sync_event_file_changed_name(self):
        # Build an event and establish that it has already been observed and
        # written
        event = self.fake_event()
        mock_created = datetime.date.today() - datetime.timedelta(days=7)
        mock_old_filename = FileWriter.create_filename(mock_created,
                                                       event['name'])
        mock_file_info = {
            'title': event['name'],
            'filename': mock_old_filename
        }
        prep_writer = FileWriter(self.test_posts_dir)
        prep_writer.write(MeetupEvent(event), mock_old_filename)

        # Modify event name
        event['name'] = 'A new name'
        expected_transformed_event = MeetupEvent(event)
        mock_new_filename = FileWriter.create_filename(mock_created,
                                                       event['name'])

        # Verify that
        # 1. writer.delete is called to delete to old file
        # 2. writer.write is going to write content that includes the updated
        #    name
        # 3. writer.write is going to write to a new file using the new name
        with mock.patch.object(self.subject.writer, 'write') as mock_write,\
            mock.patch.object(self.subject.writer, 'delete') as mock_delete,\
            mock.patch.object(self.subject.db, 'find_event') as\
                mock_find_event:
            mock_find_event.return_value = mock_file_info
            self.subject.sync_event_file(event)
            mock_delete.assert_called_with(mock_old_filename)
            self.assertEqual(str(mock_write.call_args[0][0]),
                             str(expected_transformed_event))
            self.assertEqual(mock_write.call_args[0][1], mock_new_filename)
