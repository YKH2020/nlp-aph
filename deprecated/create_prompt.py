from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

def create_prompt(db: Chroma, query: str, k: int = 5) -> tuple[list, str]:
    search_results = db.similarity_search_with_score(query, k) # Messing around

    PROMPT = '''
    Answer the question using the following context:
    {context}

    _______
    Answer the question using the above context:
    {question}
    '''

    def remove_subset_chunks(chunks: list[str]) -> list[str]:
        unique_chunks = []
        for chunk in sorted(chunks, key=len, reverse=True): 
            if not any(chunk in uc for uc in unique_chunks):
                unique_chunks.append(chunk)
        return unique_chunks

    # Start from raw results
    raw_chunks = [doc.page_content.strip() for doc, _ in search_results]

    # Step 1: remove exact duplicates
    raw_chunks = list(set(raw_chunks))

    # Step 2: remove subset duplicates
    filtered_chunks = remove_subset_chunks(raw_chunks)

    # Optional: assemble into prompt
    context = "\n\n_______\n\n".join(filtered_chunks)
    final_prompt = ChatPromptTemplate.from_template(PROMPT).format(context=context, question=query)
    return search_results, final_prompt