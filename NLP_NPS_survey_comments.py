# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 23:16:35 2023

@author: j00849687
"""

import facebook
import requests
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
nltk.download('punkt')

# Facebook authentication
app_id = '855595116359195'
app_secret = 'e364b8c9f6b1a14cf4a4238699a278d6'
access_token_url = f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=client_credentials"
access_token_response = requests.get(access_token_url)
access_token = access_token_response.json()['access_token']

# Initialize the Graph API with the access token
graph = facebook.GraphAPI(access_token)

# Fetch mentions of your page
page_id = 'bmobile'
mentions = graph.get_connections(id=page_id, connection_name='tagged', fields='message,created_time,from', limit=100)

# NLP Analysis
sentiments = []
all_words = []

for mention in mentions['data']:
    text = mention.get('message', '')
    blob = TextBlob(text)
    sentiments.append(blob.sentiment.polarity)  # Sentiment analysis
    words = nltk.word_tokenize(text)
    all_words.extend(words)

# Calculate the frequency distribution of words
word_freq = Counter(all_words)

# Most common words
common_words = word_freq.most_common(10)
words, counts = zip(*common_words)

# Plotting
plt.figure(figsize=(10, 5))

# Sentiment plot
plt.subplot(1, 2, 1)
plt.hist(sentiments, bins=20, color='blue')
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Frequency')

# Word frequency plot
plt.subplot(1, 2, 2)
plt.bar(words, counts, color='green')
plt.title('Top 10 Common Words')
plt.xlabel('Words')
plt.xticks(rotation=45)
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


#%%
import requests
import pandas as pd

def get_facebook_ads_data(account_id, access_token, fields, limit):
    url = f'https://graph.facebook.com/v17.0/{account_id}/ads?access_token={access_token}&fields={fields}&limit={limit}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Conexión exitosa")
        json_response = response.json()
        return json_response
    else:
        print(f"Error en la conexión. Código de estado: {response.status_code}")
        return None

variable_account_number = ''
access_token = ''
fields = 'insights{clicks,cpc,cpm,cpp,ctr,date_start,date_stop,frequency,impressions,objective,reach,spend,quality_ranking,account_id,account_name,campaign_name,campaign_id}'
limit = 10

ads_data_json = get_facebook_ads_data(variable_account_number, access_token, fields, limit)

if ads_data_json is not None:
    print(ads_data_json)