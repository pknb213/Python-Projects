import time

import streamlit as st

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📄"
)

st.title("DocumentGPT")

with st.chat_message("human"):
    st.write("Hello! I'm a human message!")

with st.chat_message("ai"):
    st.write("how are you")

with st.status("Embedding file...", expanded=True) as status:
    time.sleep(2)
    st.write("File embedded!")
    time.sleep(2)
    st.write("Embedding file...")
    time.sleep(2)
    st.write("caching the file")
    status.update(label="Error", state="error")
