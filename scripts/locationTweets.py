from access import Access
import tweepy
######## AUTHENTICATION
auth = tweepy.OAuthHandler(Access.consumer_key, Access.consumer_secret)
auth.set_access_token(Access.access_token, Access.access_token_secret)

api = tweepy.API(auth)
########
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

#### Embeded Tweets
#area = api.search("Tom Hanks", lang='en', rpp=5, page=1, geocode="35.9078,127.7669,150km", show_user=True)

def hexParse(tweet):
	tweet = tweet.replace("%23", "#")
	tweet = tweet.replace("%22", "\"")
	tweet = tweet.replace("+", " ")
	return tweet

def trend_in_area(lat, log):
	#tweets(api.trends_closest(lat, log), lat, log)
    geoID = api.trends_closest(lat, log)
    trending_tweets = api.trends_place(geoID[0]['woeid'])
    trends = []
    for tweet in trending_tweets[0]['trends']:
    	trends.append(hexParse(str(tweet['query'])))
    tweets(trends[0], lat, log)

def tweets(topic, lat, log):
	for tweet in tweepy.Cursor(api.search,
	                           q=topic + " -filter:retweets",
	                           rpp=10,
	                           geocode=str(lat)+","+str(log)+","+"150km",
	                           result_type="recent",
	                           include_entities=True,
	                           lang="en",
	                           show_user=True).items():

	    print(tweet.created_at, tweet.text)
  

if __name__ == "__main__":
    print(trend_in_area(36.7783,-119.4179))