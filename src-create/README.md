
Contents of this directory
==========================
The director contains scripts that allows anyone to easily build a new lexicon for a domain of interest and collect data with it by using the collection scripts from **src-collect** folder. 

Build a Lexicon
------------------------
Given few Twitter collections from a domain of interest, the scripts generate a lexicon consisting of a set of terms (unigrams and bigrams) that are discriminative for the targeted domain. 

**Parameters**

```
Usage: build.py [options]

Options:
  -h, --help            show this help message and exit
  -s TEST, --terms_scoring=TEST
                        The statistical test used to score terms: pmi, chi2 or
                        frequency (in the relevant documents)
  -r, --hit_ratio       It normalizes the crisis score according to the number
                        of relevant tweets the term matches on.
  -t, --top_div         It filters out the terms with lower crisis scores that
                        frequently co-occur with with terms with higher scores
  -o FILE, --output=FILE
                        Write output to FILE. The script will write one term
                        per line
  -i FILE, --input=FILE
                        Read from FILE_PATH. The FILE_PATH is expected to
                        point to a director containing one sub-director per
                        collection. It assumes that each collection file
                        contains a header and on each line has: tweet id,
                        tweet text, tweet class (which needs to be among the
                        ones you set in the config.py file)

```

**Note:**
* If "--top_div" is set, the script constructs the co-occurance graph among discriminative terms and estimates the maximum weighted independent set on this graph, which is returned. To estimate this set we use a greedy that selects at each step the most discriminative terms and remove those that co-occur with them. If you are also interested in testing the heuristic based on identifying the minimum weighted coverage set check (Bar-Yehuda and Even 1985) or drop us an email. 
* We recommend to generate the lexicon based on more collections as the script favors terms that frequently appear in multiple collections (e.g., divide your data based on sub-topics).

Dependencies
------------
The scripts depend on the following external libraries (which you might consider installing in this order):
* [Scipy](http://www.scipy.org)
* [Numpy](http://www.numpy.org)
* [NLTK (including the data)](http://www.nltk.org)
* [scikit-learn](http://scikit-learn.org)
* [networkx](http://networkx.github.io)

Note that only Python 2.7 is supported.

Questions/inquiries
-------------------

[Olteanu et al. 2014]
Alexandra Olteanu, Carlos Castillo, Fernando Diaz, Sarah Vieweg:
"CrisisLex: A Lexicon for Collecting and Filtering Microblogged
Communications in Crises". ICWSM 2014.

For further inquiries, please contact:
 * [Alexandra Olteanu](mailto:alexandra.olteanu@epfl.ch)
 * [Carlos Castillo](mailto:chato@acm.org)
