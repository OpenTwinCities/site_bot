# -*- coding: utf8 -*-
from __future__ import absolute_import
from copy import deepcopy
from datetime import datetime
from site_bot_test_helper import SiteBotTestCase
from Meetup.Event import MeetupEvent


class MeetupEventTest(SiteBotTestCase):

    def expected_frontmatter(self, source_event):
        meetup_event = deepcopy(source_event)

        return {
            'category': 'Events',
            'layout': 'event',
            'title': "%s %s" % (meetup_event['time'].strftime('%B %d'), meetup_event['title']),
            'event_date': "%s" % meetup_event['time'],
            'meetup_event_id': meetup_event['id'],
            'source_meetup_content': True,
            'venue_name': meetup_event['venue_name'],
            'venue_location': meetup_event['venue_location'],
            'published': True,
            'excerpt': meetup_event['excerpt']
        }

    def assertTransformation(self, meetup_event):
        transformed_event = MeetupEvent(meetup_event)
        expected_frontmatter = self.expected_frontmatter(meetup_event)

        self.assertCountEqual(transformed_event.frontmatter,
                              expected_frontmatter)
        self.assertCountEqual(transformed_event.metadata,
                              {k: v for (k, v) in meetup_event.items()
                               if k not in expected_frontmatter})
    def test__str__(self):
        meetup_event = self.fake_event()

        transformed_event = MeetupEvent(meetup_event)
        expected_frontmatter = self.expected_frontmatter(meetup_event)

        expected_text = [
            '---',
            "category: Events",
            "layout: event",
            "title: %s" % expected_frontmatter['title'],
            "event_date: '%s'" % expected_frontmatter['event_date'],
            "meetup_event_id: %s" % expected_frontmatter['meetup_event_id'],
            "source_meetup_content: true",
            "venue_name: %s" % expected_frontmatter['venue_name'],
            "venue_location: %s" % expected_frontmatter['venue_location'],
            "published: true",
            'excerpt: %s' % expected_frontmatter['excerpt'],
            '---',
            '',
        ]

        stringified_event = ("%s" % transformed_event).split("\n")
        print(stringified_event)
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
