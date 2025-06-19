import ollama
from knowledge_prompt import retrieve_context

def main():
    query = input("Your question: ")

    # db = access_db()
    # search_results, final_prompt = create_prompt(db, query, k=5)

    context = retrieve_context(query)
    prompt = f"""Answer the question using the following context:

    {context}

    Question: {query}"""

    # Replace langchain_ollama with official ollama call
    response = ollama.generate(
        model='qwen3:8b',
        prompt=prompt
    )

    print(f"\nResponse:\n{response['response']}")

    # Different Source listing method in the future.

if __name__ == '__main__':
    main()