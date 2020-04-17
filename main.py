import tweepy
import requests
import time, calendar
from datetime import datetime
import pytz

TWITTER_API_KEY = 'iSbU97tE2VqYVrqG4MssoLYq1'
TWITTER_API_SECRET = 'PBmDkdOklq1TBLBbEOyMzLjdmNxMkOil1GFkZzpuNUDm1Okaeg'
TWITTER_ACCESS_TOKEN = '1250156125053423619-7fiwAxBS057LGeDgB9tBKqmvlWRit5'
TWITTER_ACCESS_SECRET = 'y4fFDoMcLG95FiFEZBMHNh1DjmDkOgTXHCpYdKLD4yu0O'

NEWS_API_KEY = 'fa2dd98685aa42859cb353e4a66c7e94'

FILE_NAME_NEWS = 'last_seen_title.txt'

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)



def retrieveNews():
    url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'category=business&'
       'apiKey=' + NEWS_API_KEY)

    return requests.get(url).json()
    
def retrieveLastSeenTitle(fileName):
    readFile = open(fileName, 'r')
    lastSeenTitle = readFile.read().strip()
    readFile.close()
    return lastSeenTitle

def storeLastSeenTitle(fileName, title):
    writeFile = open(fileName, 'w')
    writeFile.write(title)
    writeFile.close()
    return

def tweetNews(news):
    articles = news["articles"]
    lastSeenTitle = retrieveLastSeenTitle(FILE_NAME_NEWS)
    lastSeenFound = False
    lastSeenPassed = True

    for article in reversed(articles):
        if (article["title"] == lastSeenTitle):
            lastSeenFound = True
            lastSeenPassed = False

    for article in reversed(articles):
        if (article["title"] == lastSeenTitle and lastSeenFound):
            lastSeenPassed = True
            continue

        if lastSeenPassed:
            tweet = article["title"] + " " + article["url"]
            print("Tweeting article...")     
            #twitter_api.update_status(status=tweet)

    storeLastSeenTitle(FILE_NAME_NEWS, articles[0]["title"])

def marketOpenOrClose():
    tz = pytz.timezone('US/Eastern')
    timeNow = datetime.now(tz)
    nyTime = datetime.strftime(datetime.now(tz), "%H:%M")
    openTime = "01:55"
    closeTime = "16:00"
    open = False

    if (nyTime == openTime and open == False
        and calendar.weekday(timeNow.year, timeNow.month, timeNow.day) < 5):
        twitter_api.update_status("The US Market has now opened!!")
        open = True
    
    if (nyTime == closeTime and open == True):
        twitter_api.update_status("The US Market has now closed")
        

print('=================================')
print("Initializing PyMarketWatch")
print('=================================')

while True:
    print("Checking for news...")
    news = retrieveNews()
    tweetNews(news)
    marketOpenOrClose()
    time.sleep(300)

