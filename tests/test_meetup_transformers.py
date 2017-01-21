# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Meetup.Transformers import transform_event
from datetime import datetime


class MeetupTransformersTest(SiteBotTestCase):
    def assertTransformation(self, meetup_event):
        meetup_event['description'] = '''
            Hello <a href="http://example.com">World</a>
        '''
        meetup_time = datetime.fromtimestamp(meetup_event['time'])
        meetup_location_fields = [
            meetup_event['venue'].get('address_1'),
            meetup_event['venue'].get('address_2'),
            meetup_event['venue'].get('city'),
            meetup_event['venue'].get('state')
        ]
        meetup_location_fields = [x for x in meetup_location_fields if x is not
                                  None]
        meetup_location = (",".join(meetup_location_fields) +
                           " %s" % meetup_event['venue']['zip'])

        expected_front_matter = [
                "category: Events",
                "layout: event",
                "title: %s %s" % (meetup_time.strftime('%B %d'),
                                  meetup_event['name']),
                "event_date: %s" % meetup_time.strftime('%Y-%m-%d %H:%M:%S'),
                "meetup_event_id: %s" % meetup_event['id'],
                "venue_name: %s" % meetup_event['venue']['name'],
                "venue_location: %s" % meetup_location,
                "published: true"
            ]
        expected_body = "Hello [World](http://example.com)\n\n"
        transformed_event = transform_event(meetup_event)

        self.assertEqual(transformed_event['body'], expected_body)
        self.assertItemsEqual(transformed_event['front_matter'].split('\n'),
                              expected_front_matter)

    def test_transform_event_no_address_2(self):
        self.maxDiff = None
        self.assertTransformation(self.fake_event())

    def test_transform_event_with_address_2(self):
        meetup_event = self.fake_event()
        meetup_event['venue']['address_2'] = self.fake.secondary_address()
        self.assertTransformation(meetup_event)
