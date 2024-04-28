import streamlit as st
from langchain.prompts import PromptTemplate

st.set_page_config(
    page_title="Language Chain Home",
    page_icon="🔗"
)

with st.sidebar:
    st.title("Language Chain")
    st.text_input("Enter your prompt here:")

st.title("Language Chain")

tab_one, tab_two, tab_three = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab_one:
    st.write("This is tab one")
with tab_two:
    st.write("This is tab two")
with tab_three:
    st.write("This is tab three")
