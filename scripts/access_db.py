from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()

def access_db() -> Chroma:
    return Chroma(
        persist_directory='./data/db',
        embedding_function=OpenAIEmbeddings(model='text-embedding-3-large')
    )