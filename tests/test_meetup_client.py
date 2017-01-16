# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.Client import MeetupClient
import mock
import requests_mock

events_count = 0


class MeetupClientTest(SiteBotTestCase):
    def setUp(self):
        super(MeetupClientTest, self).setUp()
        self.subject = MeetupClient('1234', 'test_group')

    def test_events_url(self):
        self.assertEqual(self.subject.events_url,
                         'https://api.meetup.com/test_group/events')

    @requests_mock.Mocker()
    def test_fetch_events_with_next(self, m):
        # Meetup event series go on forever; we only care about what's in the
        # near future. Only one request to the event endpoint should occur.
        fake_events = [self.fake_event() for x in range(50)]

        def events_callback(request, context):
            # Mock pagination of the events, with Link header
            global events_count
            events_count += 1
            if 25 * events_count <= len(fake_events):
                context.headers['Link'] = '<%s>;rel="next"' % request.url
            context.status_code = 200
            return fake_events[25*(events_count-1):25*events_count]

        m.get(self.subject.events_url, json=events_callback)

        events = self.subject.fetch_events()
        self.assertEqual(len(m.request_history), 1)
        self.assertEqual(events, fake_events[:25])

    @requests_mock.Mocker()
    def test_fetch_events_param_setting(self, m):
        m.get(self.subject.events_url, json=[])
        self.subject.fetch_events()
        print m.request_history[0].query
        params = m.request_history[0].qs
        self.assertTrue('key' in params)
        self.assertEqual(params['key'][0], '1234')
        self.assertTrue('fields' in params)
        self.assertTrue('self' in params['fields'])
        self.assertTrue('omit' in params)
        self.assertItemsEqual(
            params['omit'],
            ['waitlist_count', 'yes_rsvp_count', 'group',
             'manual_attendance_count', 'self.role', 'self.rsvp'])

    @mock.patch.object(MeetupClient, 'fetch_events')
    def test_events_caching(self, mock_fetch_events):
        mock_fetch_events.return_value = [1]
        self.assertEqual(self.subject.events, [1])
        self.assertEqual(self.subject.events, [1])
        mock_fetch_events.assert_called_once()

    @mock.patch.object(MeetupClient, 'fetch_events')
    def test_update_events(self, mock_fetch_events):
        mock_fetch_events.return_value = [1]
        self.assertEqual(self.subject.events, [1])
        mock_fetch_events.return_value = [2, 3]
        self.subject.update_events()
        self.assertEqual(self.subject.events, [2, 3])
