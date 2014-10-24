Contents of this directory
==========================
This directory contains tweets posted during **2013 Singapore haze** organized in two comma-separated values (.csv) files containing tweet-ids for all the tweets filtered for this event, plus the text of the tweets and labels only for the labeled ones. The directory also contains a file with details about the event.

Event description file '*-event_description.json'
-------------------------------------------------
**Contents:** This file contains location and temporal details about the event, along with a brief categorization, collection size, and the list of keywords used for filtering.

**Data Format:** JSON (check file)

**Top-level fields:** name, time, location, categorization, keywords, size

Labeled tweets file '*-tweets_labeled.csv'
------------------------------------------
**Contents:** This file contains slightly above 1000 tweets labeled by crowdsourcing workers according to *informativeness* (as informative, or not informative), *information type*, and *source*. Each tweet is accompanied by three labels, each being the result of the majority voting among at least 3 crowdsourcing workers.

**Data Format:** One tweet per line with the following comma-separated fields:
*Tweet ID, Tweet Text, Information Source, Information Type, Informativeness*

**Labels:**
The file contains labels provided by crowdsource workers, indicating if the tweet is:

 - *Informativeness:* Related and informative, Related - but not informative, Not related, Not applicable
 - *Information source:* Eyewitness, Government, NGOs, Business, Media, Outsiders, Not applicable
 - *Information type:* Affected individuals, Infrastructure and utilities, Donations and volunteering, Caution and advice, Sympathy and support, Other Useful Information, Not applicable

A description of the labeling process can be found in the reference below.

Tweet ids file '*-tweetids_entire_period'
-----------------------------------------
**Contents:** This file contains a list of tweet-ids for all the tweets filtered for this event.

**Data Format:** One tweet per line with the following comma-separated fields:
  *Timestamp, Tweet-ID, Included*

**"Included" field:**
The "Included" file indicates if the tweet was included in the period we analyzed (Y) or not (N). The inclusion/exclusion rule is based on frequency over time as detailed in the reference below.

Reference
---------
[Olteanu et al. 2015] A. Olteanu, S. Vieweg, C. Castillo. 2015. What to Expect When the Unexpected Happens: Social Media Communications Across Crises. In Proceedings of the ACM 2015 Conference on Computer Supported Cooperative Work and Social Computing (CSCW '15). ACM, Vancouver, BC, Canada.

Questions/inquiries
-------------------
For inquiries please contact [Alexandra Olteanu](mailto:alexandra.olteanu@epfl.ch), or Sarah Vieweg, or Carlos Castillo.
 
