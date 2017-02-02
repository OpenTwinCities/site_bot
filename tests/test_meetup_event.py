# -*- coding: utf8 -*-
from __future__ import absolute_import
from copy import deepcopy
from datetime import datetime
from site_bot_test_helper import SiteBotTestCase
from Meetup.Event import MeetupEvent


class MeetupEventTest(SiteBotTestCase):

    def expected_frontmatter(self, source_event):
        meetup_event = deepcopy(source_event)
        for field in ['time', 'created', 'updated']:
            meetup_event[field] = datetime.fromtimestamp(
                meetup_event[field] / 1000)

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

        return {
            'category': 'Events',
            'layout': 'event',
            'title': "%s %s" % (meetup_event['time'].strftime('%B %d'),
                                meetup_event['name']),
            'event_date': meetup_event['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'meetup_event_id': meetup_event['id'],
            'source_meetup_content': True,
            'venue_name': meetup_event['venue']['name'],
            'venue_location': meetup_location,
            'published': True,
            'excerpt': '<p>Hello <a href="http://example.com">World</a></p>'
        }

    def assertTransformation(self, meetup_event):
        transformed_event = MeetupEvent(meetup_event)
        expected_frontmatter = self.expected_frontmatter(meetup_event)

        self.assertItemsEqual(transformed_event.frontmatter,
                              expected_frontmatter)
        self.assertItemsEqual(transformed_event.metadata,
                              {k: v for (k, v) in meetup_event.iteritems()
                               if k not in expected_frontmatter})

    def test_init_no_address_2(self):
        self.assertTransformation(self.fake_event())

    def test_init_with_address_2(self):
        meetup_event = self.fake_event()
        meetup_event['venue']['address_2'] = self.fake.secondary_address()
        self.assertTransformation(meetup_event)

    def test__str__(self):
        meetup_event = self.fake_event()

        transformed_event = MeetupEvent(meetup_event)
        expected_frontmatter = self.expected_frontmatter(meetup_event)
        expected_text = [
            '---',
            "category: %s" % expected_frontmatter['category'],
            "layout: %s" % expected_frontmatter['layout'],
            "title: %s" % expected_frontmatter['title'],
            "event_date: %s" % expected_frontmatter['event_date'],
            "meetup_event_id: %s" % expected_frontmatter['meetup_event_id'],
            "source_meetup_content: true",
            "venue_name: %s" % expected_frontmatter['venue_name'],
            "venue_location: %s" % expected_frontmatter['venue_location'],
            "published: true",
            'excerpt: <p>Hello <a href="http://example.com">World</a></p>',
            '---',
            '',
        ]

        stringified_event = ("%s" % transformed_event).split("\n")
        print stringified_event
        self.assertEqual(stringified_event[0], expected_text[0])
        # Frontmatter ordering is not guarrenteeded, and doesn't need to be
        for x in range(1, 11):
            locations = [i for i, line in enumerate(stringified_event)
                         if line == expected_text[x]]
            self.assertEqual(len(locations), 1,
                             'Found the wrong number of %s' % expected_text[x])
            self.assertGreaterEqual(locations[0], 1)
            self.assertLess(locations[0], 11)

        for x in range(11, 13):
            self.assertEqual(stringified_event[x], expected_text[x])
