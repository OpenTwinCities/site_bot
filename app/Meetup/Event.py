# -*- coding: utf8 -*-
import yaml


class MeetupEvent:
    def __init__(self, event):
        self.__frontmatter__ = {
            'category': 'Events',
            'layout': 'event',
            'title': "%s %s" % (event['time'].strftime('%B %d'), event['title']),
            'event_date': "%s" % event['time'],
            'meetup_event_id': event['id'],
            'source_meetup_content': True,
            'venue_name': event['venue_name'],
            'venue_location': event['venue_location'],
            'published': True,
            'excerpt': event['excerpt']
        }

        self.__metadata__ = {k: v for (k, v) in event.items()
                             if k not in self.__frontmatter__}

    @property
    def frontmatter(self):
        return self.__frontmatter__

    @property
    def metadata(self):
        return self.__metadata__

    def unicode(self):
        return "\n".join([
            '---',
            yaml.dump(self.frontmatter).strip(),
            '---',
            ''
        ])

    def __str__(self):
        return self.unicode()
