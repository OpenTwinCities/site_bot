[![Build Status](https://travis-ci.org/OpenTwinCities/site_bot.svg?branch=master)](https://travis-ci.org/OpenTwinCities/site_bot)

Open Twin Cities Site Bot
=========================

A bot that automatically adds and updates content on <http://www.opentwincities.org>.

# Setup 

## Dependencies

- python
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [opentwincities.github.com repo](https://github.com/OpenTwinCities/opentwincities.github.com) -
  Must be in a subfolder named `opentwincities.github.com`

## Environment Variables

The following environment variables must be set:

- `SITE_BOT_REPO_AUTHOR_NAME`: Name to be included for the commit author
- `SITE_BOT_REPO_AUTHOR_EMAIL`: Email Address to be used for the commit author
- `SITE_BOT_REPO_AUTHOR_KEY`: Name of the SSH key to use when pulling/pushing 
- `SITE_BOT_MEETUP_GROUP_NAME`: Name of the group to get events from 
- `SITE_BOT_MEETUP_API_KEY`: API key from Meetup

## Dev Environment

```
git clone git@github.com:OpenTwinCities/site_bot.git
cd site_bot
mkvirtualenv site_bot
workon site_bot
pip install -r requirements.txt
```

# Tests

```
nosetests
```
