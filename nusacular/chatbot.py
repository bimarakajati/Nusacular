import streamlit as st
import google.generativeai as genai
from local_db import *

genai.configure(api_key=st.secrets["gemini_api_key"])
model = genai.GenerativeModel('gemini-pro')

def chatbot():
    st.title("Nusacular Bot")

    # Load chat history from the database
    messages = retrieve_messages()
    for message in messages :
        with st.chat_message(message[0]):  # message[0] corresponds to the 'role'
            st.markdown(message[1])  # message[1] corresponds to the 'content'

    # React to user input
    if prompt := st.chat_input("Mau tanya apa?"):
        # Display user message in chat message container
        prompt = prompt.strip()
        st.chat_message("user").markdown(prompt)
        print('Prompt:', prompt)

        # Add user message to the database
        insert_message("user", prompt)

        response = model.generate_content(prompt)
        print('Response:', response.text, '\n')

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Add assistant response to the database
        insert_message("assistant", response.text)

    # Button to clear the database (conditionally displayed)
    if messages:
        if st.button("Clear Database"):
            clear_database()
            st.experimental_rerun() # Reload the Streamlit app