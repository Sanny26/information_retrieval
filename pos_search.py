from utils import preprocess

import pickle
import pdb

def position_merge(positions):
    """
    Calculates if positions are mergeable.
      Args -
          positions: List of lists contaning all positions of word in a document. 
      Returns -
          results: List of starting positions for all groups that are mergeable.
    """
    result = positions[0]
    for avl_pos in positions[1:]:
        required_pos = [x+1 for x in result]
        result = set(required_pos).intersection(set(avl_pos))
    result = [x+1-len(positions) for x in result]
    return result



def get_search_results(query):
    """
    Searches for the query in the positional index.
      Args -
          query: List of processed words
      Return -
          ranked: List of (doc_id, start_position) for the query.
    """
    result = list()
    doc_list = set(doc_names.keys())
    for word in query:
        if word in index:
          doc_list = doc_list.intersection(index[word].keys())
    
    for doc_id in doc_list:
        positions = list()
        for word in query:
            positions.append(index[word][doc_id])
        doc_result = [(doc_id, x) for x in position_merge(positions)]
        result += doc_result
    ranked = sorted(result, key= lambda x: (x[0], x[1]))
    return ranked



if __name__ == "__main__" :
    index = pickle.load(open('pickles/pos_index.p','rb'))
    doc_names = pickle.load(open('pickles/file_names.p', 'rb'))  

    search_string = raw_input("Enter the search string\n")
    stm_text = preprocess(search_string)
    ranked_docs = get_search_results(stm_text)
