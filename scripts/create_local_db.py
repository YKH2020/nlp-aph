from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()

def create_local_db(pages_chunks: list) -> None:
    Chroma.from_documents(
        documents=pages_chunks,
        embedding=OpenAIEmbeddings(model='text-embedding-3-large'),
        persist_directory='../data/db',
        collection_metadata={"hnsw:space": "cosine"}
    )
    # db.persist()