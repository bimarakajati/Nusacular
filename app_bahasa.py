import pickle
import g4f
import streamlit as st
from streamlit_option_menu import option_menu


role = [
    'system',
    "user",
    "assistant",
    "user",
]

# navigas sidebar
with st.sidebar:
    selected = option_menu("Nusacular", 
                           ['Prediksi Bahasa Daerah', 'Chatbot'],
                           icons=['flag', 'robot'],
                           default_index=0)

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
else:
    st.title("Nusacular Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Mau tanya apa?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        while True:
            response = g4f.ChatCompletion.create(
                        model='gpt-3.5-turbo',
                        messages=[{"role": role[1], "content": prompt}]
                    )
            if response == '':
                continue
            else:
                break
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})