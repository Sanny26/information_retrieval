from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import os
import pdb
import re
import pickle

def get_header(result_len):
    return ">>\n>> Searching in the index table\n>> Search string found in {} documents.".format(result_len)

def print_line(doc_id, name):
    print("| {}.   {} |".format(doc_id, name))

def preprocess_file(f_path):
    """Parses the file to get text and preprocesses the text.
        Args - 
            f_path: Path of the file that is to be parsed.
        Return -
            stm_text: Parsed and processed text.
    """
    title = " \n "
    f_object = open(f_path,'r')
    content = f_object.read()
    parser = re.compile(r'(<TEXT>)(.*?)(</TEXT>)', re.S)
    text = parser.findall(content)[0][1].strip()
    parser = re.compile(r'(<TITLE>)(.*?)(</TITLE>)', re.S)
    if parser.findall(content):
        title += parser.findall(content)[0][1].strip()
    stm_text = preprocess(text+" "+title)
    return stm_text


def preprocess(text, position=False):
    """Tokenizes and stems the given text. 
        Args - 
            text:       Text to be processed.
            position:   Bool args to return positions of words in the original doc.
        Return -
            stm_text:   Parsed and processed text.
            text_pos:   Returns positions corresponding to stm_text.
    """
    tknzr = TweetTokenizer()
    tkn_text = tknzr.tokenize(text)
    
    stp_wrds = set(stopwords.words('english'))
    stp_text_pos = [(i,pos) for pos, i in enumerate(tkn_text) if i not in stp_wrds]
    if len(stp_text_pos)==0:
        return stp_text_pos 
    stp_text, text_pos = map(list, zip(*stp_text_pos))

    stemmer = PorterStemmer()
    stm_text = [stemmer.stem(word) for word in stp_text]
    
    if position:
        return stm_text, text_pos
    return stm_text


def print_more(prev_i, ranked_docs, doc_names, doc_contents):
    """Print more information or results based on a given command.
        Args - 
            prev_i:  
            ranked_docs: A list of tuples(doc_id, query word match frequency) that are ranked.
            doc_names:  Dictionary of <doc_ids, doc_names>.
            doc_contents: Dictionary of  <doc_id, query words ocurring in the doc>.
    """

    print( ">> To get more document results, print 'm'")
    print( ">> To get word occurences of a doc, enter its Id")
    command = raw_input()
    if command=="m":
       print( "___"*48)
       for i in range(prev_i, prev_i+5):
           print_line(i, doc_names[ranked_docs[i][0]])
       print( "___"*48)
       print_more(i, ranked_docs, doc_names, doc_contents)
    elif command.isdigit():
       ind = ranked_docs[int(command)][0]
       print( "___"*48)
       print( 'Words that appeared in doc', command, " :")
       print( ', '.join(doc_contents[ind]))
       print( "___"*48)
       print_more(prev_i, ranked_docs, doc_names, doc_contents)
    else:
       return 0

def print_results(doc_names, ranked_docs, doc_contents):
    """
    Prints search results.
        Args - 
            result_len: Conatains the length of the search result.
            doc_names:  Dictionary of <doc_ids, doc_names>.
            ranked_docs: A list of tuples(doc_id, query word match frequency) that are ranked.
            doc_contents: Dictionary of  <doc_id, query words ocurring in the doc>.
    """
    print( get_header(len(ranked_docs)) )
    print( "___"*48 )
    for i in range(0,5):
        print_line(i, doc_names[ranked_docs[i][0]])
    print( "___"*48 )
    prev_i = i
    print_more(prev_i, ranked_docs, doc_names, doc_contents)
