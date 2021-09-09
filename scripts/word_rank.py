import argparse
from collections import Counter

from tqdm import tqdm

from util import normalize, spacy_deserialize


def calc_word_rank(docs):
    cnt = Counter()
    for doc in tqdm(docs):
        cnt.update(normalize(doc))
    words = []
    for word, _ in cnt.most_common():
        words.append(word)
    return words


def main(files, output_path):
    docs = []
    for f in files:
        docs += spacy_deserialize(f)
    words = calc_word_rank(docs)
    with open(output_path, "w") as w:
        for word in words:
            w.write(word.strip() + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    parser.add_argument("--output-path", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
