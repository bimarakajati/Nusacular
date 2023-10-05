import streamlit as st
import pickle

with open('model/lrmodel.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

st.title("Prediksi Bahasa Daerah")

input_kata = st.text_input(label="Masukkan kata")
prediksi = st.button ("Prediksi")


if prediksi:
    predicted_language = loaded_model.predict([input_kata])

    class_probabilities = loaded_model.predict_proba([input_kata])

    st.write("Predicted Language:", predicted_language[0])

    confidence_score = max(class_probabilities[0])
    st.write("Confidence Score:", confidence_score)