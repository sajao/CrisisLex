Contents of this directory
==========================
(Work-in-Progress) The director contains scripts that allows anyone to easily collect tweets using CrisisLex. This can be done in two ways:

Simple data collection
----------------------
Collects tweets containing the lexicon terms.

**Parameters**
  -h, --help            show this help message and exit
  -l FILE, --lexicon=FILE
                        Read lexicon from file. Expects one term per line.
  -t FILE, --optional_terms=FILE
                        Read user defined terms from file. Expects one term
                        per line.
  -o FILE, --output=FILE
                        Write output to FILE. The expected format is .json

Adaptive data collection
------------------------
Collects tweets containing the lexicon terms for a while, identifies new terms that describe the most prominent crisis 

**Parameters**


Requirements
------------
 * Only Python 2.7 is supported
 * The adaptive data collector depends on the following external libraries:
    * [Scipy](http://www.scipy.org)
    * [Numpy](http://www.numpy.org)
    * [NLTK (including the data)](http://www.nltk.org)
    * [scikit-learn](http://scikit-learn.org)

Questions/inquiries
-------------------

[Olteanu et al. 2014]
Alexandra Olteanu, Carlos Castillo, Fernando Diaz, Sarah Vieweg:
"CrisisLex: A Lexicon for Collecting and Filtering Microblogged
Communications in Crises". ICWSM 2014.

For further inquiries, please contact:
 * [Alexandra Olteanu](mailto:alexandra.olteanu@epfl.ch)
 * [Carlos Castillo](mailto:chato@acm.org)