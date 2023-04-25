# Chat.py
# Streamlit App demonstrates chat functionality

import os
import pickle
import streamlit as st

from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI

st.set_page_config(page_icon="💬", page_title="Jcrew Bot")

st.markdown(
    "<h1 style='text-align: center;'>Jcrew Bot</h1>",
    unsafe_allow_html=True)


def main():

    # Set up Chain

    os.environ["OPENAI_API_KEY"] = 'my_key'
    input_path = '/Users/cristinconnerney/Desktop/Instalily/data/data2.pkl'

    with open(input_path, "rb") as f:
        vectorstore = pickle.load(f)

    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
    You can assume the question is about Jcrew products.
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

    template = """You are an AI assistant for answering questions about Jcrew products.
    You are given the following documents. Provide a conversational answer. Share products that are relevant.
    If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
    If the question is not about clothing or Jcrew, politely inform them that you are tuned to only answer questions about clothing.
    Question: {question}
    =========
    {context}
    =========
    Answer:"""

    QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])

    retriever = vectorstore.as_retriever()
    llm = OpenAI(temperature=0)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )

    def conversational_chat(query):

        output = qa_chain({"question": query, "chat_history": st.session_state['history']})["answer"]
        st.session_state['history'].append((query, output))

        return output

    # UI and Streamlit-chat stuff ---------------------------------------------

    if 'history' not in st.session_state:
        st.session_state['history'] = []
        
    if 'reset_chat' not in st.session_state:
        st.session_state['reset_chat'] = False

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey!"]

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about Jcrew Products"]


    # Create a container for displaying the chat history
    response_container = st.container()
    
    # Create a container for the user's text input
    container = st.container()

    with container:
        
        # Create a form for the user to enter their query
        with st.form(key='my_form', clear_on_submit=True):
            
            user_input = st.text_input("Query:", placeholder="Ask a question here", key='input')

            submit_button = st.form_submit_button(label='Send')
            reset_button = st.form_submit_button(label='Reset')

    if reset_button:
        st.session_state['reset_chat'] = True

    # If the "reset_chat" flag has been set, reset the chat history and generated messages
    if st.session_state['reset_chat']:
        
        st.session_state['history'] = []
        st.session_state['past'] = ["Hey!"]
        st.session_state['generated'] = ["Hello! Ask me about Jcrew Products"]
        response_container.empty()
        st.session_state['reset_chat'] = False
        
        
    # If the user has submitted a query
    if submit_button and user_input:
        
        # Generate a response
        output = conversational_chat(user_input)
        
        # Add user input and chatbot output to chat history
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

    # If there are generated messages to display
    if st.session_state['generated']:
        
        # Display the chat history
        with response_container:
            
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")

# Command to run: streamlit run Chat.py

if __name__ == "__main__":
    main()