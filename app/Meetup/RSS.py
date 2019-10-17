# -*- coding: utf8 -*-
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime


class MeetupRSS:
    MEETUP_DOMAIN = 'www.meetup.com'

    def __init__(self, group_id):
        self.group_id = group_id
        self.__rss__ = None
        self.__events__ = None

    @property
    def rss_url(self):
        return 'https://%s/%s/events/rss' % (self.MEETUP_DOMAIN, self.group_id)

    def fetch_rss(self):
        """Use feedparser to get entries from the RSS feed"""
        return feedparser.parse(self.rss_url)

    def update_entries(self):
        """Fetch entries from RSS feed and store them"""
        self.__rss__ = self.fetch_rss()
        self.__events__ = self.__rss__.entries

    def parse_event(self, e):
        """Helper function to convert RSS event data to
        expected data for MeetupEvent"""
        event = {}
        event['title'] = e.title

        event['id'] = e.guid.rsplit('/')[-2] if e.guid.endswith('/') else e.guid.rsplit('/', 1)[-1]

        # published_parsed has the date in struct_time
        # Convert to datetime for better output
        event['time'] = datetime.fromtimestamp(mktime(e.published_parsed))

        # Find a better way to parse this specific element
        html = BeautifulSoup(e.summary, 'html.parser')
        event['excerpt'] = None
        for tag in html.find_all('p'):
            for p in tag.find_all('p'):
                event['excerpt'] = str(p)
                break

        event['venue_name'] = None
        event['venue_location'] = None

        return event

    @property
    def events(self):
        """Stored entries from the RSS feed"""
        if self.__events__ is None:
            self.update_entries()
        return self.__events__
