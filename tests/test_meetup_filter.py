# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.Filter import filter_event
from datetime import datetime, timedelta


class MeetupFiltersTest(SiteBotTestCase):

    def test_filter_event(self):
        ten_minutes_from_now = datetime.now() + timedelta(minutes=10)
        one_hour_from_now = datetime.now() + timedelta(hours=1)
        two_hours_from_now = datetime.now() + timedelta(hours=2)

        events = [self.fake_event_parsed() for x in range(5)]
        events[0]['status'] = 'past'
        events[1]['status'] = 'upcoming'
        events[1]['visibility'] = 'members'
        events[2]['status'] = 'upcoming'
        events[2]['visibility'] = 'public'
        events[2]['time'] = two_hours_from_now
        events[3]['status'] = 'upcoming'
        events[3]['visibility'] = 'public'
        events[3]['time'] = ten_minutes_from_now
        events[3]['self'] = {}
        events[3]['self']['actions'] = ['announce', 'upload_photo', 'delete',
                                        'edit_hosts', 'edit', 'comment',
                                        'rsvp']
        events[4]['status'] = 'upcoming'
        events[4]['visibility'] = 'public'
        events[4]['time'] = ten_minutes_from_now
        events[4]['self'] = {}
        events[4]['self']['actions'] = ['upload_photo', 'delete', 'edit_hosts',
                                        'edit', 'comment', 'rsvp']

        filtered_events = []
        for event in events:
            if (filter_event(event, one_hour_from_now)):
                filtered_events.append(event)

        self.assertEqual(len(filtered_events), 1)
        self.assertEqual(filtered_events[0]['status'], 'upcoming')
        self.assertEqual(filtered_events[0]['visibility'], 'public')
        self.assertFalse('announce' in filtered_events[0]['self']['actions'])

