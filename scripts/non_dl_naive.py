from load_docs import load_docs
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from hmmlearn.hmm import GaussianHMM
from itertools import groupby
from sklearn.preprocessing import StandardScaler
import numpy as np
import re

def jaccard_similarity(a: str, b: str) -> float:
    a_tokens = set(re.findall(r'\w+', a.lower()))
    b_tokens = set(re.findall(r'\w+', b.lower()))
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens) if a_tokens and b_tokens else 0.0

def get_top_matches(query: str, sentences: list, k: int = 10) -> list[tuple[float]]:
    scores = [
        (entry["sentence"], jaccard_similarity(query, entry["sentence"]), entry["title"], entry["author"], entry["page"])
        for entry in sentences
    ]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:k]

def get_every_sentence(docs: list) -> list:
    # ---- r"(?<=[.?!])\s+" -> optimal sentence split regex taken from SemanticChunker documentation --- #
    every_sentence = []
    for doc in docs:
        sentences = re.split(r"(?<=[.?!])\s+", doc.page_content)
        for s in sentences:
            s = s.strip()
            if s:  # skip empty sentences
                every_sentence.append({
                    "sentence": s,
                    "title": doc.metadata.get("title", ""),
                    "author": doc.metadata.get("author", ""),
                    "page": doc.metadata.get("page_label", "")
                })
    return every_sentence

def naive(path: str) -> list:
    print('Loading documents...')
    docs = load_docs(path)
    every_sentence = get_every_sentence(docs)

    query = input('\nType in a relevant sentence: ')
    top_matches = get_top_matches(query, every_sentence, k=10)

    for sentence, score, title, author, page in top_matches:
        print(f"[{score:.2f}] Page {page} from {title} by {author}:\n→ {sentence}\n")

    return every_sentence

def non_dl(path: str) -> None:
    docs = load_docs(path)
    every_sentence = get_every_sentence(docs)

    # Will specify a default value if key is not found. Groups the sentences in every sentence by title into the defaultdict.
    grouped_by_doc = defaultdict(list)
    for s in every_sentence:
        grouped_by_doc[s['title']].append(s)

    topic_chunks = []
    topic_keywords_all_docs = {}

    for title, sentences in grouped_by_doc.items():
        sent_texts = [s['sentence'] for s in sentences]

        vectorizer = TfidfVectorizer(max_features=100)
        X_text = vectorizer.fit_transform(sent_texts).toarray()

        feats = []
        for i, s in enumerate(sentences):
            pos_norm = i / len(sentences)
            title_case_count = sum(w.istitle() for w in s['sentence'].split())
            feats.append([pos_norm, title_case_count])

        feats = np.array(feats)
        X_combined = np.concatenate([X_text, feats], axis=1)
        X = StandardScaler().fit_transform(X_combined)

        n_components = 5
        model = GaussianHMM(n_components=n_components, covariance_type="full", n_iter=200, tol=1e-2)
        model.fit(X)
        score = model.score(X)
        print(f"\nTitle: {title}\nn={n_components} → log-likelihood: {score}")

        topic_states = model.predict(X)
        for i, s in enumerate(sentences):
            s['topic'] = int(topic_states[i])

        # Extract top keywords per topic
        topic_to_indices = defaultdict(list)
        for idx, topic in enumerate(topic_states):
            topic_to_indices[topic].append(idx)

        feature_names = vectorizer.get_feature_names_out()
        topic_keywords = {}

        for topic, indices in topic_to_indices.items():
            topic_tfidfs = X_text[indices]  # only rows for this topic
            summed = topic_tfidfs.sum(axis=0)  # sum TF-IDF scores
            top_indices = summed.argsort()[::-1][:8]  # top 8 keywords
            top_terms = [feature_names[i] for i in top_indices]
            topic_keywords[topic] = top_terms

        topic_keywords_all_docs[title] = topic_keywords

        for topic, group in groupby(sentences, key=lambda x: x['topic']):
            group_list = list(group)
            chunk_text = " ".join(s['sentence'] for s in group_list)
            topic_chunks.append({
                "title": title,
                "topic": topic,
                "keywords": topic_keywords.get(topic, "off topic"),
                "page_start": group_list[0]["page"],
                "text": chunk_text
            })

    for chunk in topic_chunks:
        print(f"\nTitle: {chunk['title']}")
        print(f"Topic: {chunk['topic']} — Keywords: {', '.join(chunk['keywords'])}")
        print(f"Starts on Page {chunk['page_start']}")
        print(f"Text: {chunk['text'][:1000]}...continue reading from source for more.")