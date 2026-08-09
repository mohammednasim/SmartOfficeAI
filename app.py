import os
import streamlit as st

from config import UPLOAD_FOLDER
from graph.graph import graph
from graph.state import AgentState

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.retriever import create_vector_store


st.title(" Smart Office AI")
st.write("Upload a PDF document and ask questions!")

# PDF Upload Section
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        docs = load_pdf(save_path)
        chunks = split_documents(docs)
        create_vector_store(chunks)
        st.success("PDF uploaded and processed successfully!")
    except Exception as e:
        st.warning(f"PDF uploaded but RAG processing failed: {e}")
        st.info("You can still use other features like calculator, SQL, email, and calendar.")

# Chat Section
st.divider()
st.subheader("Ask a Question")

user_input = st.text_input("Your question:")

if st.button("Send") and user_input:
    with st.spinner("Processing..."):
        state = {"user_input": user_input, "response": "", "next": ""}
        result = graph.invoke(state)
        st.write("**AI Response:**")
        st.write(result["response"])