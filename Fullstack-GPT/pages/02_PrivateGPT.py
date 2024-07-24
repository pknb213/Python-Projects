from typing import Any

import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.embeddings import CacheBackedEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import OllamaEmbeddings

st.set_page_config(
    page_title="Private GPT",
    page_icon="📄",
)


class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.message_box = st.empty()
        self.message = ""

    def on_llm_start(
            self,
            *args,
            **kwargs: Any,
    ) -> Any:
        self.message_box = st.empty()

    def on_llm_end(
            self,
            *args,
            **kwargs: Any,
    ) -> Any:
        save_message(self.message, "ai")

    def on_llm_new_token(
            self,
            token: str,
            *args,
            **kwargs: Any,
    ) -> Any:
        self.message += token
        self.message_box.markdown(self.message)


llm = ChatOllama(
    model="mistral:latest",
    temperature=0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),

    ]
)


@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/private_files/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    cache_dir = LocalFileStore(f"./.cache/private_embeddings/{file.name}")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )

    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)

    embeddings = OllamaEmbeddings(
        model="mistral:latest",
    )
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], save=False)


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


prompt = ChatPromptTemplate.from_template(
    """Answer the question using only the following context and not your training data. if you don't know the answer just say you don't know.
        Don't make anything up And Please answer in Korean only.
        Context: {context}
        Question: {question}
    """
)
st.title("Private GPT")

st.markdown(
    """
        Welcome!
        Use this chatbot to ask questions to an AI about your files!

        Upload your files on the sidebar.
    """
)

with st.sidebar:
    file = st.file_uploader(
        "Upload a .txt, .pdf or .dock file",
        type=["txt", "pdf", "docx"]
    )

if file:
    retriever = embed_file(file)
    send_message("I'm ready! Ask me anything!", "ai", save=False)
    paint_history()
    message = st.chat_input("Ask me anything!")
    if message:
        send_message(message, "human")
        # docs = retriever.invoke(message)
        # docs = "\n\n".join(document.page_content for document in docs)
        # prompt = template.format_messages(context=docs, question=message)
        # lim.predict_messages(prompt)
        chain = {
                    "context": retriever | RunnableLambda(format_docs),
                    "question": RunnablePassthrough()
                } | prompt | llm
        # response = chain.invoke(message)
        # send_message(response.content, "ai")
        with st.chat_message("ai"):
            response = chain.invoke(message)
else:
    st.session_state["messages"] = []
