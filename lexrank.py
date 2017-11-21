from pagerank import PageRank 
from utils import preprocess
import itertools
import numpy as np
from jac import coeff_score
import pdb

class LexRank():
    def __init__(self, name):
        self.content = open(name, 'r').read().split('.')
        self.sent = dict()

    def get_text(self):

    	tokens_sent = list()
        raw_sent = dict()
        for i, each in enumerate(self.content):
            sent = preprocess(each)
            tokens_sent.append( sent )
            raw_sent[i] = each

        all_tokens = itertools.chain.from_iterable(tokens_sent)
        word_to_id = {token: idx for idx, token in enumerate(set(all_tokens))}

        tokens_ids = []
        for sent in tokens_sent:
            vec = [0 for i in range(len(word_to_id))]
            for tok in sent:
                vec[word_to_id[tok]] += 1
            tokens_ids.append(vec)

        lmatrix = np.zeros((len(tokens_ids), len(tokens_ids)), dtype=np.float)
        
        for i in range(len(tokens_ids)):
        	for j in range(len(tokens_ids)):
        		sent1 = tokens_ids[i]
        		sent2 = tokens_ids[j]
        		if i!=j:
        			lmatrix[i][j] = coeff_score(sent1, sent2, 'cosine')

        P = PageRank(lmatrix.shape[0], lmatrix)
        P.iterate(10)

        sent_threshold = 2
        sorte = [i[0] for i in sorted(enumerate(P.page_scores), key=lambda x:x[1], reverse = True)]

        text = raw_sent[sorte[0]].strip() + raw_sent[sorte[1]].strip() + '\n'

        return text





l = LexRank('/home/sanny/Documents/ir/test/text.txt')
summary = l.get_text()
print summary


