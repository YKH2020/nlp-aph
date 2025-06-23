from knowledge_prompt import retrieve_context
from zephyr import ask_zephyr

def main():
    query = input("Your question: ").strip()
    context = retrieve_context(query)

    prompt = f"""Answer the question using the following context:

{context}

Question: {query}"""

    response = ask_zephyr(prompt)
    print("\nResponse:\n" + response)

if __name__ == "__main__":
    main()