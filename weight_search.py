"""Weighted search using TF-IDF weights."""
from collections import Counter
from utils import preprocess, print_results

import pickle


def get_search_results(query, index):
    """
    Search the query in the index provided.

    Args -
      query: Search query string.
      index: A dictionary of words as keys and doc_info as values.
    Return -
      ranked_docs: A list of tuples(doc_id, query word match frequency) that are ranked.
      doc_content: A dictionary of docs as keys and
    """
    ranking = Counter()
    doc_contents = dict()
    for word in query:
        if word in index:
            posting_list = index[word]
            ranking += Counter(posting_list)
            for each in posting_list:
                if each not in doc_contents:
                    doc_contents[each] = [word]
                else:
                    doc_contents[each].append(word)
    ranked_docs = ranking.most_common()
    return ranked_docs, doc_contents


def main():
    """Main."""
    weights = pickle.load(open('pickles/tf-idf.p', 'rb'))
    doc_names = pickle.load(open('pickles/tf-idf-file-names.p', 'rb'))

    search_string = raw_input("Enter the search string\n")
    stm_text = preprocess(search_string)
    ranked_docs, doc_contents = get_search_results(stm_text, weights)
    print_results(doc_names, ranked_docs, doc_contents)


if __name__ == "__main__":
    main()
