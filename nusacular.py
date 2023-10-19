import g4f
import pickle
import streamlit as st
import google.generativeai as palm
from local_db import *

with open('model/lrmodel.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

def deteksi():
    st.title("Deteksi Bahasa Daerah")

    input_kata = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button ("Deteksi")

    if prediksi or input_kata != "":
        predicted_language = loaded_model.predict([input_kata])
        print("Predicted language:", predicted_language)
        st.write("Predicted Language:", predicted_language[0])

        class_probabilities = loaded_model.predict_proba([input_kata])
        print("Class probabilities:", class_probabilities)

        confidence_score = max(class_probabilities[0])
        st.write("Confidence Score:", confidence_score)

        with st.expander("Lihat detail"):
            bahasa = ['Bataknese', 'Indonesian', 'Javanese', 'Sundanese']
            for i in range(len(bahasa)):
                st.write(f'{bahasa[i]}:')
                st.progress(class_probabilities[0][i])

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

        palm.configure(api_key=st.secrets["API_KEY"])
        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        model = models[0].name

        response = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
        )
        print('Response:', response.result, '\n')

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.result)

        # Add assistant response to the database
        insert_message("assistant", response.result)

    # Button to clear the database (conditionally displayed)
    if messages:
        if st.button("Clear Database"):
            clear_database()
            st.experimental_rerun() # Reload the Streamlit app

def about_us():
    st.title("About Us")

    # About Us
    st.markdown("""
    Dibuat pada 4 Oktober 2023, Nusacular (Nusantara Vernacular) adalah sebuah aplikasi yang dapat memprediksi bahasa daerah dan juga dapat digunakan sebagai chatbot.

    Bahasa daerah yang dapat diprediksi oleh aplikasi ini adalah:
    - Bahasa Jawa
    - Bahasa Sunda
    - Bahasa Batak Toba

    Aplikasi ini dibuat oleh:
    |             Name            |      NIM       |
    | --------------------------- | -------------- |
    | Bima Rakajati               | A11.2020.13088 |
    | Enrico Zada                 | A11.2020.12972 |
    | Rosalia Natal Silalahi      | A11.2020.13084 |
    | Devi Kartika Sari           | A11.2020.12518 |
    """)