import streamlit as st
import g4f
from local_db import *

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

        # Define roles for messages
        role = ["system", "user", "assistant"]

        response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[{"role": role[1], "content": prompt}],
                    provider=g4f.Provider.ChatgptDemo,
                )
        print('Response:', response, '\n')

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to the database
        insert_message("assistant", response)

    # Button to clear the database (conditionally displayed)
    if messages:
        if st.button("Clear Database"):
            clear_database()
            st.experimental_rerun() # Reload the Streamlit app