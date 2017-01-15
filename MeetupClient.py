import requests


class MeetupClient:
    MEETUP_API_DOMAIN = 'api.meetup.com'

    def __init__(self, key, group_id):
        self.key = key
        self.group_id = group_id

    @property
    def events_url(self):
        return 'https://%s/%s/events' % (self.MEETUP_API_DOMAIN, self.group_id)

    @property
    def events(self):
        events = []
        request_url = self.events_url
        done = False
        while not done:
            resp = requests.get(request_url)
            if resp.status_code == 200:
                events += resp.json()
                if 'next' in resp.links:
                    request_url = resp.links['next']['url']
                else:
                    done = True
        return events
