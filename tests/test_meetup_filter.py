# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.Filters import filter_events
import time


class MeetupFiltersTest(SiteBotTestCase):

    def test_filter_events(self):
        two_hours_ago = int(round((time.time() - 7200) * 1000))
        one_hour_ago = int(round((time.time() - 3600) * 1000))
        ten_minutes_ago = int(round((time.time() - 600) * 1000))
        ten_minutes_from_now = int(round((time.time() + 600) * 1000))
        one_hour_from_now = int(round((time.time() + 3600) * 1000))
        two_hours_from_now = int(round((time.time() + 7200) * 1000))

        events = [self.fake_event() for x in range(6)]
        events[0]['status'] = 'past'
        events[1]['status'] = 'upcoming'
        events[1]['visibility'] = 'members'
        events[2]['status'] = 'upcoming'
        events[2]['visibility'] = 'public'
        events[2]['updated'] = two_hours_ago
        events[3]['status'] = 'upcoming'
        events[3]['visibility'] = 'public'
        events[3]['updated'] = ten_minutes_ago
        events[3]['self']['actions'] = ['announce', 'upload_photo', 'delete',
                                        'edit_hosts', 'edit', 'comment',
                                        'rsvp']
        events[4]['status'] = 'upcoming'
        events[4]['visibility'] = 'public'
        events[4]['updated'] = ten_minutes_ago
        events[4]['time'] = two_hours_from_now
        events[4]['self']['actions'] = ['upload_photo', 'delete', 'edit_hosts',
                                        'edit', 'comment', 'rsvp']
        events[5]['status'] = 'upcoming'
        events[5]['visibility'] = 'public'
        events[5]['updated'] = ten_minutes_ago
        events[5]['time'] = ten_minutes_from_now
        events[5]['self']['actions'] = ['upload_photo', 'delete', 'edit_hosts',
                                        'edit', 'comment', 'rsvp']

        filtered_events = filter_events(events, one_hour_ago,
                                        one_hour_from_now)
        self.assertEqual(len(filtered_events), 1)
        self.assertEqual(filtered_events[0]['status'], 'upcoming')
        self.assertEqual(filtered_events[0]['visibility'], 'public')
        self.assertFalse('announce' in filtered_events[0]['self']['actions'])
