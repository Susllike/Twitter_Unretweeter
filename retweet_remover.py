import tweepy
import configparser
import time

#config
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#Authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = config['twitter']['username']

user_stats = api.get_user(screen_name = user)
statuses_count = user_stats.statuses_count

#Ceiling divison
loops = -1 * (-statuses_count // 200)

#All tweets info will be here
all_tweets = []

end_tweet_id = user_stats._json["status"]["id"]

#Most recent tweet appending
all_tweets.append(
	{
		"text": api.get_status(end_tweet_id).text,
		"id": end_tweet_id,
	}
)

for i in range(loops):
	tweets = api.user_timeline(
		screen_name = user, 
		count = 200, 
		max_id = end_tweet_id)

	if len(tweets) != 200:
		end_tweet_id = tweets[len(tweets)-1].id
	else:
		end_tweet_id = tweets[199].id

	for i in range(1, len(tweets)):
		all_tweets.append(
			{
				"text": tweets[i].text,
				"id": tweets[i].id
			}
		)

#Counter for aesthetics
count = 0
for tweet in all_tweets:
	#"RT" in the beginning of tweets means it's a retweet.
	if tweet["text"][0:2] == "RT":
		api.unretweet(tweet["id"])
		print(f"#{count+1} unretweeted!")
		count += 1
		time.sleep(0.1)