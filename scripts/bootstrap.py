from load_docs import load_docs
from chunks import chunks
from create_local_db import create_local_db

def main():
    PATH = '../data/in_use'
    docs = load_docs(PATH)
    pages_chunks = chunks(docs)
    create_local_db(pages_chunks)

    print("ChromaDB created at ../data/db")

if __name__ == '__main__':
    main()