import tweepy

import sys
import os
sys.path.append(os.getcwd() + "/static/scripts")
from py.access import Access

auth = tweepy.OAuthHandler(Access.consumer_key, Access.consumer_secret)
auth.set_access_token(Access.access_token, Access.access_token_secret)

api = tweepy.API(auth)

def hexParse(tweet):
    # Change from hard code later... Need unicode conversion
    tweet = tweet.replace("%23", "#")
    tweet = tweet.replace("%22", "\"")
    tweet = tweet.replace("+", " ")
    return tweet

def nearbyTrends(latitude, longitude):
    geoID = api.trends_closest(latitude, longitude)

    trending_tweets = api.trends_place(geoID[0]['woeid'])
    print "TOTAL TWEETS: " + str(len(trending_tweets[0]['trends']))

    trends = []
    for tweet in trending_tweets[0]['trends']:
        trends.append(hexParse(str(tweet['query'])))

    return trends

if __name__ == "__main__":
    print nearbyTrends(27.6648, 81.5158)
