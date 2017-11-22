from nltk import word_tokenize, bigrams
from collections import Counter
from math import floor

import os
import pdb
import io
import pickle

counter = dict()
top_k_val = 100

def get_ngrams(text, n=2):
    words = word_tokenize(text)
    ngrams = list()
    for each in words:
        for i in range(len(each)-n):
            ngrams.append(each[i:i+n])

    return Counter(ngrams)


def get_file_lprofile(fname):
    counter = Counter([])

    with io.open(fname, 'r', encoding='utf8') as f:
        for line in f:
            counter += get_ngrams(line)
            
    return counter

def dump_lprofiles():
    global counter

    l_profiles = dict()
    for i in range(32):
        l_profiles[i] = [each[0] for each in counter[i].most_common(top_k_val)]

    pickle.dump(l_profiles, open('lprofiles.txt', 'wb'))
        

if __name__ =='__main__':

    dr_path = "DLI32/"
    files = os.listdir(dr_path)

    for name in files:
        lan_id = int(name.split('.')[0])
        if lan_id%10 == 0:
           label = floor(lan_id/10) -1;
        else:
           label = floor(lan_id/10)    
        
        fcounter = get_file_lprofile(dr_path+name)
        if label in counter.keys():
            counter[label] += fcounter
        else:
            counter[label] = fcounter

    dump_lprofiles()

    



        

    
    
