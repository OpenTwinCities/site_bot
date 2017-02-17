# -*- coding: utf8 -*-


def filter_events(events, updated_since, happening_before):
    """Returns only those events which are publically visible, upcoming, have
    been announced, and have been updated since updated_since or is
    happening before happening_before.
    :param events: List of events to filter
    :param updated_since: Unix timestamp that is the oldest 'updated' value
                          allowed
    :param happening_before: Unix timestamp that is the newest 'time' value
                          allowed
    """
    return [event for event in events
            if event['status'] == 'upcoming' and
            event['visibility'] == 'public' and
            'announce' not in event['self']['actions'] and
            (event['updated'] > updated_since or
             event['time'] < happening_before)]
