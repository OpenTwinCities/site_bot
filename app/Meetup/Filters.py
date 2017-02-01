# -*- coding: utf8 -*-


def filter_events(events, updated_since):
    """Returns only those events which are publically visible, upcoming, have
    been announced, and have been updated since the provided time.
    :param events: List of events to filter
    :param updated_since: Unix timestamp that is the oldest 'updated' value
                          allowed
    """
    return [event for event in events
            if event['status'] == 'upcoming' and
            event['visibility'] == 'public' and
            event['updated'] > updated_since and
            'announce' not in event['self']['actions']]
