import streamlit as st
from langchain.prompts import PromptTemplate

# streamlit run Home.py
st.title("Home")

st.subheader("Welcome to the Home Page")

st.markdown("""
    #### I love it
""")

st.write("Hello")
st.write([1,2,3,4,5])
st.write({"a": 1, "b": 2, "c":3})
st.write(PromptTemplate)

p = PromptTemplate.from_template("x x x x")
st.write(p)

st.selectbox("Select Model", ("GPT-3", "GPT-4", "GPT-5"))

