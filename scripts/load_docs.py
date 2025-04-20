from langchain_community.document_loaders import PyPDFDirectoryLoader

def load_docs(path: str) -> PyPDFDirectoryLoader:
    """Load PDF documents and print its content."""
    loader = PyPDFDirectoryLoader(path)
    return loader.load()