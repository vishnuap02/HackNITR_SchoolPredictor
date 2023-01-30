# import requests
#
# def course_from_web_scrapper(url):
#     page = requests.get(url)
#
#     print(page.text)
#
# course_from_web_scrapper('https://www.ryangroup.org/academics/curriculums')

import tweepy
# import pandas as pd
# import flair
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')


api_key = "8xfDBiaypiJedpqaeNVuMkSRr"
api_key_secret = "Ir9wPWK8lcl3evzpvYazpfTaQGO0NX2dd5CcHBwJp4pDOE079N"
access_key = "1288461840482148353-3F7mvTs2JHOwq2ZWHvoIpMekzHmqbL"
access_key_secret = "qlUz3eHpfYMPpxIrqIfgf1Oyfnq6OTlY5rDN9mBYN8BB5"

def get_tweets(keywords):
    auth = tweepy.OAuth1UserHandler( api_key, api_key_secret,access_key ,access_key_secret )
    api = tweepy.API(auth)

    columns = ['date','user','text']
    data_tweets = []

    keywords = keywords+" lang:en -is:retweet -is:reply"
    # print(keywords)
    public_tweets = api.search_tweets(keywords,count=100,result_type='recent', lang='en')
    print('Total : ',len(public_tweets))

    for tweet in public_tweets:
        data_tweets.append(tweet.text)

    # df_tweets = pd.DataFrame(data_tweets,columns=columns)
    # print(df_tweets)

    return data_tweets


def tweet_sentiment(keywords):
    df_tweets = get_tweets(keywords)
    results = []
    sia= SIA()
    for headline in df_tweets:
        pol_score = sia.polarity_scores(headline)  # run analysis
        pol_score['headline'] = headline  # add headlines for viewing
        results.append(pol_score)
    sum=0
    count =0
    for val in results:
        sum+=val['compound']
        count +=1
    if count==0:
        avg=0
    else:
        avg = sum/count
    # df_tweets['Score'] = pd.DataFrame(results)['compound']
    return avg



# print(df_tweets)