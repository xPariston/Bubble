import twitter_scraper
from volt_dict import volttwitter
import datetime

class tweetclass:
    def __init__(self,user,url,tweet):
        self.user = user
        self.url = url
        self.tweet = tweet


def scrapetweets(time):
    allnewtweets = []

    for twitteruser in volttwitter:
        for tweet in twitter_scraper.get_tweets(twitteruser,pages=1):
            if tweet['time'] <= datetime.datetime.now() + datetime.timedelta(minutes=time):
                url = "https://twitter.com/" + twitteruser + "/status/" + tweet["tweetId"]
                allnewtweets.append(tweetclass(twitteruser,url,tweet))

    return allnewtweets

