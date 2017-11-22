"""Page Rank for sample data available at http://amitavadas.com/PageRank/."""

from page_rank import PageRank
import numpy as np


def read_data(filepath):
    """Read data and create PageRank matrix."""
    page_links = list()
    page_dict = dict()

    with open(filepath, "r") as f:
        for i, line in enumerate(f):
            content = line.split()
            page_id = int(content.pop(0))
            page_dict[page_id] = i
            page_links.append([int(x) for x in content])

    page_matrix = np.zeros((len(page_links), len(page_links)), dtype=int)

    for i, page in enumerate(page_links):
        for links in page:
            page_matrix[i, page_dict[links]] = 1

    return page_dict, page_matrix


def main(filepath):
    """Main."""
    page_dict, page_matrix = read_data(filepath)
    PR = PageRank(len(page_dict), link_matrix=page_matrix, page_ids=page_dict)
    PR.iterate(10)
    scores = PR.page_scores
    scores = scores/scores.sum()

    page_dict = PR.pages
    page_numbers = dict([[v, k] for k, v in page_dict.items()])
    score_ids = np.argsort(scores)[::-1]

    print("Score\t\t\tPage ID")
    for score_id in score_ids:
        print("{}\t\t\t{}".format(scores[score_id], page_numbers[score_id]))


if __name__ == "__main__":
    main("data.txt")
