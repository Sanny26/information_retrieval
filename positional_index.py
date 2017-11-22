from utils import preprocess_file

import os
import pdb
import pickle

def create_positional_index(path):
    """
    Creates a positional index for all the files in the path's sub-directories.
        Args -
            path: String contaning directory path.
        Return -
            index: Dictionary containing <word, (<doc_id, [positions]>
                                                 <'doc_freq', integer> )>
            doc_names: Dictionary containing <doc_id, doc_name>.
    """
    doc_no = 1
    index = dict()
    doc_names = dict()

    sub_dirs = os.listdir(path)
    for dr in sub_dirs:
        dr_path = path+dr+"/"
        files = os.listdir(dr_path)
        for f in files:
            f_path = dr_path+f
            doc_names[doc_no] = f_path
            
            processed_text, positions = preprocess_file(f_path, position=True)
            
            for lis_indx, word in enumerate(processed_text):
                if word not in index:
                    index[word] = dict()

                if word in index:
                   if doc_no not in index[word]:
                       index[word][doc_no]=[positions[lis_indx]]
                   else:
                       index[word][doc_no].append(positions[lis_indx])

            if doc_no==10000:
               break
            doc_no+=1

    for key in index:
        index[key]['doc_freq']=len(index[key])

    return index, doc_names



if __name__ == "__main__" :
 
    path = "data/"
    index, doc_names = create_positional_index(path)

    pickle.dump(index, open('pickles/pos_index.p', 'wb'))
    pickle.dump(doc_names, open('pickles/pos_file_names.p', 'wb'))

    # doc_names = pickle.load(open('file_names.p', 'rb'))
    # index = pickle.load(open('index.p', 'rb'))
    # doc_freq = pickle.load(open('doc_freq.p', 'rb'))
    # doc_no = max(doc_names.keys())+1

    pdb.set_trace()
