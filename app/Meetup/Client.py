# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import copy
import requests


class MeetupClient:
    MEETUP_API_DOMAIN = 'api.meetup.com'

    def __init__(self, group_id):
        self.group_id = group_id
        self.__base_query_params__ = {}
        self.__events__ = None

    def query_params(self, additional_params={}):
        params = copy.deepcopy(self.__base_query_params__)
        params.update(additional_params)
        return params

    @property
    def events_url(self):
        return 'https://%s/%s/events' % (self.MEETUP_API_DOMAIN, self.group_id)

    def fetch_events(self):
        """Requests and returns events from Meetup"""
        return requests.get(self.events_url, params=self.query_params({
            'fields': ['self', 'venue.state'],
            'omit': ['waitlist_count', 'yes_rsvp_count', 'group', 'manual_attendance_count', 'self.role', 'self.rsvp']
            })).json()

    def update_events(self):
        """Fetches events from Meetup and stores them locally. Overwrites any
        already stored events."""
        self.__events__ = self.fetch_events()

    def parse_event(self, e):
        event = copy.deepcopy(e)
        # Copied from previous version of Meetup/Event.py
        # All times from Meetup are in milliseconds
        for field in ['time', 'created', 'updated']:
            event[field] = datetime.utcfromtimestamp(
                (event[field] + event['utc_offset']) / 1000)

        location_fields = [
            event['venue'].get('address_1'),
            event['venue'].get('address_2'),
            event['venue'].get('city'),
            event['venue'].get('state')
        ]
        location_fields = [x for x in location_fields if x is not None]
        event['venue_location'] = (",".join(location_fields) +
                          " %s" % event['venue'].get('zip')).strip()
        event['excerpt'] = str(BeautifulSoup(event['description'], 'html.parser').p)

        event['title'] = "%s %s" % (event['time'].strftime('%B %d'), event.get('name'))
        event['event_date'] = event['time']
        event['meetup_event_id'] = event.get('id')
        event['venue_name'] = event['venue'].get('name')

        return event

    @property
    def events(self):
        """Stored events from Meetup. Events will be fetched if none are stored
        locally."""
        if self.__events__ is None:
            self.update_events()
        return self.__events__

