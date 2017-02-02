# -*- coding: utf8 -*-
import copy
import requests


class MeetupClient:
    MEETUP_API_DOMAIN = 'api.meetup.com'

    def __init__(self, key, group_id):
        self.key = key
        self.group_id = group_id
        self.__base_query_params__ = {'key': self.key}
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
            'omit': ['waitlist_count', 'yes_rsvp_count', 'group',
                     'manual_attendance_count', 'self.role', 'self.rsvp']
            })).json()

    def update_events(self):
        """Fetches events from Meetup and stores them locally. Overwrites any
        already stored events."""
        self.__events__ = self.fetch_events()

    @property
    def events(self):
        """Stored events from Meetup. Events will be fetched if none are stored
        locally."""
        if self.__events__ is None:
            self.update_events()
        return self.__events__
