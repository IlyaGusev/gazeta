import json

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm


IGNORE_POS_TAGS = ("PUNCT", "CCONJ", "ADP", "PART", "SCONJ", "PRON", "ADV", "DET", "SYM", "NUM")
IGNORE_TOKENS = ("-", )


def normalize(doc, lowercase=True, ignore_pos=True, ignore_tokens=True):
    lemmas = []
    for token in doc:
        lemma = token.lemma_
        pos = token.pos_
        token = token.text
        if ignore_pos and pos in IGNORE_POS_TAGS:
            continue
        if ignore_tokens and token in IGNORE_TOKENS:
            continue
        if lowercase:
            lemma = lemma.lower()
        lemmas.append(lemma)
    return lemmas


def spacy_serialize(texts, spacy_model, output_path):
    docs = DocBin()
    for doc in tqdm(spacy_model.pipe(texts)):
        docs.add(doc)
    bytes_data = docs.to_bytes()
    with open(output_path, "wb") as w:
        w.write(bytes_data)


def spacy_deserialize(path):
    spacy_model = spacy.blank("ru")
    with open(path, "rb") as r:
        docs = DocBin().from_bytes(r.read())
    return list(docs.get_docs(spacy_model.vocab))


def write_jsonl(records, path):
    with open(path, "w") as w:
        for r in records:
            w.write(json.dumps(r, ensure_ascii=False) + "\n")
