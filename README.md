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
brew install pyenv-virtualenvwrapper
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
If you have the opentwincities.github.com repo locally, you can create a symbolic link to it. This example assumes your opentwincities.github.com and site_bot repos are in the same directory:
```bash
ln -s ../opentwincities.github.com opentwincities.github.com
```

To prepare you project for a local run execute
```bash
git clone git@github.com:OpenTwinCities/site_bot.git
cd site_bot
mkvirtualenv site_bot
workon site_bot
pip uninstall -y -r <(pip freeze)  # Uninstall any packages that exist in the virtualenv
pip install -r requirements.txt
```

## Running the tests

```bash
nosetests
```


# Tag & Deploy

This repository is setup to automatically deploy when a tag is pushed. Thus, to deploy, somebody
with write access to the repository can:

```bash
git tag                   # Find latest tag, decide what the next version should be based on SemVar
git tag X.Y.Z -a
git push origin tag X.Y.Z
```

This will cause Travis CI to run unit tests, then deploy if the tests pass.

## Deployment Details

### Deployed Environments

Site bot is currently deployed on an EC2 instance in Open Twin Cities' AWS account. The public
domain name of that instance is `ec2-52-6-202-131.compute-1.amazonaws.com`. Site bot is scheduled
to run once an hour via `cron`. This cron configuration also sets the
[Environment Variables](#environment-variables) for the script.


### Manual Deployment

```bash
pip uninstall -y -r <(pip freeze)  # Uninstall any packages that exist in the virtualenv
pip install -r deployment-requirements.txt
fab \
  -H USERNAME@HOST:PORT \
  -i PATH_TO_PRIVATE_KEY \
  deploy --ref BRANCH_OR_TAG_TO_DEPLOY
```

Note: The `site_bot` repo must already be cloned on the host that is being deployed to and located in
`/opt/site_bot`. The `opentwincities.github.com` must also already be cloned in
`/opt/site_bot/opentwincities.github.com` The user whose authentication is being used by `fabric`
must also have read and write permission on `/opt/site_bot`.

# Run the application
```bash
python app.py
```
