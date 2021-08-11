import tweepy
import pandas as pd
import datetime
import random

# auth
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
A_TOKEN = ''
A_SECRET = ''

# Setup API access
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(A_TOKEN, A_SECRET)

api = tweepy.API(auth)

# Check connection
api.verify_credentials()


# Create function to extract tweet object attributes from a given time frame
# Then create a dataframe to store tweets
def get_tweets(tweet_object):
    # creating an empty list for tweet objects
    tweets = []

    # Determine start of week and end of week
    today = datetime.date.today()
    start_of_week = pd.to_datetime(today - datetime.timedelta(days=today.weekday()))

    # loop through tweet objects to extract pertinent attributes
    for t in tweet_object:
        tweet_id = t.id  # unique ID
        text = t.text  # text from tweet
        favs = t.favorite_count  # count of favs
        rts = t.retweet_count  # count of RTs
        created = t.created_at

        # check to see if tweet was retweeted or original tweet
        # check to see if tweet is from this week
        if hasattr(t, 'retweeted_status') or created <= start_of_week:
            continue  # skip tweet if RT or not from the current week
        else:
            pass  # add tweet if original

        # append attributes to list
        tweets.append({'tweet_id': tweet_id,
                       'text': text,
                       'favs': favs,
                       'rts': rts,
                       'created': created})

    # create data frame from tweets list
    df = pd.DataFrame(tweets, columns=['tweet_id',
                                       'text',
                                       'favs',
                                       'rts',
                                       'created'])

    # create a popularity score (rts + favs)
    df['popularity'] = df['rts'] + df['favs']

    # convert UTC to Central time
    df['created_local'] = df['created'].dt.tz_localize('UTC').dt.tz_convert('US/Central')

    return df


# Get most popular tweet
def get_popular(df):
    # Get most popular tweet
    max = df['popularity'].max()
    id = df[df['popularity'] == max]['tweet_id'].values[0]
    rt = df[df['popularity'] == max]['rts'].values[0]
    fav = df[df['popularity'] == max]['favs'].values[0]
    return [id, rt, fav]


# Retweet the most popular tweet of the week
def rt_popular(df):
    # Get tweet ID of most popular tweet
    id = get_popular(df)[0]

    # Retweet most popular tweet
    api.retweet(id)


# Favorite the most popular tweet of the week
def fav_popular(df):
    # Get tweet ID of most popular tweet
    id = get_popular(df)[0]

    # Retweet most popular tweet
    api.create_favorite(id)


# Reply to the most popular tweet of the week
def reply_popular(df):
    # Get tweet ID of most popular tweet
    id = get_popular(df)[0]

    # Static list of responses that will be chosen by random
    reply = ['YAASSS! This tweet was a banger! We have no choice but to #STAN #SoSofia',
             'This tweet is #SoSofia',
             'Imma STANfia #SoSofia',
             'Killing the Twitter game! #SoSofia',
             'This tweet was #GIRLBOSS #SoSofia',
             'Girlie keep it up! WE STAN! #SoSofia',
             'Your tweets are golden we must protect them AT ALL COST! #STAN #SoSofia']

    # Generate a random number that will be used to index into the reply list
    num = random.randint(0, 6)

    # Reply most popular tweet
    api.update_status(f'@wisdomberryson {reply[num]}', id)


# Get Sofia's tweets
user = 'wisdomberryson'
sofia = api.user_timeline(user, count=500)
sofia_tweets = get_tweets(sofia)

# Retweet most popular tweet
rt_popular(sofia_tweets)

# Favorite most popular tweet
fav_popular(sofia_tweets)

# Reply to Sofia's most popular tweet
reply_popular(sofia_tweets)
