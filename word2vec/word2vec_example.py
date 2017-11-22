"""Example for Word2Vec using the word2vec python library."""

import re
import word2vec


def clean_str(string):
    """Tokenization/string cleaning."""
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\"", " \" ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = re.sub(r"[.,#!$%&;:{}=_`\"~()/\\]", "", string)
    return string.strip().lower()


def clean_data(filepath, limit_dataset=100000):
    """Clean the data."""
    print("Cleaning the data and adding it to {}.cleaned".format(filepath))
    counter = 0
    out = open(filepath+".cleaned", "w")
    with open(filepath, "r") as f:
        for line in f:
            try:
                text = line.split('\t')[1]
            except IndexError:
                continue
            clean_text = " ".join([clean_str(x) for x in text.split()])
            out.write(clean_text + '\n')
            counter += 1

            if counter > limit_dataset:
                break

    out.close()


def gen_vectors(filepath, vec_size=100):
    """Generate word2vec."""
    word2vec.word2vec(filepath + ".cleaned", filepath + ".bin", size=vec_size, verbose=True)
    pass


def main(filepath, dataset=100000, vec_size=100):
    """Main."""
    clean_data(filepath, dataset)
    gen_vectors(filepath, vec_size)

    model = word2vec.load(filepath + ".bin")
    print("\nVocabulary      is:", model.vocab)
    print("\nWord vectors shape:", model.vectors.shape)
    print("\nWord vectors:\n", model.vectors)
    print("\nVector for 'music' is:\n", model['music'])


if __name__ == "__main__":
    main("conversations.out")
