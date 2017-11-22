from collections import Counter
from utils import preprocess, preprocess_file
import operator
import math


def coeff_score(A, B, coeff='jacquard'):
    """
    Returns score for string A and B.
        Args - 
            A, B: Strings to compare.
            coeff: String containing score evaluating measure,
        Returns evaluated score.            
    """
    if coeff=='jacquard':
        A_set = set(A)
        B_set = set(B)
        numerator = len( A_set.intersection(B_set) )
        denominator = len( A_set.union(B_set) )
    elif coeff=='cosine':
        A_vec = Counter(A)
        B_vec = Counter(B)
        intersection = set(A_vec.keys()) & set(B_vec.keys())
        numerator = sum([A_vec[x] * B_vec[x] for x in intersection])

        A_sum = sum([A_vec[x]**2 for x in A_vec.keys()])
        B_sum = sum([B_vec[x]**2 for x in B_vec.keys()])
        denominator = math.sqrt(A_sum) * math.sqrt(B_sum)
    else:
        return "Coefficient not found"
    
    if denominator==0:
       return  0.0
    else:
       return float(numerator) / denominator


def evaluate_query(path, query, coeff):
    """
    Evaluates and searches for the query and returns ranked results.
        Args -
            path: String containing the directory path.
            query: Query string.
            coeff: String containing coefficient evaluation measure.
        Return - 
            ranked_list: Dictionary containing <doc_no, score>>
    """
    search = dict()
    doc_no = 1

    sub_dirs = os.listdir(path)
    for dr in sub_dirs:
        dr_path = path+dr+"/"
        files = os.listdir(dr_path)
        for f in files:
            f_path = dr_path+f
            doc_names[doc_no] = f_path
            processed_text = preprocess_file(f_path)
            processed_query = preprocess(query)
            search[doc_no] = coeff_score(processed_text, processed_query, coeff)
                    
            if doc_no==10000:
               break
            doc_no+=1
    ranked_list = sorted(search.items(), key=operator.itemgetter(1))
    return dict(ranked_list)


if __name__ == "__main__" :
    
    query = raw_input("Enter query\n")
    coeff = raw_input("Enter 'a' for Jacquard coefficient based results and 'b' for cosine similarity based scores\n")
    if coeff=='a':
        coeff='jacquard'
    elif coeff=='b':
        coeff='cosine'

    path = "/home/sanny/Documents/ir/en.docs.2011/en_BDNews24/"
    ranked_list = evaluate_query(path, query, coeff)
    
    
