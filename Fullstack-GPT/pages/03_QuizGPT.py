import streamlit as st
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.output_parsers.base import T
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter


class JsonOutputParser(BaseOutputParser):
    def parse(self, text: str) -> T:
        text = (
            text
            .replace("```", "")
            .replace("json", "")
            .replace("true", "True")
            .replace("false", "False")
        )
        return eval(text)


output_parser = JsonOutputParser()

st.set_page_config(
    page_title="Quiz GPT",
    page_icon="？",
)

"""
강의 목표: Output Parser
GPT3&4에서 사용하는 Function 뭐뭐도 배움
Streamlit 심화 학습
"""

st.title("Quiz GPT")

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-1106",
    streaming=True,
    callbacks=[
        StreamingStdOutCallbackHandler()
    ]
)


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            if context language is Korean, you should make it by Korean!
            
            You are a helpful assistant that is role playing as a teacher.

            Based ONLY on the following context make 10 questions to test the user's knowledge about the text.

            Each question should have 4 answers, three of them must be incorrect and one should be correct.

            Use (o) to signal the correct answer. 

            Question examples:

            Question: 한국의 수도는 무엇 인가요?
            Answers: 경기|울산|부산|울산(o)

            Question: 2024년 한국의 대통령은 누구 인가요?
            Answers: 김영삼|윤석렬(o)|김대중|안철수

            Question: '임진왜란'은 언제 발생 했나요?
            Answers: 1592(o)|1950|2002|2021

            Your turn!

            Context: {context}
            """
        )
    ]
)

questions_chain = {
                      "context": format_docs
                  } | questions_prompt | llm

formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
    You are a powerful formatting algorithm.

    You format exam questions into JSON format.
    Answers with (o) are the correct ones.

    Example Input:
    Question: What is the color of the ocean?
    Answers: Red|Yellow|Green|Blue(o)

    Question: What is the capital or Georgia?
    Answers: Baku|Tbilisi(o)|Manila|Beirut

    Question: When was Avatar released?
    Answers: 2007|2001|2009(o)|1998

    Question: Who was Julius Caesar?
    Answers: A Roman Emperor(o)|Painter|Actor|Model


    Example Output:

    ```json
    {{ "questions": [
            {{
                "question": "What is the color of the ocean?",
                "answers": [
                        {{
                            "answer": "Red",
                            "correct": false
                        }},
                        {{
                            "answer": "Yellow",
                            "correct": false
                        }},
                        {{
                            "answer": "Green",
                            "correct": false
                        }},
                        {{
                            "answer": "Blue",
                            "correct": true
                        }},
                ]
            }},
                        {{
                "question": "What is the capital or Georgia?",
                "answers": [
                        {{
                            "answer": "Baku",
                            "correct": false
                        }},
                        {{
                            "answer": "Tbilisi",
                            "correct": true
                        }},
                        {{
                            "answer": "Manila",
                            "correct": false
                        }},
                        {{
                            "answer": "Beirut",
                            "correct": false
                        }},
                ]
            }},
                        {{
                "question": "When was Avatar released?",
                "answers": [
                        {{
                            "answer": "2007",
                            "correct": false
                        }},
                        {{
                            "answer": "2001",
                            "correct": false
                        }},
                        {{
                            "answer": "2009",
                            "correct": true
                        }},
                        {{
                            "answer": "1998",
                            "correct": false
                        }},
                ]
            }},
            {{
                "question": "Who was Julius Caesar?",
                "answers": [
                        {{
                            "answer": "A Roman Emperor",
                            "correct": true
                        }},
                        {{
                            "answer": "Painter",
                            "correct": false
                        }},
                        {{
                            "answer": "Actor",
                            "correct": false
                        }},
                        {{
                            "answer": "Model",
                            "correct": false
                        }},
                ]
            }}
        ]
     }}
    ```
    Your turn!
    Questions: {context}
""",
        )
    ]
)

formatting_chain = formatting_prompt | llm


@st.cache_resource(show_spinner="Loading file...")
def split_file(file):
    file_content = file.read()
    file_path = f"./.cache/quiz_files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs


@st.cache_data(show_spinner="Making quize...")
def run_quiz_chain(_docs, topic = None):
    chain = {"context": questions_chain} | formatting_chain | output_parser
    return chain.invoke(_docs)


@st.cache_data(show_spinner="Searching Wikipedia...")
def wiki_search(term):
    retriever = WikipediaRetriever(top_k_results=5, lang='ko')
    return retriever.get_relevant_documents(term) # Deprecated 됬으니 invoke 써라 뜸


with st.sidebar:
    docs = None
    topic = None

    choice = st.selectbox("Choose what you want to use.", (
        "File", "Wikipedia Articl"
    ))
    if choice == "File":
        file = st.file_uploader("Upload a .docx, .txt or .pdf file", type=["docx", "txt", "pdf"])
        if file:
            docs = split_file(file)
    else:
        topic = st.text_input("Enter a topic to search on Wikipedia")
        if topic:
            docs = wiki_search(topic)

if not docs:
    st.markdown(
        """
        ### Quiz GPT에 오신걸 환영합니다.
        
        이 페이지에서는 Quiz GPT를 사용하여 퀴즈를 생성할 수 있습니다.
        시작하려면, 왼쪽 사이드바에서 파일을 업로드하거나, 위키피디아에서 토픽을 검색하세요.
        """
    )
else:
    response = run_quiz_chain(docs, topic if topic else file.name)
    st.write(response)
    with st.form("questions_form"):
        for question in response['questions']:
            st.write(question["question"])
            value = st.radio(
                "Select an option",
                [answer["answer"] for answer in question["answers"]],
                index=None,
            )
            if {"answer": value, "correct": True} in question["answers"]:
                st.success("Correct!")
            elif value is not None:
                st.error("Wrong!")
        button = st.form_submit_button("Submit")

