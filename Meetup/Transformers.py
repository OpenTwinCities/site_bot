# -*- coding: utf8 -*-
from datetime import datetime
import html2text
from ruamel import yaml


def transform_event(event):
    event_time = datetime.fromtimestamp(event['time'])
    location_fields = [
       event['venue'].get('address_1'),
       event['venue'].get('address_2'),
       event['venue'].get('city'),
       event['venue'].get('state')
    ]
    location_fields = [x for x in location_fields if x is not None]
    venue_location = (",".join(location_fields) +
                      " %s" % event['venue'].get('zip')).strip()
    front_matter = {
        'category': 'Events',
        'layout': 'event',
        'title': "%s %s" % (event_time.strftime('%B %d'), event.get('name')),
        'event_date': event_time,
        'meetup_event_id': event.get('id'),
        'venue_name': event['venue'].get('name'),
        'venue_location': venue_location,
        'published': True
    }

    return {
        'front_matter': yaml.dump(front_matter,
                                  Dumper=yaml.RoundTripDumper).strip(),
        'body': html2text.html2text(event['description'])
    }
