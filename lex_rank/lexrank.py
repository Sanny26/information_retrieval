"""Lex Rank."""
from lex_rank_utils import LexRankCompute
from utils import preprocess
import itertools
import numpy as np
import math


def cosine(A, B):
    """Cosine Similarity."""
    A = np.array(A)
    B = np.array(B)
    dot = (A*B).sum()
    mod_A = math.sqrt((A * A).sum())
    mod_B = math.sqrt((B * B).sum())

    return dot/(mod_A * mod_B)


class LexRank():
    """Class for Lex Rank."""

    def __init__(self, name):
        """Init."""
        self.content = open(name, 'r').read().split('.')
        self.sent = dict()

    def lex_rank(self):
        """Do LexRank."""
        tokens_sent = list()
        raw_sent = dict()
        for i, each in enumerate(self.content):
            sent = preprocess(each)
            tokens_sent.append(sent)
            raw_sent[i] = each

        all_tokens = itertools.chain.from_iterable(tokens_sent)
        word_to_id = {token: idx for idx, token in enumerate(set(all_tokens))}

        tokens_ids = []
        for sent in tokens_sent:
            vec = [0 for i in range(len(word_to_id))]
            for tok in sent:
                vec[word_to_id[tok]] = 1
            tokens_ids.append(vec)

        lmatrix = np.zeros((len(tokens_ids), len(tokens_ids)), dtype=np.float)

        for i in range(len(tokens_ids)):
            for j in range(len(tokens_ids)):
                sent1 = tokens_ids[i]
                sent2 = tokens_ids[j]
                if i != j:
                    lmatrix[i][j] = cosine(sent1, sent2)

        P = LexRankCompute(lmatrix.shape[0], lmatrix)
        P.iterate(1)


        sorte = [i[0] for i in sorted(enumerate(P.page_scores), key=lambda x:x[1], reverse=True)]
        print(P.page_scores, sorte)

        text = raw_sent[sorte[0]].strip() + raw_sent[sorte[1]].strip() + '\n'

        return text


if __name__ == "__main__":
    l = LexRank('text.txt')
    summary = l.lex_rank()
    print(summary)
