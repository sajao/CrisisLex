# Tweepy
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

"""
Tweepy Twitter API library
"""
__version__ = '2.1'
__author__ = 'Joshua Roesslein'
__license__ = 'MIT'

from tweepy1.models import Status, User, DirectMessage, Friendship, SavedSearch, SearchResults, ModelFactory, Category
from tweepy1.error import TweepError
from tweepy1.api import API
from tweepy1.cache import Cache, MemoryCache, FileCache
from tweepy1.auth import BasicAuthHandler, OAuthHandler
from tweepy1.streaming import Stream, StreamListener
from tweepy1.cursor import Cursor

# Global, unauthenticated instance of API
api = API()

def debug(enable=True, level=1):

    import httplib
    httplib.HTTPConnection.debuglevel = level

