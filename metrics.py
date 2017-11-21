import numpy as np
from nltk import word_tokenize
import pdb


def lcs(xstr, ystr):
    if not xstr or not ystr:
        return ""
    x, xs, y, ys = xstr[0], xstr[1:], ystr[0], ystr[1:]
    if x == y:
        return x + lcs(xs, ys)
    else:
        return max(lcs(xstr, ys), lcs(xs, ystr), key=len)

def get_ngrams(text, n=2):
    words = word_tokenize(text)
    ngrams = list()
    for i in range(len(words)):
    	if i+n < len(words):
    		ngrams.append(tuple(words[i:i+n]))
    return ngrams

###--------------------------------Metric Functions----------------------------------------------

def rouge_n(ref_summary, pred_summary):
	##Input params have to be list of summaries 
	if len(ref_summary) != len(pred_summary):
		print('Insufficent data')
		return
	count1 = count2 = 0
	for i in range(len(ref_summary)):
		N1 = get_ngrams(ref_summary[i])
		N2 = get_ngrams(pred_summary[i])
		count1 += len(set(N1).intersection(set(N2)))
		count2 += len(N1)

	rouge_val = count1/ float(count2)
	return rouge_val

def rouge_lcs(ref_summary, pred_summary):
	##Input params are a single test case
	ref_sent = ref_summary.split('.')
	pred_sent = pred_summary.split('.')
	r_lcs = p_lcs = 0
	for sent in ref_sent:
		union_lcs = ""
		for sent2 in pred_sent:
			union_lcs += lcs(sent, sent2)
		union_lcs = set(union_lcs.strip().split(' '))
		r_lcs += len(union_lcs)
		p_lcs += len(union_lcs)


	r_lcs /= float(len(ref_summary.split(' ')))
	p_lcs /= float(len(pred_summary.split(' ')))

	beta = p_lcs / (r_lcs + 1e-12)
	num = (1 + (beta**2)) * r_lcs * p_lcs
	denom = r_lcs + ((beta**2) * p_lcs)
	f_lcs = num / (denom + 1e-12)
	
	return f_lcs

def recall(rel_doc_list, ret_doc_list):
	A_set = set(rel_doc_id)
	B_set = set(ret_doc_list)
	AiB = len(A_set.intersection(B_set))
	return float(AiB)/len(A_set)

def precision(rel_doc_list, ret_doc_list):
	A_set = set(rel_doc_list)
	B_set = set(ret_doc_list)
	AiB = len(A_set.intersection(B_set))
	return float(AiB)/len(B_set)

def f_score(precision ,recall , alpha=0.5):
	a = float(alpha* precision)
	b = float((1-alpha)*recall)
	return 2/(1/a+1/b)

def avg_precision(comp_list):
	precision = []
	correct = 0
	for i in range(len(comp_list)):
		if comp_list[i]:
			correct += 1
			precision.append(correct/float(i+1))
		else:
			precision.append(0)

	return np.mean(precision)

def MAP(queries, rel_doc_id, retrieved_doc):
	result = 0
	for i,query in enumerate(queries):
		result += avg_precision(np.array(rel_doc_id[i]) == np.array(retrieved_doc[i]))
	return result/ float(len(queries))

	
if __name__ == "__main__" :
	print MAP([1,2], [[1, 2, 3, 4, 5],[6, 7, 8, 9, 10]], [[1, 6, 7, 4, 5], [6, 7, 8, 9, 10]])
        pdb.set_trace()
