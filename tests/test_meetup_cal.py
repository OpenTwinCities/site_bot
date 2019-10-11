# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.Calendar import MeetupCalendar
from icalendar import Calendar
import mock
import requests_mock
import os


class MeetupCalendarTest(SiteBotTestCase):
    def setUp(self):
        super(MeetupCalendarTest, self).setUp()
        self.subject = MeetupCalendar('test_group')

    def test_url(self):
        self.assertEqual(self.subject.ical_url,
                         'https://www.meetup.com/test_group/events/ical')

    @mock.patch.object(MeetupCalendar, 'fetch_calendar')
    def test_fetch_events(self, mock_fetch_events):
        self.subject.__cal__ = self.fake_calendar()
        self.assertEqual(len(self.subject.events), 2)

    def fake_calendar(self):
        g = open('tests/fake_calendar.ics','rb')
        return Calendar.from_ical(g.read())

