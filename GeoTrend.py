# from access import Access
import tweepy
import json
import requests
from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')

# @app.route("/")

access_token = "895504784152641539-wdQSBCOwWIsvM0PkKsuanUOXnm3mUG9"
access_token_secret = "ugXTqduzil3XbVEJRXuPjhodz67Pd9mOu1RmQ5GlkEp1O"
consumer_key = "zHgyEexCVqfVBueaOvnlLXVrR"
consumer_secret = "DtDVzfv01mI4TkxjKj3M6XGS04wGVXi9tuJAxowd68w90D9g6Z"
ibmUsername = "3fed9a96-c16d-42e9-a828-f00773c6203c"
ibmPassword = "VFBY3QNTU4Id"
ibmUrl = "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

@app.route('/')
def index():
    return render_template('index.html')

def hexParse(tweet):
    # Change from hard code later... Need unicode conversion
    tweet = tweet.replace("%23", "#")
    tweet = tweet.replace("%22", "")
    tweet = tweet.replace("+", " ")
    return tweet

def analyzeTone(tweet):
    headers = {"content-type": "text/plain"}

    r = requests.post(Access.ibmUrl, auth=(ibmUsername, ibmPassword),headers = headers,
         data=tweet)
    return r.text

@app.route('/nearbyTrends/', methods=['GET'])
def nearbyTrends():
    # Getting data from ajax
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    return str( api.trends_place)
    # Getting WOEID from lat, long coords
    geoID = api.trends_closest(latitude, longitude)
    return str(geoID)
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

@app.route('/searchTweets/', methods=['GET'])
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

@app.route('/test/', methods=['GET'])
def test():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return str(latitude) + ',' + str(longitude)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
