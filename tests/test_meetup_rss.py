# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.RSS import MeetupRSS
import feedparser
import mock
import requests_mock


class MeetupRSSTest(SiteBotTestCase):
    def setUp(self):
        super(MeetupRSSTest, self).setUp()
        self.subject = MeetupRSS('test_group')

    def test_url(self):
        self.assertEqual(self.subject.rss_url,
                         'https://www.meetup.com/test_group/events/rss')

    @mock.patch.object(MeetupRSS, 'fetch_rss')
    def test_fetch_events(self, mock_fetch_events):
        self.subject.__rss__ = self.fake_rss()
        self.subject.__events__ = self.subject.__rss__.entries
        self.assertEqual(len(self.subject.events), 2)
    
    def fake_rss(self):
        g = open('tests/fake_rss.xml','rb')
        return feedparser.parse(g.read())

