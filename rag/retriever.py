import hashlib
import os

from langchain_chroma import Chroma

from config import CHROMA_PATH

from rag.embedding import get_embedding_model


COLLECTION_NAME = "office_documents"


_vector_store = None


def get_vector_store():
    """
    Create the Chroma vector store only once.
    """

    global _vector_store

    if _vector_store is None:

        _vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_model()
        )

    return _vector_store


def _document_hash(chunks):
    """
    Generate a unique hash for the uploaded document.
    """

    text = ""

    for chunk in chunks:
        text += chunk.page_content
        

    return hashlib.md5(text.encode()).hexdigest()


def create_vector_store(chunks):
    """
    Store the document only once.
    """

    vector_store = get_vector_store()

    doc_hash = _document_hash(chunks)

    hash_file = os.path.join(
        CHROMA_PATH,
        "last_document.hash"
    )

    if os.path.exists(hash_file):

        with open(hash_file, "r") as f:

            previous_hash = f.read().strip()

        if previous_hash == doc_hash:
            return vector_store

    try:
        vector_store.delete_collection()
    except Exception:
        pass

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model()
    )

    vector_store.add_documents(chunks)

    with open(hash_file, "w") as f:
        f.write(doc_hash)

    global _vector_store
    _vector_store = vector_store

    return vector_store


def get_retriever():

    return get_vector_store().as_retriever(
        search_kwargs={
            "k": 3
        }
    )