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

def preprocess_file(f_path, position = False):
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
    if position is True:
        return preprocess(text+" "+title, position)
    return preprocess(text+" "+title)


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
    stp_text = [i for i in tkn_text if i not in stp_wrds]
    if len(stp_text)==0:
        return stp_text

    text_pos = [pos for pos, i in enumerate(stp_text)] 
    #stp_text, text_pos = map(list, zip(*stp_text_pos))

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

def print_docs_only(prev_i, ranked_docs, doc_names):
    """Print more information or results based on a given command.
        Args - 
            prev_i:  
            ranked_docs: A list of tuples(doc_id, query word match frequency) that are ranked.
            doc_names:  Dictionary of <doc_ids, doc_names>.
    """

    print( ">> To get more document results, print 'm'")
    command = raw_input()
    if command=="m":
        print( "___"*48)
        for i in range(prev_i, min(len(ranked_docs), prev_i+5)):
            print_line(i, doc_names[ranked_docs[i][0]])
        print( "___"*48)
        print_docs_only(i, ranked_docs, doc_names)
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
    i = 0
    for i in range(0,min(len(ranked_docs), 5)):
        print_line(i, doc_names[ranked_docs[i][0]])
    
    prev_i = i
    if (prev_i+1) >= len(ranked_docs):
        print('==='*48)
    else:
        print( "___"*48 )
        if len(doc_contents)!=0:
            print_more(prev_i, ranked_docs, doc_names, doc_contents)
        else:
            print_docs_only(prev_i, ranked_docs, doc_names)
