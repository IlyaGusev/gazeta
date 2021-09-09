import argparse

from sklearn.feature_extraction.text import TfidfVectorizer

from util import spacy_deserialize, normalize


def build_idf_vocabulary(texts, max_df=0.2, min_df=5):
    texts = [" ".join(normalize(text)) for text in texts]

    print("Building TfidfVectorizer...")
    vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df)
    vectorizer.fit(texts)
    idf_vector = vectorizer.idf_.tolist()

    print("{} words in vocabulary".format(len(idf_vector)))
    idfs = list()
    for word, idx in vectorizer.vocabulary_.items():
        idfs.append((word, idf_vector[idx]))

    idfs.sort(key=lambda x: (x[1], x[0]))
    return idfs


def main(files, output_path):
    docs = []
    for f in files:
        docs += spacy_deserialize(f)
    idfs = build_idf_vocabulary(docs)
    print("Saving vocabulary with IDFs...")
    with open(output_path, "w") as w:
        for word, idf in idfs:
            w.write("{}\t{}\n".format(word, idf))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    parser.add_argument("--output-path", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
