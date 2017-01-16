# -*- coding: utf8 -*-
import os
from Git.Client import GitClient
from Meetup.Client import MeetupClient
from Meetup.Filters import filter_events

REPO_RELATIVE_PATH = 'opentwincities.github.com/'
REPO_AUTHOR_NAME = os.environ['SITE_BOT_REPO_AUTHOR_NAME']
REPO_AUTHOR_EMAIL = os.environ['SITE_BOT_REPO_AUTHOR_EMAIL']
REPO_AUTHOR_KEY = os.environ['SITE_BOT_REPO_AUTHOR_KEY']
MEETUP_GROUP_NAME = os.environ['SITE_BOT_MEETUP_GROUP_NAME']
MEETUP_API_KEY = os.environ['SITE_BOT_MEETUP_API_KEY']

meetup = MeetupClient(MEETUP_API_KEY, MEETUP_GROUP_NAME)
git = GitClient(REPO_RELATIVE_PATH, REPO_AUTHOR_NAME, REPO_AUTHOR_EMAIL,
                REPO_AUTHOR_KEY)


def time_to_search_from():
    # TODO Make this read from a file instead of generating a time
    # Returning 1 month ago
    import time
    return int(round((time.time() - 2592000) * 1000))


def poll_and_update():
    events = filter_events(meetup.events, time_to_search_from())

    if events:
        git.pull()

        # TODO Modify repo

        if git.is_dirty():
            git.stage_all()
            git.commit()
            git.push()
