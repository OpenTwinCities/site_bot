# -*- coding: utf8 -*-
from MeetupClient import MeetupClient
import requests_mock
from site_bot_test_helper import SiteBotTestCase

events_count = 0


class MeetupClientTest(SiteBotTestCase):
    def setUp(self):
        super(MeetupClientTest, self).setUp()
        self.subject = MeetupClient('1234', 'test_group')

    def test_events_url(self):
        self.assertEqual(self.subject.events_url,
                         'https://api.meetup.com/test_group/events')

    @requests_mock.Mocker()
    def test_events_pagination_completion(self, m):
        fake_events = [self.fake_event() for x in range(50)]

        def events_callback(request, context):
            global events_count
            events_count += 1
            if 25 * events_count <= len(fake_events):
                context.headers['Link'] = '<%s>;rel="next"' % request.url
            context.status_code = 200
            return fake_events[25*(events_count-1):25*events_count]

        m.get(self.subject.events_url, json=events_callback)
        self.assertEqual(self.subject.events, fake_events)
