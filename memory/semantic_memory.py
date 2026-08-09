from langchain_chroma import Chroma

from config import CHROMA_PATH

from rag.embedding import get_embedding_model


COLLECTION_NAME = "semantic_memory"


_memory_store = None


def get_memory_store():

    global _memory_store

    if _memory_store is None:

        _memory_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_model()
        )

    return _memory_store


def save_memory(text):

    memory_store = get_memory_store()

    memory_store.add_texts([text])


def search_memory(query, k=3):

    memory_store = get_memory_store()

    docs = memory_store.similarity_search(
        query,
        k=k
    )

    return docs