[![Build Status](https://travis-ci.org/OpenTwinCities/site_bot.svg?branch=master)](https://travis-ci.org/OpenTwinCities/site_bot)

Open Twin Cities Site Bot
=========================

A bot that automatically adds and updates content on <http://www.opentwincities.org>.

# Setup 

## Dependencies

- python
- [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

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
