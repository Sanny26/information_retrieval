from collections import Counter
from math import log
from utils import preprocess_file
import os

import pickle

def get_tf_idf_weights(path):
    doc_no = 1
    doc_names = dict()
    tf_list = dict()    # how many term t occurs in doc d
    df_list = dict()   # how many docs contain term t
    sub_dirs = os.listdir(path)
    N = 0

    for dr in sub_dirs:
        dr_path = path+dr+"/"
        files = os.listdir(dr_path)
        for f in files:
            f_path = dr_path+f
            doc_names[doc_no] = f_path
            doc_no += 1
            
            processed_text = preprocess_file(f_path)
            tf = Counter(processed_text)
            for term, frequency in dict(tf).items():
                if term not in df_list.keys():
                    N += 1
                    df_list[term] = 1
                else:
                    df_list[term] += 1

                if frequency>0:
                    tf_list[term+"$"+str(doc_no)] = 1+log(frequency, 10)

    for key, val in tf_list.items():
        term = key.split('$')[0]

        tf_list[key] *= log(float(N)/df_list[term], 10)
    ###change tf_list stroge as doc_id and term sep
    return tf_list, doc_names



if __name__ == "__main__" :
	path = "/home/sanny/Documents/ir/en.docs.2011/en_BDNews24/"
	weights, doc_names = get_tf_idf_weights(path)

	pickle.dump(weights, open("pickles/tf-idf.p", "wb"))
	pickle.dump(doc_names, open("pickles/tf-idf-file-names.p", "wb"))