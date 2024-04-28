import streamlit as st
from langchain.prompts import PromptTemplate

st.set_page_config(
    page_title="Language Chain Home",
    page_icon="🔗"
)

st.markdown(
    """
    # Hello !!
    
    Welcome to my Fullstack GPT Portfolio!
    
    Here are the my apps i made
    
    - [ ] [DocumentGPT](/DocumentGPT)
    - [ ] [PrivateGPT](/PrivateGPT)
    - [ ] [QuizGPT](/QuizGPT)
    - [ ] [SiteGPT](/SiteGPT)
    - [ ] [MeetingGPt](/MeetingGPT)
    - [ ] [InvestorGPT](/InvestorGPT)
    
    """
)

# with st.sidebar:
#     st.title("Language Chain")
#     st.text_input("Enter your prompt here:")
#
# st.title("Language Chain")
#
# tab_one, tab_two, tab_three = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
#
# with tab_one:
#     st.write("This is tab one")
# with tab_two:
#     st.write("This is tab two")
# with tab_three:
#     st.write("This is tab three")
