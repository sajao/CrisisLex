Contents of this directory
==========================

This directory contains information about events that produced coverage spikes on Twitter, on mainstream media ([GDELT](http://gdeltproject.org)), or both. It also includes a list of keywords (for Twitter) and a list of themes/taxonomies (for GDELT)

Events list file: 'covered_climate_events.csv'
----------------------------------------------

**Contents:** This file contains information about 350 events that received medium to high coverage in Twitter, mainstream media, or both, covering a period of 17 months in 2013 and 2014, and labeled by relevance to climate-change, triggers, actions, and 6 news values (i.e. extraordinary, unpredictable, high magnitude, negative, conflictive, and related to elite persons). Each label is the result of the majority voting among at least 5 crowdsourcing workers (3 crowdsourcing workers for the easier task of false positives removal).

**Data Format:** One event per line with the following 16 comma-separated fields: *Media, Event, Peak Days, Sample URLs, Relatedness (crowd), Relatedness (authors), Primary Type (or trigger), Primary Sub-type (or action), Secondary Type (or trigger), Secondary Sub-type (or action), Negativity, Magnitude, Predictability, Elite persons, Conflict, Unexpectedness*

**Labels:**
The file contains the following elements for each event:

 - *Media:* News or Twitter
 - *Event:* the event name in the form of a headline
 - *Peak Days:* the days in which a coverage spike was detected in the respective media
 - *Sample URLs:* URLs of articles or tweets about the event
 - *Relatedness (crowd):* related to climate change, weakly related to climate change, not related to climate change
 - *Relatedness (authors):* yes (related to climate change), borderline (weakly related to climate change), no (not related to climate change)
 - *Primary/Secondary Type (or trigger):* disaster, for-profit (excl. media), govt (exec & legislative), individuals, media, NGOs/groups of people
 - *Primary/Secondary Sub-type (or action):* natural hazards, human-induced hazards, legal actions, meetings/conferences, generic (campaigns/statements/other), publication/studies/research
 - *Negativity:* this is good news, this is neither good nor bad news, this is bad news
 - *Magnitude:* the magnitude of this event is high, the magnitude of this event is moderate, the magnitude of this event is low
 - *Predictability:* a member of the public could not have know this will happen;
a member of the public could have know this will happen
 - *Elite persons:* this involves someone rich, powerful, or famous; this does not involve someone rich, powerful, or famous
 - *Conflict:* this depicts a conflict between two opposing persons/groups, 
this does not depict a conflict between two opposing persons/groups
 - *Unexpectedness:* this is an ordinary event, this is an extraordinary event
 
A description of the instructions given to crowdsourced workers in the news values annotation task can be found in the 'news_values_annotation_tasks_summary.txt'.

Twitter keywords file 'twitter_climate_keywords.txt'
--------------------------------------------
**Contents:** This file contains a list of climate-change related keywords. 

**Data Format:** plain text with one keyword per line (this format is also compatible with the one required by our collection scripts).

GDELT Themes/Taxonomies file 'gdelt_climate_themes.txt'
----------------------------------------------
**Contents:** This file contains a list of climate-change related themes/taxonomies. 

**Data Format:** plain text with one [GDELT](http://gdeltproject.org) theme/taxonomy per line. The initial/bootstrap theme, the themes list and taxonomies list are marked by a line starting with "#".

Crowdsourcing examples file 'news_values_annotation_tasks_summary.txt'
----------------------------------------------
**Contents:** This file contains example instructions and of correctly annotated events. 

**Data Format:** plain text.

Reference
---------
[Olteanu et al. 2015] Alexandra Olteanu, Carlos Castillo, Nicholas Diakopoulos, Karl Aberer. 2015. Comparing Events Coverage in Online News and Social Media: The Case of Climate Change. In Proceedings of the AAAI Conference on Web and Social Media (ICWSM'15). AAAI Press, Oxford, UK.

Questions/inquiries
-------------------
For inquiries please contact [Alexandra Olteanu](mailto:alexandra.olteanu@epfl.ch), or Carlos Castillo, or Nicholas Diakopoulos, or Karl Aberer.
 
Version history
---------------

 * 2015-04-06: v1.0, initial release.
