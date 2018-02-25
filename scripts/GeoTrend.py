from access import Access
import tweepy
import json

auth = tweepy.OAuthHandler(Access.consumer_key, Access.consumer_secret)
auth.set_access_token(Access.access_token, Access.access_token_secret)

api = tweepy.API(auth)

def hexParse(tweet):
    # Change from hard code later... Need unicode conversion
    tweet = tweet.replace("%23", "#")
    tweet = tweet.replace("%22", "")
    tweet = tweet.replace("+", " ")
    return tweet

def nearbyTrends(latitude, longitude):
    # Getting WOEID from lat, long coords
    geoID = api.trends_closest(latitude, longitude)

    # Gettings trends near the WOEID
    trending_tweets = api.trends_place(geoID[0]['woeid'])

    trends = []
    count = 0

    # Extracting trends based on geolocation
    for tweet in trending_tweets[0]['trends']:
        if (count >= 10):
            break

        trends.append(hexParse(str(tweet['query'])))
        count = count+1

    searchTweets(trends, latitude, longitude, 10)

    json_string = json.dumps(trends)
    return json.loads(json_string)

def searchTweets(trends, latitude, longitude, radius):
    # Geocode with lat,long,radius
    gCode = str(latitude) + "," + str(longitude) + "," + str(radius) + "mi"

    queryAndTweet = {}
    for query in trends:
        results = api.search(q=query, lang="en", count=1, result_type="recent", geocode=gCode)

        tweets = {}
        count = 1
        for tweet in results:
            # print tweet._json
            tweets['tweet' + str(count)] = {}
            tweets['tweet' + str(count)]['username'] = tweet._json['user']['screen_name']
            tweets['tweet' + str(count)]['timestamp'] = tweet._json['created_at']
            tweets['tweet' + str(count)]['tweet'] = tweet._json['text']
            tweets['tweet' + str(count)]['hashtags'] = tweet._json['entities']['hashtags']
            count = count + 1

        print tweets
        if query in queryAndTweet:
            queryAndTweet[query].append(tweets)
        else:
            queryAndTweet[query] = tweets
    print queryAndTweet
    json_string = json.dumps(queryAndTweet)
    return json.loads(json_string)

if __name__ == "__main__":
    print nearbyTrends(40.0068, -105.2628)
