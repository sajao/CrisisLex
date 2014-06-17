# CrisisLex
# Author: Alexandra Olteanu
# Check LICENSE for details about copyright.

import nltk
import math

class Lexicon:
    def __init__(self, documents, terms, classes, class_types, frequency, main_class, min_docs):
        self.terms = terms  # the terms used to build the lexicon
        self.documents = documents
        self.classes = classes
        self.terms_frequency = frequency
        self.terms_frequency_per_class = dict()
        self.main_class = main_class
        # the minimum support for a term (i.e., number of documents in the class of interest in order to be considered)
        self.min_docs = min_docs
        self.class_occ = dict()
        for c in class_types:
            self.terms_frequency_per_class[c]=nltk.FreqDist()
            self.class_occ[c] = classes.count(c)
        for i, doc in enumerate(self.documents):
            cls = self.classes[i]
            for t in doc:
                self.terms_frequency_per_class[cls].inc(t)

    # the scoring functions return the list of discriminative terms for the class of interest according to each metric
    def pmi_polarity_metric(self, thr = None):
        terms = {}
        for t in self.terms:
            fr = self.terms_frequency_per_class[self.main_class][t]
            if fr<= self.min_docs:
                continue
            try:
                # tweets that contain t and are in the class
                n11 = self.terms_frequency_per_class[self.main_class][t]
                # tweets that contain t and are not in the class; we add 1 to ensure that pmi never defaults to inf
                n01 = self.terms_frequency[t] - n11 +1
                if n11 == 0:
                    pmi = 0
                else:
                    if n01 == 0:
                        pmi = 100
                    else:
                        pmi = math.log((float(n11)/self.class_occ[self.main_class])/(float(n01)/(len(self.documents)-self.class_occ[self.main_class])))
                        if pmi<0:
                            pmi = 0
            except:
                print "I can't compute the crisis score. Do you have enough training data?"
            if thr is None:
                terms[t] = pmi
            else:
                if pmi>=thr:
                    terms[t] = pmi
        return terms

    def chi2_metric(self, thr = None):
        terms = {}
        n = len(self.documents)
        for t in self.terms:
            fr = self.terms_frequency_per_class[self.main_class][t]
            if fr<= self.min_docs:
                continue
            try:
                n11 = self.terms_frequency_per_class[self.main_class][t] # tweets that contain t and are in the class
                n01 = self.terms_frequency[t] - n11 # tweets that contain t and are not in the class
                n10 = self.class_occ[self.main_class] - n11 # tweets that do not contain t and are in the class
                n00 = (n - self.class_occ[self.main_class]) - n01
                p_t_pos = float(n11)/self.class_occ[self.main_class]
                p_t_neg = float(n01)/(len(self.documents)-self.class_occ[self.main_class])

                try:
                    chi2 = (n*(n11*n00-n10*n01)*(n11*n00-n10*n01))/((n11+n01)*(n11+n10)*(n10+n00)*(n01+n00))
                except:
                    chi2 = 0
                if p_t_pos<p_t_neg:
                    chi2 = -chi2

                if thr is None:
                    terms[t] = chi2
                else:
                    if chi2>=thr:
                        terms[t] = chi2
            except:
                print "I can't compute the crisis score. Do you have enough training data?"
        return terms

    def frequency_metric(self, thr = None):
        terms = {}
        for t in self.terms:
            fr = self.terms_frequency_per_class[self.main_class][t]
            if fr >=self.min_docs:
                try:
                    p = float(fr)/self.class_occ[self.main_class]
                except:
                    print "I can't compute the crisis score. Do you have enough training data?"

                if thr is None:
                    terms[t] = p
                else:
                    if p>=thr:
                        terms[t] = p
        return terms