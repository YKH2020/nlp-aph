from langchain_ollama import OllamaLLM
from create_prompt import create_prompt
from access_db import access_db
from non_dl_naive import non_dl, naive

def main():
    query = input()
    db = access_db()
    search_results, final_prompt = create_prompt(db, query, k=5)

    model = OllamaLLM(model='aya-expanse:latest')
    response = model.invoke(final_prompt)
    print(f'Response:\n{response}')

    print([score for _, score in search_results])

    sources = '\n\n_______\n\n'.join(
        {f"{piece.metadata.get('title')} — {piece.metadata.get('author')}"
        for piece, _ in search_results}
    )
    print(f'We got this response based on the following trustworthy and reputable source(s):\n\n{sources}')
    # Update Metadata in future!

if __name__ == '__main__':
    main()

    # ----- Uncomment the following if you want to see the other approaches: ----- #
    # PATH = './data/in_use'
    # naive(PATH)
    # non_dl(PATH)