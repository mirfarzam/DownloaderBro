
import tweepy
import datetime
import configparser
import time


config = configparser.ConfigParser()
config.read('credential.conf')

consumer_key = config['API']["API_key"]
consumer_secret = config['API']["API_secret_key"]
access_token = config['ACCESS']["Access_token"]
access_token_secret = config['ACCESS']["Access_token_secert"]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# api.verify_credentials()

def check_mentions(api, keywords, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is None:
            continue
        main = (api.statuses_lookup([tweet.in_reply_to_status_id], include_entities=True ))[0]
        final_video = None
        try :
           if 'media' in main.extended_entities:
               maxBit = 0
               maxURL = None
               for video in main.extended_entities['media'][0]['video_info']['variants']:
                   try:
                    #    print(f"{video['bitrate']} and is {video['url']}")
                       if video['bitrate'] > maxBit:
                           maxBit = video['bitrate']
                           maxURL = video['url']
                   except:
                    #    print(f"Error in finding video in tweet id : {main.id}")  
                    continue   
            #    final_video = max(MyCount, key=int)
               if maxURL is not None:
                  api.update_status(f'@{tweet.user.screen_name} Hi Bro! this is the Link {maxURL}', in_reply_to_status_id = tweet.id_str) 
        except:
            # print(f"Cannot get Tweet video and tweet id is : {main.id}")
            continue
        # print(final_video)
        
    return new_since_id


since_id = 1
while True:
    since_id = check_mentions(api, ["help", "support"], since_id)
    time.sleep(10)