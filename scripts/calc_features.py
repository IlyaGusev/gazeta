import argparse
from functools import lru_cache

import spacy
import numpy as np
from nltk import edit_distance
from datasets import load_dataset
from tqdm import tqdm
from scipy import sparse
from scipy.sparse.csgraph import maximum_bipartite_matching

from util import spacy_deserialize, write_jsonl, normalize


class TextSummaryScorer:
    def __init__(self, word_rank_file, idfs_file):
        self.word2rank = dict()
        with open(word_rank_file) as r:
            for i, word in enumerate(r):
                self.word2rank[word.strip()] = i
        self.idfs = dict()
        with open(idfs_file) as r:
            for line in r:
                word, score = line.strip().split("\t")
                self.idfs[word] = score
        self.pipiline = {
            "LevSim": self.levenshtein_similarity,
            "NbChars": self.char_ratio,
            "WordRank": self.word_rank_ratio,
        }
        self.bad_pos_tags = ("PUNCT", "CCONJ", "ADP", "PART", "SCONJ", "PRON", "ADV", "DET", "SYM", "NUM")

    def __call__(self, text, summary):
        values = dict()
        for name, action in self.pipiline.items():
            values[name] = action(text, summary)
        return values

    @staticmethod
    def levenshtein_similarity(text, summary):
        text = str(text)
        summary = str(summary)
        text = text[:len(summary)].lower()
        summary = summary.lower()
        return edit_distance(text, summary) / len(summary)

    @staticmethod
    def char_ratio(text, summary):
        text = str(text)
        summary = str(summary)
        return (len(summary) / len(text)) if len(text) != 0.0 else 0.0

    def word_rank_ratio(self, text, summary):
        summary_score = self._word_rank_score(summary)
        text_score = self._word_rank_score(text)
        return summary_score / text_score if text_score != 0.0 else 0.0

    def lexical_similarity(self, text, summary):
        src_lemmas = normalize(text)
        dst_lemmas = normalize(summary)
        matching = self._get_matching(src_lemmas, dst_lemmas)
        assert len(matching) == len(src_lemmas)
        print(matching)

    def _log_rank(self, word):
        rank = self.word2rank.get(word, len(self.word2rank))
        return np.log(1 + rank)

    def _word_rank_score(self, text):
        lemmas = normalize(text)
        lemmas = [l for l in lemmas if l in self.word2rank]
        if len(lemmas) == 0:
            return np.log(1 + len(self.word2rank))
        ranks = [self._log_rank(l) for l in lemmas]
        return np.quantile(ranks, 0.75)

    @staticmethod
    def _get_matching(src_lemmas, dst_lemmas):
        biadjacency_matrix = np.zeros((len(src_lemmas), len(dst_lemmas)), dtype=np.bool)
        for i, lemma1 in enumerate(src_lemmas):
            for j, lemma2 in enumerate(dst_lemmas):
                if lemma1.lower() == lemma2.lower():
                    biadjacency_matrix[i, j] = 1
        biadjacency_matrix = sparse.csr_matrix(biadjacency_matrix)
        return maximum_bipartite_matching(biadjacency_matrix, perm_type='column')


def main(
    texts_spacy_file,
    summaries_spacy_file,
    dataset_name,
    dataset_version,
    dataset_split,
    word_rank_file,
    idfs_file,
    output_path
):
    dataset = load_dataset(dataset_name, script_version=dataset_version)
    dataset = list(dataset[dataset_split])
    scorer = TextSummaryScorer(word_rank_file, idfs_file)
    texts_analyzes = spacy_deserialize(texts_spacy_file)
    summaries_analyzes = spacy_deserialize(summaries_spacy_file)
    assert dataset[0]["text"] == str(texts_analyzes[0])
    assert dataset[-1]["text"] == str(texts_analyzes[-1])
    assert dataset[0]["summary"] == str(summaries_analyzes[0])
    assert dataset[-1]["summary"] == str(summaries_analyzes[-1])

    records = list()
    for r, text_analysis, summary_analysis in tqdm(zip(dataset, texts_analyzes, summaries_analyzes)):
        values = scorer(text_analysis, summary_analysis)
        r.update(values)
        records.append(r)
    write_jsonl(records, output_path)
    print(max([(r["WordRank"], r) for r in records]))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--texts-spacy-file", type=str, required=True)
    parser.add_argument("--summaries-spacy-file", type=str, required=True)
    parser.add_argument("--dataset-name", type=str, required=True)
    parser.add_argument("--dataset-version", type=str, required=True)
    parser.add_argument("--dataset-split", type=str, required=True)
    parser.add_argument("--word-rank-file", type=str, required=True)
    parser.add_argument("--idfs-file", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
