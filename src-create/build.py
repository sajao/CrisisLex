# CrisisLex
# Author: Alexandra Olteanu
# Check LICENSE for details about copyright.

#TO-DO: further testing and code cleaning will be done

import nltk
import math
import os
import glob
import networkx as nx
from optparse import OptionParser
from nltk.stem.porter import PorterStemmer

import read
import config
import lexicon

# estimates the maximum weighted independent set formed by terms in the co-occurrence graph
def extract_max_weight_indep_terms_greedy(terms_weights, term_occ, freq, size, min_occ = 0.7):
    #build the occ_graph
    G = nx.Graph()
    l = len(terms_weights)
    term_weights = dict(terms_weights)

    # add nodes
    for t in term_weights:
        G.add_node(t, score = term_weights[t])

    # add edges
    terms = term_weights.keys()
    for i,t in enumerate(terms):
        if i == l-1:
            break
        for j in range(i+1,l):
            occ = float(term_occ.get((t,terms[j]),0)+term_occ.get((terms[j],t),0))
            try:
                edge_weight = occ/(freq[t]+freq[terms[j]]-occ)
            except:
                edge_weight = 0
            if edge_weight >= min_occ:
                G.add_edge(t,terms[j])

    indep = list()
    sorted_terms = sorted(term_weights, key=term_weights.get, reverse=True)
    while True:
        if len(sorted_terms)==0:
            break
        node = sorted_terms[0]
        indep.append(node)
        ng = G.neighbors(node)
        sorted_terms.remove(node)
        for n in ng:
            sorted_terms.remove(n)
            G.remove_node(n)
        G.remove_node(node)
    return set(indep[:size])

def get_aggregated_score(args):
    return (float(sum(args))/len(args)) * (1. / (1 + math.exp(-( float(len(args)) / 2 ))))

#term_fd is the hit ratio across datasets
def discriminative_coverage(term_weights, hit_ratio = None):
    weights = dict()

    i = len(term_weights)
    l = i

    sorted_terms = sorted(term_weights, key=term_weights.get, reverse=True)
    # discriminative sorting of quantiles
    for t in sorted_terms:
        weights[t] = float(i)/l
        i-=1
    if hit_ratio is None:
        return weights

    i=l
    sorted_terms = sorted(hit_ratio, key=hit_ratio.get, reverse=True)
    #normalized by hit-ratio based quantiles
    for t in sorted_terms:
        if t in term_weights:
            weights[t] *= float(i)/l
            i-=1

    return weights

#generates the lexicon
def get_raw_lexicon(collections, tweets_terms, word_set, tweets_cls, word_occ, fd, mean_function, discriminative_function, use_hit_ratio = False):
    occs, fd_all = dict(), nltk.FreqDist()
    term_weights = dict()
    if use_hit_ratio:
        hit_ratios = dict()

    for d in collections:
        lex = lexicon.Lexicon(tweets_terms[d], word_set[d], tweets_cls[d], [config.positive_class_label, config.negative_class_label], fd[d], config.positive_class_label, 20)
        w = discriminative_function(lex)
        for occ in word_occ[d]:
            occs[occ] = occs.get(occ,0)+word_occ[d][occ]
        for fr in fd[d]:
            fd_all[fr] = fd_all.get(fr,0)+fd[d][fr]
        for term in w:
            if term not in term_weights:
                term_weights[term] = []
            term_weights[term].append(w[term])
            if use_hit_ratio:
                if term not in hit_ratios:
                    hit_ratios[term] = []
                hit_ratios[term].append(float(lex.terms_frequency_per_class[lex.main_class][term])/lex.class_occ[lex.main_class])

    for term in term_weights:
        term_weights[term] = mean_function(term_weights[term])

    if use_hit_ratio:
        for term in term_weights:
            hit_ratios[term] = mean_function(hit_ratios[term])
        term_weights = discriminative_coverage(term_weights, hit_ratios)
    else:
        term_weights = discriminative_coverage(term_weights)

    return term_weights, occs, fd_all

# reverses the bigrams to their own most frequent form instead of reversing it each word frequent form
def reverse_stemmed_terms_set(stemmed_terms, reverse_stemming, reverse_bigrams_stemming):
    terms = []
    for w in stemmed_terms:
        ws = w.split()
        if len(ws)==2:
            if (ws[0],ws[1]) in reverse_bigrams_stemming:
                rev = reverse_bigrams_stemming[(ws[0],ws[1])]
                terms.append(rev[0]+' '+rev[1])
            else:
                exit("I can't reverse the bi-gram: The \"%s\" bi-gram was not stemmed"%w)
        else:
            if w in reverse_stemming:
                rev = reverse_stemming[w]
                terms.append(rev)
            else:
                exit("I can't reverse the uni-gram: The \"%s\" uni-gram was not stemmed"%w)
    return terms

# builds a map that reverse all the stemmed words to the most frequent form
def reverse_stemming(stem_map):
    rev_stemming = dict()
    for s in stem_map:
        max = 0
        aux = None
        for w in stem_map[s]:
            if max < stem_map[s][w]:
                max = stem_map[s][w]
                aux = w
        if aux is None:
            print "Generate map: The word was not stemmed", s
            print stem_map
            exit(0)
        rev_stemming[s] = aux
    return rev_stemming

def reverse_stemming_bigrams(stem_bigrams_map):
    return reverse_stemming(stem_bigrams_map)

# writes the lexicon to file
def save_lexicon(output, scored_terms, term_freq, stem, score):
    ps = PorterStemmer()
    f1 = open(output, "w")
    f2 = open(output[0:len(output)-len(output.split(".")[len(output.split("."))-1])-1]+"_with_scores_%s.txt"%score,"w")
    print "Saving the lexicon to file..."
    for i,t in enumerate(scored_terms):
        print>>f1,t[0]
        print>>f2,"%s,%s,%s"%(t[0],t[1],term_freq[stem[i]])
    print "The Lexicon is ready!"

if __name__ == "__main__":

    #command line options
    parser = OptionParser()
    parser.add_option("-s", "--terms_scoring", dest="test",
                  help="The statistical test used to score terms: pmi, chi2 or frequency (in the relevant documents)",
                  default = "pmi")
    parser.add_option("-r", "--hit_ratio", dest="hit_ratio",
                  help="It normalizes the crisis score according to the number of relevant tweets the term matches on.",
                  action="store_true", default = False)
    parser.add_option("-t","--top_div", dest="optimization",
                  help="It filters out the terms with lower crisis scores that frequently co-occur with with terms with higher scores",
                  action="store_true", default = False)
    parser.add_option("-o", "--output", dest="output",
                  help="Write output to FILE. The script will write one term per line",
                  metavar="FILE", default = "your_lexicon.csv")
    parser.add_option("-i", "--input", dest="input",
                  help="Read from FILE_PATH. The FILE_PATH is expected to point to a director containing one sub-director per collection. "
                       "It assumes that each collection file contains a header and on each line has: tweet id, tweet text, tweet class (which needs to be among the ones you set in the config.py file)",
                  metavar="FILE", default = "")

    (options, args) = parser.parse_args()

    tweets_cls = dict()
    tweets_terms = dict()
    wd_occ = dict()
    word_set = dict()
    fd = dict()
    stem_map, bigrams_map = dict(), dict()
    collections = set()

    #set discriminative functions
    scoring_options = {'pmi':lexicon.Lexicon.pmi_polarity_metric,'chi2':lexicon.Lexicon.chi2_metric,'frequency':lexicon.Lexicon.frequency_metric}
    try:
        discriminative_function = scoring_options[options.test]
    except:
        exit("The terms scoring parameter accepts only the following options: pmi, chi2, frequency")

    #extracts terms and computes statistics about them
    print "Extracting the data..."
    labeled_collections = glob.glob(options.input+"/*")
    for l in labeled_collections:
        if not os.path.isdir(l):
            continue
        collection_path = glob.glob(l+"/*")
        print collection_path
        for c in collection_path:
            print c
            labeled_data = open(c, "r")
            collections.add(c)
            tweets_cls[c], tweets_terms[c], wd_occ[c], word_set[c], fd[c] = read.get_terms(labeled_data, stem_map, bigrams_map)
    print "Done with reading..."

    term_weights, occs, fd_all = get_raw_lexicon(collections, tweets_terms, word_set, tweets_cls, wd_occ, fd, get_aggregated_score, discriminative_function, options.hit_ratio)
    if options.optimization:
        optimized_terms = extract_max_weight_indep_terms_greedy(term_weights,occs,fd_all,config.lexicon_size)
    else:
        optimized_terms = set()

    top_stemmed = [t for t in sorted(term_weights, key=term_weights.get, reverse=True) if ((not options.optimization) or (options.optimization and t in optimized_terms))][:config.lexicon_size]
    top = reverse_stemmed_terms_set(top_stemmed, reverse_stemming(stem_map), reverse_stemming_bigrams(bigrams_map))
    sorted_terms_weights = [(top[i],term_weights[t]) for (i,t) in enumerate(top_stemmed)]
    save_lexicon(options.output, sorted_terms_weights, fd_all, top_stemmed, options.test)