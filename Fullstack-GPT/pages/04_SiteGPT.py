# 1. playwright, 2. chromium
# 2. sitemap
import streamlit as st
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import SitemapLoader

# ua = UserAgent()


def parse_page(soup: BeautifulSoup):
    header = soup.find("header")
    tooter = soup.find("tooter")
    if header:
        header.decompose()
    if tooter:
        tooter.decompose()
    return (
        str(soup.get_text())
        .replace("\n", " ")
        .replace("\xa0", " ")
        .replace("CloseSearch Submit Blog", "")
    )


@st.cache_data(show_spinner="Loading Website...")
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[
            # r"^(.*\/blog\/).*",
        ],
        parsing_function=parse_page,
    )
    loader.requests_per_second = 5
    loader.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    docs = loader.load_and_split(text_splitter=splitter)
    return docs


st.set_page_config(
    page_title="Quiz GPT",
    page_icon="？",
)

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
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please provide a sitemap URL")
    else:
        docs = load_website(url)
        st.write(docs)