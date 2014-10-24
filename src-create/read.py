# CrisisLex
# Author: Alexandra Olteanu
# Check LICENSE for details about copyright.

import csv
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

def get_stemmed_terms_list(doc, stem_words_map = None, stem_bigrams_map = None):
    ps = PorterStemmer()
    local_map = dict()
    word_list = []

    clean_doc = [(w.strip()).lower() for w in doc.split() if len(w) in range(3,16)]
    filtered_words = [w.strip('.,;?!:)(#') for w in clean_doc if not w.strip('.,;?!:)(#') in stopwords.words('english')]

    for w in filtered_words:
        if w.isalpha():
            w_temp = ps.stem_word(w)
            if stem_words_map is not None:
                if w_temp not in stem_words_map:
                    stem_words_map[w_temp] = dict()
                stem_words_map[w_temp][w] = stem_words_map[w_temp].get(w, 0)+1
                local_map[w_temp] = w
            word_list.append(w_temp)

    bigrams = nltk.bigrams(word_list)
    for b in bigrams:
        bigram_org = (local_map[b[0]],local_map[b[1]])
        if stem_bigrams_map is not None:
                if b not in stem_bigrams_map:
                    stem_bigrams_map[b] = dict()
                stem_bigrams_map[b][bigram_org] = stem_bigrams_map[b].get(bigram_org, 0)+1

    return word_list, bigrams

# keeps track of the exact form of the stemmed bigrams, not only the one of the words
def get_tweet_terms(tweet, stem_map = None, bigrams_map = None):
    words, bigrams = get_stemmed_terms_list(tweet, stem_map, bigrams_map)
    filtered_words = [w for w in words if not w in stopwords.words('english')]

    bigrams = nltk.bigrams(filtered_words)
    words_set = set(filtered_words)
    terms_dict = {}

    for w in words_set:
        terms_dict['%s'%w] = 'y'

    for b in bigrams:
        terms_dict['%s %s'%(b[0],b[1])] = 'y'

    return terms_dict

def get_terms(ifile, stem_map = None, bigrams_map = None, min_occurence = 0.001):
    tweets_cls = []
    tweets_type = []
    tweets_terms = []
    tweets_id = []
    tweets_no = 0
    ws = set()
    wd_occ = dict()
    fd = nltk.FreqDist()
    r = csv.reader(ifile)

    print "Reading..."
    headers = r.next()
    for tokens in r:
        tweets_no += 1
        id = tokens[0].strip()
        tweet = tokens[1].strip()
        cls = tokens[2].strip()
        terms = get_tweet_terms(tweet, stem_map, bigrams_map)

        tweets_cls.append(cls)
        tweets_type.append(type)
        tweets_id.append((id,tweet))
        tweets_terms.append(terms)
        [fd.inc(x) for x in terms]
        ws.update(set(terms.keys()))
    print "... %s tweets"%tweets_no

    print "Cleaning..."
    for t in tweets_terms:
        s = set()
        term = t.keys()
        l = len(term)
        for i,f in enumerate(term):
            if fd[f] <= min_occurence*tweets_no:
                s.add(f)
            if l > 1:
                if i == l-1:
                    break
                for j in range(i+1, l):
                    wd_occ[(f, term[j])] = wd_occ.get((f, term[j]), 0)+1
        for f in s:
            del t[f]
            ws.discard(f)

    return tweets_cls, tweets_terms, wd_occ, ws, fd