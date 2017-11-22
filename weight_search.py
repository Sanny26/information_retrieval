"""Weighted search using TF-IDF weights."""
from collections import Counter
from utils import preprocess, print_results

import pickle


def get_search_results(query, matrix, terms, docs):
    """
    Search the query in the index provided.

    Args -
      query: Search query string.
      index: A dictionary of words as keys and doc_info as values.
    Return -
      ranked_docs: A list of tuples(doc_id, query word match frequency) that are ranked.
      doc_content: A dictionary of docs as keys and
    """
    result = set(docs.keys())
    for word in query:
        term_index = terms.index(word)
        tf = matrix[term_index]
        indices = set((tf > 0).nonzero()[0])
        result = result.intersection(indices)

    return list(result)


def main(TF=False):
    """Main."""
    if TF:
        weights = pickle.load(open('pickles/tf.p', 'rb'))
        doc_names = pickle.load(open('pickles/tf-file-names.p', 'rb'))
        terms = pickle.load(open("pickles/tf-terms.p", "rb"))
        search_string = raw_input("Enter the search string\n")

        stm_text = preprocess(search_string)
        ranked_docs = get_search_results(stm_text, weights, terms, doc_names)
        for line in ranked_docs:
            print("Doc: {}".format(doc_names[line]))
    else:
        weights = pickle.load(open('pickles/tf-idf.p', 'rb'))
        doc_names = pickle.load(open('pickles/tf-idf-file-names.p', 'rb'))
        terms = pickle.load(open("pickles/tf-idf-terms.p", "rb"))

        search_string = raw_input("Enter the search string\n")
        stm_text = preprocess(search_string)
        ranked_docs = get_search_results(stm_text, weights, terms, doc_names)
        for line in ranked_docs:
            print("Doc: {}".format(doc_names[line]))

if __name__ == "__main__":
    main(TF=True)
    main()
