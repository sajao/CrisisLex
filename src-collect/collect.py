# CrisisLex
# Author: Alexandra Olteanu
# Check LICENSE for details about copyright.

import sys
import tweepy1 as t
import utils
from tweepy1.parsers import ModelParser
from tweepy1 import StreamListener
from tweepy1 import Stream
from optparse import OptionParser

import config as c

class PrintListener(StreamListener):
    output = None
    def on_data(self, data):
        if self.output is None:
            print data
            return True
        else:
            print>>self.output, data.strip()
            return True

    def on_error(self, status):
        print status
        
    def set_output(self, output_json):
        self.output = output_json

if __name__ == "__main__": 

    #command line options
    parser = OptionParser()
    parser.add_option("-l", "--lexicon", dest="lexicon",
                  help="Read lexicon from file. Expects one term per line.",
                  metavar="FILE", default = "")
    parser.add_option("-t", "--optional_terms", dest="additional",
                  help="Read user defined terms from file. Expects one term per line.",
                  metavar="FILE", default = "")
    parser.add_option("-o", "--output", dest="filename",
                  help="Write output to FILE. The expected format is .json",
                  metavar="FILE", default = "your_json_file.json")
    (options, args) = parser.parse_args()

    #authenticate
    auth = t.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
    auth.set_access_token(c.ACCESS_KEY, c.ACCESS_SECRET)
    api = t.API(auth_handler=auth, parser = ModelParser())
    
    pl = PrintListener()
    pl.set_output(open(options.filename,"w"))
        
    if len(options.lexicon) == 0:
        sys.exit("It is mandatory to provide a lexicon. " +
                 "Run the scrip with -h or --help to learn about options, or try from the script location: " +
                 "python collect.py -l ../data/lexicon-v1/crisislex_recommended_v1.txt")

    to_track = utils.get_query_terms(open(options.lexicon,"r"))
    
    if len(options.additional) > 0:
        additional_terms = utils.get_query_terms(open(options.additional,"r"))
        to_track[0:0] = additional_terms
    
    #start tracking crisis-relevant tweets
    stream = Stream(auth, pl)
    stream.filter(track=to_track[0:400])