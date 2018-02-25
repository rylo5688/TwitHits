from access import Access
import tweepy
import json
import requests

auth = tweepy.OAuthHandler(Access.consumer_key, Access.consumer_secret)
auth.set_access_token(Access.access_token, Access.access_token_secret)

api = tweepy.API(auth)

def hexParse(tweet):
    # Change from hard code later... Need unicode conversion
    tweet = tweet.replace("%23", "#")
    tweet = tweet.replace("%22", "")
    tweet = tweet.replace("+", " ")
    return tweet

def analyzeTone(tweet):
    headers = {"content-type": "text/plain"}

    r = requests.post(Access.ibmUrl, auth=(Access.ibmUsername, Access.ibmPassword),headers = headers,
         data=tweet)
    return r.text

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

    # searchTweets(trends, latitude, longitude, 20)

    json_string = json.dumps(trends)
    return json.loads(json_string)

def searchTweets(trends, latitude, longitude, radius):
    # Geocode with lat,long,radius
    gCode = str(latitude) + "," + str(longitude) + "," + str(radius) + "mi"

    queryAndTweet = {}
    for query in trends:
        results = api.search(q=query, lang="en", count=3, result_type="recent", geocode=gCode, tweet_mode="extended")
        # print results
        tweets = {}
        count = 1
        for tweet in results:
            tweets['tweet' + str(count)] = {}
            tweets['tweet' + str(count)]['username'] = tweet._json['user']['screen_name']
            tweets['tweet' + str(count)]['timestamp'] = tweet._json['created_at']
            tweets['tweet' + str(count)]['tweet'] = tweet._json['full_text']
            tweets['tweet' + str(count)]['hashtags'] = tweet._json['entities']['hashtags']
            tweets['tweet' + str(count)]['sentiment'] = analyzeTone(tweet._json['full_text'].encode(errors='ignore').decode('utf-8'))
            count = count + 1

        print tweets
        if query in queryAndTweet:
            queryAndTweet[query].append(tweets)
        else:
            queryAndTweet[query] = tweets
    # print queryAndTweet
    json_string = json.dumps(queryAndTweet)
    return json.loads(json_string)


# if __name__ == "__main__":
#     print nearbyTrends(27.6648, 81.5158)
