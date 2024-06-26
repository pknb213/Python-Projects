import time

import streamlit as st
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📄"
)


def embed_fil(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    st.write(file_content, file_path)

    with open(file_path, "wb") as f:
        f.write(file_content)

    cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )

    loader = UnstructuredFileLoader(
        file_path=f"{file_path}"
    )
    docs = loader.load_and_split(text_splitter=splitter)

    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embeddings, cache_dir
    )
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


st.title("DocumentGPT")

st.markdown(
    """
        Welcome!
        Use this chatbot to ask questions to an AI about your files!
    """
)

file = st.file_uploader(
    "Upload a .txt, .pdf or .dock file",
    type=["txt", "pdf", "docx"]
)

if file:
    retriever = embed_fil(file)
    s = retriever.invoke("winston")
    s

