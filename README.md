# @PyMarketWatch: A Financial News Bot

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) 

### Introduction

This is a simple twitter bot that aims to help you stay up to date on various business news. It implements the Twitter API along with using the News API to collect news titles and sources.

### Cloning and Setting up

If you wish to clone this repository to experiment with the code and make it your own, there are a few simple steps you have to follow.

#### Additional Modules

This project relies on two additional python modules `tweepy` and `pytz`. `tweepy` is a wrapper for the Twitter API while `pytz` is used to set the timezone to US Eastern time for the bot to be able to tweet when the market opens and closes. The easiest way to install this is by using pip in the repository's directory:

```
$ pip3 install -r requirements.txt
```

#### API Keys

In main.py, you would see the following block of code:

```python
# API Keys for Twitter API
TWITTER_API_KEY = os.environ.get('API_KEY')
TWITTER_API_SECRET = os.environ.get('API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
```

These API keys are unique to every user and you will have to generate one for yourself at [developer.twitter.com](developer.twitter.com). Once you have generated your codes, simply replace the `os.environ.get('') `in each line with its respective code. The same would be done for the key of the News Api

```python
# API Key for News API
NEWS_API_KEY = os.environ.get('NEWS_API')
```

You can generate a key for this api at [newsapi.org](newsapi.org)

#### Deleting Extra Files

You can also go ahead and delete the Procfile as it is mainly used by me to deploy the bot on Heroku

### Check it out in action!

Check out the bot [@PyMarketWatch](https://twitter.com/PyMarketWatch)

