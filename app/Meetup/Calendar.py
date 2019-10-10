# -*- coding: utf8 -*-
import requests
from icalendar import Calendar


class MeetupCalendar:
    MEETUP_DOMAIN = 'www.meetup.com'

    def __init__(self, group_id):
        self.group_id = group_id
        self.__raw_cal__ = None
        self.__cal__ = None
        self.__events__ = None

    @property
    def ical_url(self):
        return 'https://%s/%s/events/ical' % (self.MEETUP_DOMAIN, self.group_id)

    def fetch_calendar(self):
        """Requests and returns calendar from Meetup"""
        return requests.get(self.ical_url).text

    def update_calendar(self):
        """Fetches calendar from Meetup and stores it locally."""
        self.__raw_cal__ = self.fetch_calendar()
        self.__cal__ = Calendar.from_ical(self.__raw_cal__)

    def parse_event(self, e):
        """Helper function to convert Calendar event data to
        expected data for MeetupEvent"""
        event = {}
        event['title'] = e.get('summary')

        url = e.get('url')
        event['id'] = url.rsplit('/')[-2] if url.endswith('/') else url.rsplit('/', 1)[-1]

        event['time'] = e.get('dtstamp').dt
        event['excerpt'] = e.get('description').replace('\n\n', '. ').replace('\n', '. ')

        event['venue_name'] = None
        event['venue_location'] = None

        return event

    @property
    def events(self):
        if self.__cal__ is None:
            self.update_calendar()

        if self.__events__ is None:
            self.__events__ = []
            for event in self.__cal__.walk():
                if event.name == 'VEVENT':
                    self.__events__.append(event)
                    
        return self.__events__
