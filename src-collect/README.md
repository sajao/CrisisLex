Contents of this directory
==========================
The director contains scripts that allows anyone to easily collect tweets using CrisisLex. This can be done in two ways:

Simple data collection
----------------------
Collects tweets containing the lexicon terms.

**Parameters**

```
Usage: collect.py [options]

Options:
  -h, --help            show this help message and exit
  -l FILE, --lexicon=FILE
                        Read lexicon from file. Expects one term per line.
  -t FILE, --optional_terms=FILE
                        Read user defined terms from file. Expects one term
                        per line.
  -o FILE, --output=FILE
                        Write output to FILE. The expected format is .json
  -x PROXY, --set_proxy=PROXY
                        Sets proxy
```

Adaptive data collection
------------------------
Collects tweets containing the lexicon terms for a while, identifies new terms that describe the most prominent current crises, and resets the crawling with a new query that includes these new terms. 

**Parameters**

```
Usage: adaptive_collect.py [options]

Options:
  -h, --help            show this help message and exit
  -l FILE, --lexicon=FILE
                        Read lexicon from file. Expects one term per line.
  -t FILE, --optional_terms=FILE
                        Read user defined terms from file. Expects one term
                        per line.
  -o FILE, --output=FILE
                        Write output to FILE. The expected format is .json
  -p Hours, --pseudo_relevance_time=Hours
                        Indicates how much time the crawler collects data
                        before it adapts the query to the most prominent
                        crisis
  -a ADAPTIVE, --set_adaptive=ADAPTIVE
                        Specifies if the query will be adapted to the most
                        prominent crisis
  -k HASHTAGS, --hashtags=HASHTAGS
                        0 - use any type of terms; 1 - use only hashtags; 2 -
                        combine hashtags with other terms
  -n NEW_TERMS_NO, --new_terms_no=NEW_TERMS_NO
                        Specifies the number of new terms to be added to the
                        query
  -x PROXY, --set_proxy=PROXY
                        Sets proxy
```

**Note:**
* The addaptive collector implements a simple pseudo-relevance mechanism that ranks terms based on their frequency in the pseudo-relevant documents. For more details about it, or how to implement the label propagation based mechanism or the optimizations based on terms co-occurance check the [CrisisLex paper](http://crisislex.org/icwsm2014_crisislex.pdf) or drop us an email. 

Requirements & Dependencies
---------------------------
 * You need a set of Twitter API keys. To obtain the API keys, you have to first create a Twitter app via https://dev.twitter.com/apps and edit the config.py file. 
 * Only Python 2.7 is supported
 * The adaptive data collector depends on the following external libraries:
    * [Scipy](http://www.scipy.org)
    * [Numpy](http://www.numpy.org)
    * [NLTK (including the data)](http://www.nltk.org)
    * [scikit-learn](http://scikit-learn.org)

Questions/inquiries
-------------------

[Olteanu et al. 2014] Alexandra Olteanu, Carlos Castillo, Fernando Diaz, Sarah Vieweg: "[CrisisLex: A Lexicon for Collecting and Filtering Microblogged Communications in Crises](http://crisislex.org/papers/icwsm2014_crisislex.pdf)". In Proceedings of the AAAI Conference on Weblogs and Social Media (ICWSM'14). AAAI Press, Ann Arbor, MI, USA.

For inquiries please contact [Alexandra Olteanu](mailto:alexandra.olteanu@epfl.ch), or Carlos Castillo, or Fernando Diaz, or Sarah Vieweg.

Version history
---------------

 * 2014-10-26: v1.0 release.
 * 2014-07-14: pre-release.

