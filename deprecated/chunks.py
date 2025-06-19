from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import itertools
from dotenv import load_dotenv
load_dotenv()

def chunks(docs: PyPDFDirectoryLoader) -> list:
    text_splitter = SemanticChunker(
        OpenAIEmbeddings(model='text-embedding-3-large'), 
        breakpoint_threshold_type="gradient", # Gradient because our sources fall under the same topic.
        buffer_size=0
    )

    ranges = [
        (0, 5), (187, 200), (201, 207), (289, 290), (291, 298),
        (459, 459), (460, 471), (522, 522), (523, 533),
        (730, 738), (739, 745), (1007, 1009), (1012, 1013),
        (1014, 1018), (1419, 1421), (1422, 1435), (1704, 1741),
        (1747, 1747), (1748, 1755), (1877, 1877), (1891, 1894)
    ]

    # Flatten ranges to a set of excluded page numbers
    bad_pages = set()
    for start, end in ranges:
        bad_pages.update(range(start, end + 1))

    pages = []
    for i, doc in enumerate(docs):
        # Implement removal of certain title / toc pages / disregarding empty page content pages
        if doc.page_content != '' and i not in bad_pages:
            pages.append(text_splitter.create_documents(texts=[doc.page_content], metadatas=[doc.metadata]))

    pages_chunks = list(itertools.chain.from_iterable(pages))
    return pages_chunks