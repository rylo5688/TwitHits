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

for tweet in tweepy.Cursor(api.search,
                           q="Twice -filter:retweets",
                           rpp=10,
                           geocode="35.9078,127.7669,150km",
                           result_type="recent",
                           include_entities=True,
                           lang="en",
                           show_user=True).items():

    print(tweet.created_at, tweet.text)
  