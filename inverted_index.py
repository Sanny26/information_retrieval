from utils import preprocess_file

import os
import pdb
import pickle


def  create_inverted_index(path):
    """
    Create an inverted index for all the files that occur in given 
    path's sub-directories.
        Args -
            path: String contaning directory path.
        Return - 
            index: Dictionary containing <words, posting lists>.
            index_freq: Dictionary containing <words, word corpusfrequency>.
            doc_names: Dictionary containing <doc_id, doc_name>. 
    """
    doc_no = 1
    index = dict()
    doc_names = dict()
    index_freq = dict() 

    sub_dirs = os.listdir(path)
    for dr in sub_dirs:
        dr_path = path+dr+"/"
        files = os.listdir(dr_path)
        for f in files:

            f_path = dr_path+f
            doc_names[doc_no] = f_path            
            processed_text = preprocess_file(f_path)            
            for word in processed_text:
                if word in index:
                   if doc_no not in index[word]:
                       index[word].append(doc_no)
                else:
                   index[word]=[doc_no]
            
            doc_no+=1

    for key in index:
        index_freq[key]=len(index[key])

    return index, index_freq, doc_names




if __name__ == "__main__":
    
    path = "/home/sanny/Documents/ir/en.docs.2011/en_BDNews24/"
    index, index_freq, doc_names = create_inverted_index(path)

    pickle.dump(index, open('index.p', 'wb'))
    pickle.dump(doc_names, open('file_names.p', 'wb'))
    pickle.dump(index_freq, open('doc_freq.p', 'wb'))
    print("Created inverted index successfully. \nData pickling done\n")
    pdb.set_trace()
