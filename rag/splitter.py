from langchain_text_splitters import RecursiveCharacterTextSplitter


_text_splitter = None


def get_text_splitter():
    """
    Create the text splitter only once.
    """

    global _text_splitter

    if _text_splitter is None:

        _text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )
        

    return _text_splitter


def split_documents(documents):
    """
    Split PDF documents into chunks.
    """

    splitter = get_text_splitter()

    chunks = splitter.split_documents(documents)

    return chunks

