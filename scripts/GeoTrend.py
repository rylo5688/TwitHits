from access import Access
import tweepy

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
    geoID = api.trends_closest(latitude, longitude)
    print geoID[0]['woeid']
    trending_tweets = api.trends_place(geoID[0]['woeid'])
    print "TOTAL TWEETS: " + str(len(trending_tweets[0]['trends']))

    trends = []
    count = 0
    for tweet in trending_tweets[0]['trends']:
        if (count >= 10):
            break

        trends.append(hexParse(str(tweet['query'])))
        count = count+1

    searchTweet(trends, latitude, longitude, 8)

    return trends

def searchTweet(trends, latitude, longitude, radius):
    # API.search(q[, lang][, locale][, rpp][, page][, since_id][, geocode][, show_user])
    gCode = str(latitude) + "," + str(longitude) + "," + str(radius) + "km"

    queryAndTweet = {}
    for query in trends:
        results = api.search(q=query, count=1, geocode=gCode)

        if query in queryAndTweet:
            queryAndTweet[query].append([results])
        else:
            queryAndTweet[query] = [results]

        # if len(results) > 0:
            # queryAndTweet.append({query : [] })




if __name__ == "__main__":
    print nearbyTrends(40.0068, -105.2628)
