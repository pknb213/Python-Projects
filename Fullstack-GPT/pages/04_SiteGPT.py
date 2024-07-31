# 1. playwright, 2. chromium
# 2. sitemap
import streamlit as st
from langchain.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer

st.set_page_config(
    page_title="Quiz GPT",
    page_icon="？",
)

html2text_transformer = Html2TextTransformer()

st.title("Site GPT")

st.markdown(
    """
        Welcome!
        Use this chatbot to ask questions to an AI about your files!

        Upload your files on the sidebar.
    """
)

with st.sidebar:
    url = st.text_input("Write down a URL", placeholder="https://example.com")

if url:
    # async chromium loader
    loader = AsyncChromiumLoader([url])
    docs = loader.load()
    transformed = html2text_transformer.transform_documents(docs)
    st.write(docs)