# -*- coding: utf8 -*-
from datetime import date
import os
import sys
import time
sys.path.insert(1, 'app/')
from Git.Client import GitClient
from Meetup.Calendar import MeetupCalendar
from Meetup.JSON import MeetupJSON
from Meetup.RSS import MeetupRSS
from Meetup.Event import MeetupEvent
from File.DB import FileDB
from File.Writer import FileWriter


class App:
    def __init__(self, CONSTANTS):
        for name in CONSTANTS:
            setattr(self, name, CONSTANTS[name])
        self.meetup = MeetupRSS(self.MEETUP_GROUP_NAME)
        self.git = GitClient(self.REPO_PATH, self.REPO_AUTHOR_NAME,
                             self.REPO_AUTHOR_EMAIL)
        self.writer = FileWriter(self.EVENT_POSTS_DIR)
        self.db = FileDB(self.EVENT_POSTS_DIR)

    def sync_event_file(self, event):
        renamed = False

        file_info = self.db.find_event(event['id'])
        if file_info:
            if file_info['title'] != event['title']:
                renamed = True
                (file_date, title) = FileWriter.split_filename(
                    file_info['filename'])
                filename = FileWriter.create_filename(file_date, event['title'])
            else:
                filename = file_info['filename']
        else:
            filename = FileWriter.create_filename(event['time'], event['title'])

        if renamed:
            self.writer.delete(file_info['filename'])

        self.writer.write(MeetupEvent(event), filename)

    def sync_git(self):
        if self.git.status:
            self.git.stage_all()
            self.git.commit()
            try:
                self.git.push()
                return True
            except Exception as e:
                self.git.remove_head_commit()
                self.git.pull()
                raise e
        else:
            return False

    def poll_and_update(self):
        events = self.meetup.events

        if events:
            self.git.reset_hard()
            self.git.pull()

            for event in events:
                event = self.meetup.parse_event(event)
                self.sync_event_file(event)

            self.sync_git()


def CONSTANTS():
    CONSTANTS = {
        'REPO_PATH': os.path.join(os.getcwd(), 'opentwincities.github.com/'),
        'REPO_AUTHOR_NAME': os.environ['SITE_BOT_REPO_AUTHOR_NAME'],
        'REPO_AUTHOR_EMAIL': os.environ['SITE_BOT_REPO_AUTHOR_EMAIL'],
        'MEETUP_GROUP_NAME': os.environ['SITE_BOT_MEETUP_GROUP_NAME']
    }

    CONSTANTS['EVENT_POSTS_DIR'] = os.path.join(
        CONSTANTS['REPO_PATH'], 'events', '_posts')

    return CONSTANTS


if __name__ == "__main__":
    app = App(CONSTANTS())
    app.poll_and_update()
