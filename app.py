import os
import pathlib

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def load_vectorstore():
    output_folder = pathlib.Path(os.getenv("OUTPUT_FOLDER", "outputs"))
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    vectorstore = FAISS.load_local(
        output_folder / "vectorstore", embeddings, allow_dangerous_deserialization=True
    )
    return vectorstore


vectorstore = load_vectorstore()
st.title("Semantic Search ")
st.write("Enter a query to search articles:")
query = st.text_input("Search Query", "")

if query:
    res = vectorstore.similarity_search(query, k=5)
    st.write(f"Results for query: **{query}**")
    for i, doc in enumerate(res):
        st.write(f"### {doc.metadata["category"]} | {doc.metadata["title"]}")
        st.write(doc.metadata["link"])
        st.write("---")
