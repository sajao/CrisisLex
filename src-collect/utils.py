# CrisisLex
# Author: Alexandra Olteanu
# Check LICENSE for details about copyright.

import json

#receives a string in json format
#returns the textual content of a tweet
def extract_tweet_from_json(data):
    try:
        json_tweet = json.loads(data.strip())
    except:
        exit("Not able to load json data")
    if 'text' in json_tweet:
        return json_tweet['text'].replace('\n','')
    else:
        return None

# reads the terms to be tracked from a file
# expects one term per line
def get_query_terms(input_filename):
    query_terms = []
    for line in input_filename:
        query_terms.append(line.strip())
    return query_terms