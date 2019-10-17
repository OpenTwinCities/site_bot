# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class MeetupJSON:
    MEETUP_DOMAIN = 'www.meetup.com'

    def __init__(self, group_id):
        self.group_id = group_id
        self.__events__ = None

    @property
    def json_url(self):
        return 'https://%s/%s/events/json' % (self.MEETUP_DOMAIN, self.group_id)

    def fetch_json(self):
        """Requests and returns events from Meetup"""
        return requests.get(self.json_url).json()

    def update_events(self):
        """Fetches events from Meetup and stores them locally. Overwrites any already stored events."""
        self.__events__ = self.fetch_json()

    def parse_event(self, e):
        """Helper function to convert JSON event data to
        expected data for MeetupEvent"""
        event = {}
        event['title'] = e.get('title')

        url = e.get('event_url')
        event['id'] = url.rsplit('/')[-2] if url.endswith('/') else url.rsplit('/', 1)[-1]

        """Date is coming in the following format:
        2019-10-03 00:00:00 EST
        Removing the timezone as it is not useful in this case"""
        time = e.get('local_time')[:-4]
        event['time'] = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        event['excerpt'] = str(BeautifulSoup(e.get('descr'), 'html.parser').p)

        event['venue_name'] = e.get('venue_name')

        location_fields = [
            e.get('venue_address1'),
            e.get('venue_address2'),
            e.get('venue_city'),
            e.get('venue_state')
        ]
        event['venue_location'] = (",".join(filter(None, location_fields)) +
                          " %s" % e.get('venue_zip')).strip()

        return event

    @property
    def events(self):
        """Stored events from Meetup. Events will be fetched if none are stored
        locally."""
        if self.__events__ is None:
            self.update_events()
        return self.__events__
