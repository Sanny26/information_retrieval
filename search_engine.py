#from weight_search import *

from search import *
from utils import *
from lexrank import *
import pdb

def print_file(name):
    print '> FILE NAME: {}'.format(name)

def print_summary(name):
    l = LexRank(name)
    summary = l.lex_rank()
    print '>', summary, '\n'

if __name__ == "__main__":
    weights = pickle.load(open('pickles/index.p', 'rb'))
    doc_names = pickle.load(open('pickles/file_names.p', 'rb'))

    search_string = raw_input("Enter the search string\n")
    stm_text = preprocess(search_string)
    ranked_docs, doc_contents = get_search_results(stm_text, weights)
    #pdb.set_trace()

    print get_header(len(ranked_docs))
    print "___"*48
    counter = 0
    for each in ranked_docs:
        name = doc_names[each[0]]
        if counter < 5:
            counter += 1
            print_file(name)
            print_summary(name)
        if counter == 5:
            print_file(name)
            print_summary(name)
            print ">Enter 'm' for more data."
            inp = raw_input()
            if inp == 'm':
                counter = 0
            else:
                break


    print "***"*48
