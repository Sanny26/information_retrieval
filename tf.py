"""Main code for finding TF-IDF scores."""
from collections import Counter
from math import log
from utils import preprocess_file
import os
import numpy as np
import pickle


def get_tf_idf_weights(path):
    """Get the wieghts for TF."""
    doc_no = 0
    doc_names = dict()
    tf_list = dict()    # how many term t occurs in doc d
    df_list = dict()   # how many docs contain term t
    sub_dirs = os.listdir(path)
    term_list = []
    N = 0

    for dr in sub_dirs:
        dr_path = path + dr + "/"
        files = os.listdir(dr_path)
        for f in files:
            f_path = dr_path+f
            doc_names[doc_no] = f_path
            doc_no += 1
            print(doc_no)

            processed_text = preprocess_file(f_path)
            tf = Counter(processed_text)
            for term, frequency in dict(tf).items():
                if term not in tf_list:
                    tf_list[term] = []
                    term_list.append(term)
                tf_list[term].append((doc_no, 1+log(frequency, 10)))

    matrix = np.zeros((len(tf_list), doc_no+1), dtype=float)

    for i, term in enumerate(list((tf_list.keys()))):
        l = tf_list[term]
        for doc_id, freq in l:
            matrix[i, doc_id] = freq

    return matrix, doc_names, term_list


def main():
    """Main."""
    path = "test/"
    weights, doc_names, terms = get_tf_idf_weights(path)

    pickle.dump(weights, open("pickles/tf.p", "wb"))
    pickle.dump(doc_names, open("pickles/tf-file-names.p", "wb"))
    pickle.dump(terms, open("pickles/tf-terms.p", "wb"))


if __name__ == "__main__":
    main()
