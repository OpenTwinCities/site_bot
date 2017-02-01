# -*- coding: utf8 -*-
from copy import deepcopy
from datetime import datetime
from ruamel import yaml


class MeetupEvent:

    def __init__(self, source_event):
        event = deepcopy(source_event)
        # All times from Meetup are in milliseconds
        for field in ['time', 'created', 'updated']:
            event[field] = datetime.fromtimestamp(event[field] / 1000)

        location_fields = [
            event['venue'].get('address_1'),
            event['venue'].get('address_2'),
            event['venue'].get('city'),
            event['venue'].get('state')
        ]
        location_fields = [x for x in location_fields if x is not None]
        venue_location = (",".join(location_fields) +
                          " %s" % event['venue'].get('zip')).strip()
        self.__frontmatter__ = {
            'category': 'Events',
            'layout': 'event',
            'title': "%s %s" % (event['time'].strftime('%B %d'),
                                event.get('name')),
            'event_date': event['time'],
            'meetup_event_id': event.get('id'),
            'source_meetup_content': True,
            'venue_name': event['venue'].get('name'),
            'venue_location': venue_location,
            'published': True
        }
        self.__metadata__ = {k: v for (k, v) in event.iteritems()
                             if k not in self.__frontmatter__}

    @property
    def frontmatter(self):
        return self.__frontmatter__

    @property
    def metadata(self):
        return self.__metadata__

    def __unicode__(self):
        return "\n".join([
            '---',
            yaml.dump(self.frontmatter, Dumper=yaml.RoundTripDumper).strip(),
            '---',
            ''
        ])

    def __str__(self):
        return unicode(self).encode('utf-8')
