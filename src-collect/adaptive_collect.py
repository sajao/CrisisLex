# CrisisLex
# Author: Alexandra Olteanu
# Check LICENSE for details about copyright.

import sys
import utils
import os

#handling time
import datetime

#tweepy1
import tweepy1 as t
from tweepy1.parsers import ModelParser
from tweepy1 import StreamListener
from tweepy1 import Stream

#command line parsing
from optparse import OptionParser

# authentication parameters
import config as c

#nlp processing
import nltk
from nltk.corpus import stopwords

#processes the tweet and updates hashtag_fd
#specifically, if the hashtag was already encountered it adds it to the freq dict,
# otherwise it increases the hashtag counter
def update_hashtags_stats(hashtags_fd, json_tweet):
    tweet = utils.extract_tweet_from_json(json_tweet)
    tweet_terms = []
    if tweet is None or '#' not in tweet:
        return False
    tokenizer = nltk.RegexpTokenizer('\#?[\w\d]+')
    doc = tokenizer.tokenize(tweet)
    for w_raw in doc:
        if '#' not in w_raw:
            continue
        w = (w_raw.strip('\"\'.,;?!:)(@/*&')).lower()
        tweet_terms.append(w)
        hashtags_fd.inc(w)
    return True


#processes the tweet and updates terms_fd based on the tweet terms
#specifically, if the term was already encountered it adds it to the freq dict,
# otherwise it increases the term counter
def update_terms_stats(terms_fd, json_tweet, lex):
    tweet = utils.extract_tweet_from_json(json_tweet)
    tweet_terms = []
    if tweet is None:
        return False
    tokenizer = nltk.RegexpTokenizer('\#?[\w\d]+')
    doc = tokenizer.tokenize(tweet)
    for w_raw in doc:
        w = w_raw.strip('\"\'.,;?!:)(@/*&')
        if not (w.strip('#')).isalpha():
            w_aux = ''
            #ignore non-ascii characters
            for s in w:
                if ord(s) < 128:
                    w_aux += s
                else:
                    break
            w = w_aux
        w = w.lower()
        if (w not in stopwords.words('english') and w not in set(['rt','http','amp'])) and len(w) in range(3, 16):
            if w in lex:
                continue
            tweet_terms.append(w)
            terms_fd.inc(w)
    bigrams = nltk.bigrams(tweet_terms)
    for b in bigrams:
        if b[1]+" "+b[0] in lex or b[0]+" "+b[1] in lex:
            continue
        if b[1]+" "+b[0] in terms_fd:
            terms_fd.inc(b[1]+" "+b[0])
        else:
            terms_fd.inc(b[0]+" "+b[1])
    return True


class AdaptiveListener(StreamListener):
    output = None
    adaptive = False
    start_time = None
    end_time = None
    terms = None
    terms_fd = None
    terms_no = 0
    lex_set = None
    use_hashtags = True

    def on_data(self, data):
        #prints to screen the filtered tweets
        if self.output is None:
            print data
            return True

        #prints to file the filtered tweets without any other actions
        print>>self.output, data.strip()
        if self.adaptive is False:
            return True

        #collects statistics from the tweets collected in the first hours and prints the tweets to file
        if self.adaptive:
            if datetime.datetime.now()>self.end_time:
                self.terms = self.terms_fd.keys()[:self.terms_no]
                print "Adding to the query the following terms:"
                print self.terms
                return False

            if self.use_hashtags:
                update_hashtags_stats(self.terms_fd,data)
            else:
                update_terms_stats(self.terms_fd,data,self.lex_set)
            return True

    def on_error(self, status):
        if status == 420:
            print status, "Twitter API Error: Enhance your calm -- You are being rate limited"
        elif status == 401:
            print status, "Twitter API Error: Unauthorized -- Authentication credentials were missing or incorrect. Please double check config.py"
        else:
            print status

    def set_output(self, output_json):
        self.output = output_json

    def set_adaptive(self, lex, learning_time=3, use_hashtags=True, new_terms_no=10):
        self.adaptive = True
        self.lex_set = set(lex)
        self.terms_no = new_terms_no
        self.use_hashtags = use_hashtags

        self.start_time = datetime.datetime.now()
        self.end_time = self.start_time + datetime.timedelta(hours=learning_time)
        print "Learning interval between %s to %s"%(self.start_time,self.end_time)

        self.terms_fd = nltk.FreqDist()
        self.terms = []

if __name__ == "__main__":

    #command line options
    parser = OptionParser()
    parser.add_option("-l", "--lexicon", dest="lexicon",
                    help="Read lexicon from file. Expects one term per line.",
                    metavar="FILE", default="")
    parser.add_option("-t", "--optional_terms", dest="additional",
                    help="Read user defined terms from file. Expects one term per line.",
                    metavar="FILE", default="")
    parser.add_option("-o", "--output", dest="filename",
                    help="Write output to FILE. The expected format is .json",
                    metavar="FILE", default="your_unnamed_collection.json")
    parser.add_option("-p", "--time", dest="prf_time",
                    help="Indicates how much time the crawler collects data before it adapts the query to the most prominent crisis",
                    metavar="Hours", type=int, default=1)
    parser.add_option("-a", "--set_adaptive", dest="adaptive",
                    help="Specifies if the query will be refined to the most prominent crises",
                    action="store_true",
                    default=False)
    parser.add_option("-k","--hashtags", dest = "hashtags",
                    help="0 - use any type of terms; 1 - use only hashtags; 2 - combine hashtags with other terms",
                    default=1)
    parser.add_option("-n","--new_terms", dest="new_terms_no",
                    help="Specifies the number of new terms to be added to the query",
                    type=int, default=5)
    parser.add_option("-x", "--set_proxy", dest="proxy",
                    help="Sets proxy",
                    metavar="PROXY", default = "")

    (options, args) = parser.parse_args()

    #set proxy
    if len(options.proxy) != 0:
        os.environ['http_proxy']= options.proxy
        os.environ['https_proxy']= options.proxy

    #authenticate
    auth = t.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
    auth.set_access_token(c.ACCESS_KEY, c.ACCESS_SECRET)
    api = t.API(auth_handler=auth, parser=ModelParser())

    #set up the stream listener
    pl = AdaptiveListener()
    pl.set_output(open(options.filename,"w"))

    if len(options.lexicon) == 0:
        sys.exit("It is mandatory to provide a lexicon. " +
                 "Run the scrip with -h or --help to learn about options, or try from the script location: " +
                 "python adaptive_collect.py -l ../data/lexicon-v1/crisislex_recommended_v1.txt")

    # get lexicon terms
    try:
        to_track = utils.get_query_terms(open(options.lexicon,"r"))
    except Exception as e:
        print "The file path is seems to be wrong. Check the error below or run the script with -h. Please revise and restart the script"
        print e
        exit(0)

    # add user defined terms
    if len(options.additional) > 0:
        additional_terms = utils.get_query_terms(open(options.additional,"r"))
        to_track[0:0] = additional_terms

    #set the learning time
    if options.adaptive:
        pl.set_adaptive(to_track, options.prf_time, (options.hashtags == 1), options.new_terms_no)

    #start tracking crisis-relevant tweets
    stream = Stream(auth, pl)
    stream.filter(track=to_track[0:400])

    print "New query..."
    #add new terms to be tracked and restart the crawling.
    if pl.adaptive:
        assert pl.terms
        to_track[0:0] = pl.terms

    pl.adaptive = False
    stream.filter(track=to_track[0:400])