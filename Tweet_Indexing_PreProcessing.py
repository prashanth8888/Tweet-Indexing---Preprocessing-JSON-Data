#Author: Prashanth Seralathan
#Course: Information Retrieval
#Place : Buffalo, NY
#Description: 
''' 
This Program converts the Raw JSON files obtained into required format that can be Indexed.
This Preprocessing involves the following steps,
1) Extracting Hash-Tags, Mentions, Emoticons and Coordinates(Location).
2) Text santizing
3) Classification based on the Language of the Tweet

Input: JSON file in RAW format containing the Tweets
Output: JSON file with all the pre-processing done and ready to be indexed.
		
'''


import json
import re
import string
from datetime import datetime
import pandas as pd


input_tweets_json = 'Iphone-SEP14-ko-sep18-copy2.json'
output_tweets_json= "Iphone-SEP14-ko-V02.json"
tweets_data = []


def get_time(tweet):
    time = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
    time = time.replace(minute=00, second=00)
    return time

def json_serial(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


#Gets the text, sans links, hashtags, mentions, media, and symbols.
def get_text_cleaned(tweet):
    urls = ''
    text = tweet['text']

    slices = []
    #Strip out the urls.
    if 'urls' in tweet['entities']:
        for url in tweet['entities']['urls']:
            slices += [{'start': url['indices'][0], 'stop': url['indices'][1]}]

    #Strip out the hashtags.
    if 'hashtags' in tweet['entities']:
        for tag in tweet['entities']['hashtags']:
            slices += [{'start': tag['indices'][0], 'stop': tag['indices'][1]}]
            #print("hash tags", slices)

    #Strip out the user mentions.
    if 'user_mentions' in tweet['entities']:
        for men in tweet['entities']['user_mentions']:
            slices += [{'start': men['indices'][0], 'stop': men['indices'][1]}]
            #print("User Mentions", slices)

    #Strip out the media.
    if 'media' in tweet['entities']:
        for med in tweet['entities']['media']:
            slices += [{'start': med['indices'][0], 'stop': med['indices'][1]}]

    #Strip out the symbols.
    if 'symbols' in tweet['entities']:
        for sym in tweet['entities']['symbols']:
            slices += [{'start': sym['indices'][0], 'stop': sym['indices'][1]}]

    # Sort the slices from highest start to lowest.
    slices = sorted(slices, key=lambda x: -x['start'])

    #No offsets, since we're sorted from highest to lowest.
    for s in slices:
        text = text[:s['start']] + text[s['stop']:]
    return text

def get_text_sanitized(tweet):
    return ' '.join([w.strip().rstrip(string.punctuation)\
        .lstrip(string.punctuation).strip()\
        for w in get_text_cleaned(tweet).split()\
        if w.strip().rstrip(string.punctuation).strip()])


def writeToJson():
    with open(output_tweets_json,'w+', encoding='utf8') as json_file:
        for tweet in updated_tweets:
            json_str = json.dumps(tweet, ensure_ascii=False, default=json_serial)
            json_file.write(json_str)


def determine_lang(lang):

        if lang == "en":
            new_json['text_en'] = text
        elif lang == "tr":
            new_json['text_tr'] = text
        elif lang == "ko":
            new_json['text_ko'] = text
        elif lang == "es":
            new_json['text_es'] = text

tweets_file = open(input_tweets_json, 'r', encoding='utf8').read()
count = 0
updated_tweets = []
tweet_dict={}
try:
    tweet_dict = json.loads(tweets_file)
except Exception as e:

    print("Exception while loading the json file", e)

for tweet in tweet_dict:
    try:
        new_json={}
        new_json['topic'] = "Tech"
        new_json['tweet_text'] = tweet['text']
        emoji_pattern = re.compile("["
               u"\U0001F600-\U0001F64F"  # emoticons
               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
               u"\U0001F680-\U0001F6FF"  # transport & map symbols
               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
			   u"\u2600-\u26FF\u2700-\u27BF"
                           "]")

        Sample_str = str(new_json['tweet_text'])
        lang = tweet['lang']
        new_json['tweet_lang'] = lang
        text = get_text_sanitized(tweet)
        text = emoji_pattern.sub(r'', text)
        emoticons = []
        emoticons = re.findall(u"["
               u"\U0001F600-\U0001F64F"  # emoticons
               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
               u"\U0001F680-\U0001F6FF"  # transport & map symbols
               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
			   u"\u2600-\u26FF\u2700-\u27BF" 
                           "]", new_json['tweet_text'])

        determine_lang(lang)
        text1 = tweet['text']

        if 'urls' in tweet['entities']:
            urls = ""
            for url in tweet['entities']['urls']:
                start = url['indices'][0]
                stop = url['indices'][1]
                url = text1[start:stop]
                #print('url', url)
                urls+=url+","
                #print('urls', url)
            urls=urls[0:len(urls)-1]

        new_json['tweet_urls'] = urls

        if 'hashtags' in tweet['entities']:
            hashtags = ""
            for tag in tweet['entities']['hashtags']:
                start = tag['indices'][0]
                stop = tag['indices'][1]
                hashtag = text1[start+1:stop]
                hashtags+=hashtag+","
            hashtags=hashtags[0:len(hashtags)-1]

        new_json['hashtags'] = hashtags

        if 'user_mentions' in tweet['entities']:
            mentions = ""
            for men in tweet['entities']['user_mentions']:
                start = men['indices'][0]
                stop = men['indices'][1]
                mention = text1[start+1:stop]
                mentions+=mention+","
            mentions=mentions[0:len(mentions)-1]

        new_json['mentions'] = mentions
        new_json['tweet_date'] = get_time(tweet)

        if tweet['geo'] is None:
            new_json['tweet_loc'] = None
        else:
            new_json['tweet_loc'] = tweet['geo']['coordinates']

        new_json['tweet_emoticons'] = emoticons
        updated_tweets.append(new_json)

    except Exception as e:
        print("Exception Happened", e)
        continue

#print("Number of updated Tweets", updated_tweets)

writeToJson()

