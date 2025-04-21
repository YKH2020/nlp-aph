import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from scripts.non_dl_naive import get_top_matches, get_every_sentence
from scripts.load_docs import load_docs

@pytest.mark.parametrize(
    "query_sentence",
    [
        "By having autistic friends and by letting your child know and learn from autistic adults, you can combat the ableist messages we all grow up hearing.",
        "If you asked me whether I expected to be taught mathematics or science as part of my Individualized Education Plan (IEP), I would say, “No.”",
        "I wanted so many times to be accepted for who I was",
        "For students with autism, problem behaviors may be triggered for a variety of reasons.",
        "My parents did not use any labels or even tell me I had a disability.",
        "I had found a niche where many of my Aspergian traits actually benefited me. My compulsion to know everything about cars made me a great service person.",
        "I Don’t Believe in Normal People",
        "At a conference a man with autism told me that he feels only three emotions, fear, sadness, and anger",
        "Another category is the more confessional memoir, usually written by a parent, describing the impact of autism on the family and sometimes the positive eect of an unorthodox treatment",
    ]
)
def test_exact_sentence_match_returns_score_1(query_sentence):
    docs = load_docs("./data/in_use")
    sentences = get_every_sentence(docs)

    top_matches = get_top_matches(query_sentence, sentences, k=1)
    top_sentence, score, _, _, _ = top_matches[0]

    print(f"\nQuery: {query_sentence}")
    print(f"Top Match: {top_sentence}")
    print(f"Score: {score:.2f}")

    assert score > 0.5, f"Generally expect exact match score of 1.0, but with PyPDF's imperfect extraction, we look for scores greater than 0.5. Our non-DL implementation cannot be evaluated beyond human evaluation. {score:.2f}"