import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from langchain_ollama import OllamaLLM
from scripts.create_prompt import create_prompt
from scripts.access_db import access_db


def llm_judges_similarity(query, model_response, ground_truth) -> bool:
    judge_prompt = f"""
    You are evaluating if a model's answer is sufficiently aligned with a given ground truth answer to a user question.

    Question:
    {query}

    Ground Truth:
    {ground_truth}

    Model Response:
    {model_response}

    Does the model's response correctly and meaningfully answer the user's question in a way that's comparable to the ground truth?

    Respond with only "Yes" or "No".
    """.strip()

    judge = OllamaLLM(model='aya-expanse:latest')
    verdict = judge.invoke(judge_prompt).strip().lower()

    return verdict.startswith("yes")


@pytest.mark.parametrize(
    "query, ground_truth",
    [
        (
            "What's the difference between Asperger's and autism?",
            "Asperger's is considered a high-functioning form of autism. People with Asperger's generally have better language development and cognitive skills than those with classic autism, but they may still struggle with social interaction and nonverbal communication.",
        ),
        (
            "What do you think about Autism Speaks? Is it a good resource to turn to?",
            "Autism Speaks is considered controversial and is not widely recommended as a resource by many in the autism community. It has been criticized for promoting stigma and not meaningfully including autistic voices.",
        ),
        (
            "Can autism be cured?",
            "No, autism can’t be cured—but with the right support and timely services, children can grow, learn, and do well."
        ),
        (
            "My child was fine before. Will he become “normal” again?",
            "Most signs of autism show up around age 3 and up. There’s no such thing as “normal”—neurotypical children are wired differently, so we need to help autistic children navigate the world in their own way."
        ),
        (
            "Can I just wait and ignore my autistic son's condition? Will he be okay?",
            "Waiting can make things harder. Early help gives your child the best chance to learn and grow."
        ),
        (
            "I’ve heard Albert Einstein was autistic—does that mean my child is a genius?",
            "Every child is different. What matters most is helping your child reach their full potential through therapy, learning, and life skills."
        ),
        (
            "What could I have done to stop autism in my child?",
            "Nothing. Autism isn’t caused by parenting, vaccines, or anything you missed."
        ),
        (
            "Can I afford autism therapy?",
            "Therapies can be costly, but help is available through insurance, school IEPs, Medicaid, and nonprofit organizations. Ask around—support exists."
        ),
        (
            "What special education services does the government provide?",
            "The government offers early intervention, special education (IEPs), Medicaid, SSI, therapy, assistive tech, and financial support based on your child’s needs."
        ),
        (
            "Can the school really help my autistic child? They don’t seem like experts.",
            "Yes, schools are required to support children with disabilities. Ask for an IEP and be part of the process—bring experts if needed, stay involved, and make sure your child’s needs are met."
        ),
        (
            "Are there treatments for my autistic child?",
            "There are therapies that help with speech, movement, behavior, and life skills. The goal is to help the child become as independent and confident as possible."
        ),
        (
            "Can he be independent when he grows up?",
            "Many autistic people live independently or with support. With life skills and confidence, your child can live a happy, functional life."
        ),
        (
            "Will my nonverbal autistic child ever speak?",
            "Some kids speak later, and some may not use words at all—but all children can learn to communicate in their own way. Use signs, AAC apps, and always talk to your child and include them in daily life."
        ),
        (
            "Is my autistic son's condition my fault?",
            "No. You didn’t cause this, and nothing you did made your child autistic."
        ),
    ]
)
def test_model_response_llm_verified(query, ground_truth):
    db = access_db()
    _, final_prompt = create_prompt(db, query, k=5)

    model = OllamaLLM(model='aya-expanse:latest')
    response = model.invoke(final_prompt).strip()

    print(f"\n---\nQuery: {query}")
    print(f"Response:\n{response}")
    print(f"Ground Truth:\n{ground_truth}")

    assert llm_judges_similarity(query, response, ground_truth), "LLM judged the response as insufficient."