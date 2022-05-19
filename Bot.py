from turtle import title
from typing import Text
import requests
import tweepy
import Config
import schedule
import time
import json

FILE_NAME = 'last_seen_id.txt'
run = True
client = tweepy.Client(bearer_token=Config.bearer_token,
                       consumer_key=Config.consumer_key,
                       consumer_secret=Config.consumer_secret,
                       access_token=Config.access_token,
                       access_token_secret=Config.access_token_secret, wait_on_rate_limit=True)
id = '1449222073058947075'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    print("last_seen_id:", last_seen_id)
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


# reply to Mentions
def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = client.get_users_mentions(
        since_id=last_seen_id,
        id=id, tweet_fields=['context_annotations', 'created_at'])

    if(mentions.data is None):
        print("No Data")
    elif(mentions.data is not None):
        for mention in reversed(mentions.data):
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)
            client.like(tweet_id=mention.id)
            if('#nftdrop' in mention.text.lower()):
                print('found #NFTdrop!', flush=True)
                print('responding back...', flush=True)
                client.create_tweet(
                    text='👏👏 #PSreply', in_reply_to_tweet_id=mention.id)


def auto_news_post():
    url = "https://free-news.p.rapidapi.com/v1/search"

    querystring = {"q": "Nft", "lang": "en", "page": "1", "page_size": "1"}

    headers = {
        "X-RapidAPI-Host": "free-news.p.rapidapi.com",
        "X-RapidAPI-Key": "4b500d0328msheeff8a655532a58p16802cjsn97292550983c"
    }

    res = requests.request("GET", url, headers=headers, params=querystring)
    response = res.json()
    article = response['articles'][0]
    Title = article['title']
    Link = article['link']

    print("Posting News.... \n", Title, flush=True)
    Text = ("News Today" + "\n" + Title + "\n" + Link)
    client.create_tweet(text=Text)
    print("Posted News")


schedule.every().day.at("05:00").do(auto_news_post)

while run:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
    reply_to_tweets()
    time.sleep(15)
