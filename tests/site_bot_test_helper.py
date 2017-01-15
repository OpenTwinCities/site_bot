# -*- coding: utf8 -*-
import time
from faker import Faker
import random
import unittest


class SiteBotTestCase(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()

    def fake_event(self):
        return {
            'created': time.mktime(self.fake.date_time_this_year(True,
                        True).timetuple()),
            'duration': 7200000,
            'id': self.fake.random_number(),
            'name': self.fake.sentence(4),
            'self': {
                    'actions': [
                            'upload_photo',
                            'delete',
                            'edit_hosts',
                            'edit',
                            'comment',
                            'rsvp'
                        ]
                },
            'status': random.choice(['cancelled', 'upcoming', 'past',
                        'proposed', 'suggested', 'draft']),
            'time': time.mktime(self.fake.date_time_this_year(True,
                        True).timetuple()),
            'updated': time.mktime(self.fake.date_time_this_year(True,
                        True).timetuple()),
            'utc_offset': -21600000,
            'venue': {
                    'id': self.fake.random_number(),
                    'name': self.fake.company(),
                    'lat': float(self.fake.latitude()),
                    'lon': float(self.fake.longitude()),
                    'repinned': False,
                    'address_1': self.fake.street_address(),
                    'city': self.fake.city(),
                    'country': 'us',
                    'localized_country_name': 'USA',
                    'zip': self.fake.zipcode(),
                    'state': self.fake.state_abbr()
                },
            'link': self.fake.uri(),
            'description': self.fake.paragraphs(),
            'how_to_find_us': self.fake.sentence(10),
            'visibility': random.choice([True, False])
        }
