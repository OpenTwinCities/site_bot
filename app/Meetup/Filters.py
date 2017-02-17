# -*- coding: utf8 -*-


def filter_events(events, happening_before):
    """Returns only those events which are publically visible, upcoming, have
    been announced, and are happening before happening_before.
    :param events: List of events to filter
    :param happening_before: Unix timestamp that is the newest 'time' value
                          allowed
    """
    return [event for event in events
            if event['status'] == 'upcoming' and
            event['visibility'] == 'public' and
            'announce' not in event['self']['actions'] and
            event['time'] < happening_before]
