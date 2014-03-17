==========================================================================
Contents of this directory
==========================================================================

This directory contains tweets labeled by crowdsourcing workers. Each tweet
is accompanied by a label, which is the result of the majority voting among
at least 3 crowdsourcing workers.

There is one sub-directory per crisis, for each of the following disasters:

- Sandy Hurricane 2012
  https://en.wikipedia.org/wiki/Hurricane_Sandy
- Oklahoma Tornado Season 2013
  https://en.wikipedia.org/wiki/2013_Moore_tornado
- West Texas Explosion 2013
  https://en.wikipedia.org/wiki/West_Fertilizer_Company_explosion
- Alberta Floods 2013
  https://en.wikipedia.org/wiki/2013_Alberta_floods
- Boston Bombings 2013
  https://en.wikipedia.org/wiki/Boston_Marathon_bombings
- Queensland Floods 2013
  https://en.wikipedia.org/wiki/January_2013_Eastern_Australia_floods

==========================================================================
On-topic/Off-topic files: *-ontopic_offtopic.csv
==========================================================================

CONTENTS:
Each file contains approximately 10,000 tweets. 50% of these tweets were
sampled from the geo-based sample, and 50% from the keywords-based sample.
These two samples are described in [Olteanu et al. 2014].

LABELS:
These files contain labels indicating if a tweet is on-topic (related to
the crisis at hand), or off-topic (not related to it).

FILE FORMAT:
One tweet per line with the following comma-separated fields:
tweet id, tweet text, label

==========================================================================
If you have questions about these files
==========================================================================

[Olteanu et al. 2014]
Alexandra Olteanu, Carlos Castillo, Fernando Diaz, Sarah Vieweg:
"CrisisLex: A Lexicon for Collecting and Filtering Microblogged
Communications in Crises". ICWSM 2014.

For further inquiries, please contact:
 - Alexandra Olteanu <alexandra.olteanu@epfl.ch>
 - Carlos Castillo <chato@acm.org>

