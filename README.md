[![Build Status](https://travis-ci.org/OpenTwinCities/site_bot.svg?branch=master)](https://travis-ci.org/OpenTwinCities/site_bot)

Open Twin Cities Site Bot
=========================

A bot that automatically adds and updates content on <http://www.opentwincities.org>.

OTCSB uses the Meetup.com RSS feed to get events, then uses a local copy of the OTC GitHub Pages repository to commit those events to the repo.

# Setup

## Dependencies

- python 2.x
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

### Details for usage with pyenv
Assuming [pyenv](https://github.com/pyenv/pyenv) is installed and initialized.

```bash
pip install virtualenv
pip install virtualenvwrapper
brew install pyenv-virtualwrapper
pyenv virtualenvwrapper
```

## Environment Variables

The following environment variables must be set:

- `SITE_BOT_REPO_AUTHOR_NAME`: Name to be included for the commit author
- `SITE_BOT_REPO_AUTHOR_EMAIL`: Email Address to be used for the commit author
- `SITE_BOT_MEETUP_GROUP_NAME`: Name of the group to get events from
- `SITE_BOT_MEETUP_API_KEY`: API key from Meetup

## opentincities.github.com repo

Events appear on [opentwincities.org](https://www.opentwincities.com) by committing to the [opentwincities.github.com repo](https://github.com/OpenTwinCities/opentwincities.github.com). This repo must be in a subfolder named `opentwincities.github.com`.

You'll probably want to author and push commits to the [opentwincities.github.com repo] as a user other than your
personal git/GitHub user. SSH config can be used to enable this. See
<http://stackoverflow.com/questions/7927750/specify-an-ssh-key-for-git-push-for-a-given-domain>

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
