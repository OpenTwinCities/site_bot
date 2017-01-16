# -*- coding: utf8 -*-
import html2text
import yaml


def transform_event(event):
    front_matter = {
        'category': 'Events',
        'layout': 'event',
        'title': event.get('name', 'Event')
    }
    transformed_event = {'front_matter': yaml.dump(front_matter)}
    print transformed_event['front_matter']
    transformed_event['body'] = html2text.html2text(event['description'])
    return transformed_event
