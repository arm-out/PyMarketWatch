# PyMarketWatch
#
# This python file contains all the methods and variables needed to run a
# Twitter bot using the Twitter API to tweet news and information relevant
# to the stock market. News articles and healines are obtained via the News API

import tweepy
import requests
import time, calendar
from datetime import datetime
import pytz
import os

# API Keys for Twitter API
TWITTER_API_KEY = os.environ.get('API_KEY')
TWITTER_API_SECRET = os.environ.get('API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

# API Key for News API
NEWS_API_KEY = os.environ.get('NEWS_API')

# File to store last seen title
FILE_NAME_NEWS = 'last_seen_title.txt'

# Twitter API authentication
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Retrieves news in the JSON format
def retrieveNews():
    url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'category=business&'
       'apiKey=' + NEWS_API_KEY)

    return requests.get(url).json()

# Retrieves last seen title from file
def retrieveLastSeenTitle(fileName):
    readFile = open(fileName, 'r')
    lastSeenTitle = readFile.read().strip()
    readFile.close()
    return lastSeenTitle

# Stores last seen title onto file
def storeLastSeenTitle(fileName, title):
    writeFile = open(fileName, 'w')
    writeFile.write(title)
    writeFile.close()
    return

# Tweets from a list of news articles
def tweetNews(news):
    articles = news["articles"]
    lastSeenTitle = retrieveLastSeenTitle(FILE_NAME_NEWS)
    lastSeenFound = False
    lastSeenPassed = True

    # Checks if articles have already been tweeted about
    for article in reversed(articles):
        if (article["title"] == lastSeenTitle):
            lastSeenFound = True
            lastSeenPassed = False

    # Tweets individual articles
    for article in reversed(articles):
        # Skips previously tweeted articles
        if (article["title"] == lastSeenTitle and lastSeenFound):
            lastSeenPassed = True
            continue

        if lastSeenPassed:
            tweet = article["title"] + " " + article["url"]
            print("Tweeting article...")     
            twitter_api.update_status(status=tweet)

    # Stores the last tweeted article onto file
    storeLastSeenTitle(FILE_NAME_NEWS, articles[0]["title"])

# Checks if the US market has opened or closed and tweets accordingly
def marketOpenOrClose():
    tz = pytz.timezone('US/Eastern')
    timeNow = datetime.now(tz)
    nyTime = datetime.strftime(datetime.now(tz), "%H:%M")
    openTime = "01:55"
    closeTime = "16:00"
    open = False

    # Tweets when US market opens
    if (nyTime == openTime and open == False
        and calendar.weekday(timeNow.year, timeNow.month, timeNow.day) < 5):
        twitter_api.update_status("The US Market has now opened!!")
        open = True
    
    # Tweets when the US market closes
    if (nyTime == closeTime and open == True):
        twitter_api.update_status("The US Market has now closed")
        
# Initializing message
print('=================================')
print("Initializing PyMarketWatch")
print('=================================')

# Run Loop
while True:
    print("Checking for news...")
    news = retrieveNews()
    tweetNews(news)
    marketOpenOrClose()
    time.sleep(300)

