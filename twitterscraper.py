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
        twitterpage = twitter_scraper.get_tweets(twitteruser,1)
        for tweet in twitterpage:
            if tweet['time'] <= datetime.datetime.now() + datetime.timedelta(minutes=time):
                url = "https://twitter.com/" + twitteruser + "/status/" + tweet["tweetId"]
                allnewtweets.append(tweetclass(twitteruser,url,tweet))

    return allnewtweets

