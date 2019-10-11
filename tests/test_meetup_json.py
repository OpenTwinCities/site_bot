# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.JSON import MeetupJSON
import mock
import requests_mock


class MeetupJSONTest(SiteBotTestCase):
    def setUp(self):
        super(MeetupJSONTest, self).setUp()
        self.subject = MeetupJSON('test_group')

    def test_url(self):
        self.assertEqual(self.subject.json_url,
                         'https://www.meetup.com/test_group/events/json')

    @mock.patch.object(MeetupJSON, 'fetch_json')
    def test_events_caching(self, mock_fetch_events):
        mock_fetch_events.return_value = [1]
        self.assertEqual(self.subject.events, [1])
        self.assertEqual(self.subject.events, [1])
        mock_fetch_events.assert_called_once()

    @mock.patch.object(MeetupJSON, 'fetch_json')
    def test_update_events(self, mock_fetch_events):
        mock_fetch_events.return_value = [1]
        self.assertEqual(self.subject.events, [1])
        mock_fetch_events.return_value = [2, 3]
        self.subject.update_events()
        self.assertEqual(self.subject.events, [2, 3])
