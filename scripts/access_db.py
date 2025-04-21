from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()

# Patch sqlite3 globally for ChromaDB
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # Fine when running locally

def access_db() -> Chroma:
    return Chroma(
        persist_directory='./data/db',
        embedding_function=OpenAIEmbeddings(model='text-embedding-3-large')
    )