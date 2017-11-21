"""Main implementation of Page Rank algorithm."""

import numpy as np
import pdb


class PageRank():
    """Class for PageRank."""

    def __init__(self, num_pages, link_matrix=None, page_scores=None, page_ids=None, damping_factor=0.85):
        """Constructor."""
        self.num_pages = num_pages
        self.damping = damping_factor

        if link_matrix is None:
            self.link_matrix = np.zeros((self.num_pages, self.num_pages), dtype=np.float)
        else:
            self.link_matrix = link_matrix

        if page_scores is None:
            self.page_scores = np.ones((self.num_pages), dtype=float)/num_pages
        else:
            self.page_scores = page_scores

        if page_ids is None:
            self.pages = dict()
            for x in np.arange((self.num_pages)):
                self.pages[x] = x
        else:
            self.pages = page_ids

    def outgoing(self, pages):
        """Give the number of outgoing links from a page."""
        return np.array([len(self.link_matrix[self.pages[page], :].nonzero()[0]) for page in pages])

    def page_rank(self, page):
        """Calculate the page rank of a given page."""
        incoming_links = self.link_matrix[:, self.pages[page]].nonzero()[0]
        incoming_score = 0.0

        incoming_score = np.sum(self.page_scores[incoming_links]/self.outgoing(incoming_links))
        score = (1-self.damping) + self.damping*(incoming_score)

        return score

    def update_scores(self):
        """Update all the Page Ranks for all the pages."""
        new_scores = np.ones((self.num_pages), dtype=float)

        for page in self.pages:
            new_score = self.page_rank(page)
            new_scores[self.pages[page]] = new_score

        self.page_scores = new_scores

    def iterate(self, iterations):
        """Perform multiple iterations."""
        for i in range(iterations):
            self.update_scores()


if __name__ == "__main__":
    a = np.zeros((4, 4))
    a[0, 1] = 1
    a[0, 2] = 1
    a[1, 2] = 1
    a[2, 0] = 1
    a[3, 2] = 1

    PR = PageRank(4, a)
    PR.iterate(20)