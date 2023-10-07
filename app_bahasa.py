import pickle
import g4f
from local_db import *
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Nusacular",
    page_icon="✨"
)

# Sidebar
with st.sidebar:
    selected = option_menu(
        "Nusacular", 
        ['Prediksi Bahasa Daerah', 'Chatbot', 'About Us'], 
        icons=['flag', 'robot', "person-fill"], 
        default_index=0
    )

with open('model/lrmodel.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

if selected == "Prediksi Bahasa Daerah":
    st.title("Prediksi Bahasa Daerah")

    input_kata = st.text_input(label="Masukkan kata")
    prediksi = st.button ("Prediksi")

    if prediksi:
        predicted_language = loaded_model.predict([input_kata])

        class_probabilities = loaded_model.predict_proba([input_kata])

        st.write("Predicted Language:", predicted_language[0])

        confidence_score = max(class_probabilities[0])
        st.write("Confidence Score:", confidence_score)

elif selected == "Chatbot":
    st.title("Nusacular Bot")

    # Load chat history from the database
    messages = retrieve_messages()
    for message in messages :
        with st.chat_message(message[0]):  # message[0] corresponds to the 'role'
            st.markdown(message[1])  # message[1] corresponds to the 'content'

    # React to user input
    if prompt := st.chat_input("Mau tanya apa?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        print('Prompt:', prompt, '\n')

        # Add user message to the database
        insert_message("user", prompt)

        # Define roles for messages
        role = ["system", "user", "assistant"]

        while True:
            response = g4f.ChatCompletion.create(
                        model=g4f.models.gpt_4,
                        provider=g4f.Provider.Aivvm,
                        messages=[{"role": role[1], "content": prompt}]
                    )
            if response == '':
                print("Empty response, retrying...")
                continue
            else:
                print('Response:', response)
                break

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to the database
        insert_message("assistant", response)

    # Button to clear the database (conditionally displayed)
    if messages:
        if st.button("Clear Database"):
            clear_database()
            # st.success("Database cleared successfully!")
            st.experimental_rerun()  # Reload the Streamlit app

else:
    st.title("About Us")

    # About Us
    st.markdown("""
    Dibuat pada 4 Oktober 2023, Nusacular (Nusantara Vernacular) adalah sebuah aplikasi yang dapat memprediksi bahasa daerah dan juga dapat digunakan sebagai chatbot.
    
    Aplikasi ini dibuat oleh:
    |             Name            |      NIM       |
    | --------------------------- | -------------- |
    | Bima Rakajati               | A11.2020.13088 |
    | Enrico Zada                 | A11.2020.12972 |
    | Rosalia Natal Silalahi      | A11.2020.13084 |
    | Devi Kartika Sari           | A11.2020.12518 |
    """)