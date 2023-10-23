import pickle
import re
import string
import streamlit as st

with open('model/lrmodel.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

def preprocessing(input_kata):
    translate_table = dict((ord(char), None) for char in string.punctuation)
    result = input_kata.lower()
    result = re.sub(r"\d+", "", result)
    result = result.translate(translate_table)
    return result

def deteksi():
    st.title("Deteksi Bahasa Daerah")

    input_kata = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button("Deteksi")

    if prediksi and input_kata != "" or input_kata:
        input_kata = preprocessing(input_kata)
        predicted_language = loaded_model.predict([input_kata])
        print("Predicted language:", predicted_language)
        if predicted_language[0] == "bataknese":
            predicted_language[0] = "Batak Toba"
        elif predicted_language[0] == "indonesian":
            predicted_language[0] = "Indonesia"
        elif predicted_language[0] == "javanese":
            predicted_language[0] = "Jawa"
        elif predicted_language[0] == "sundanese":
            predicted_language[0] = "Sunda"
        st.write("Prediksi bahasa:", predicted_language[0])

        class_probabilities = loaded_model.predict_proba([input_kata])
        print("Class probabilities:", class_probabilities)

        confidence_score = max(class_probabilities[0])
        st.write(f"Confidence score: `{round(confidence_score * 100, 2)}%`")

        result = [
            ["Batak Toba", class_probabilities[0][0]],
            ["Indonesia", class_probabilities[0][1]],
            ["Jawa", class_probabilities[0][2]],
            ["Sunda", class_probabilities[0][3]]
        ]
        result.sort(key=lambda x: x[1], reverse=True)

        with st.expander("Lihat detail"):
            for i in range(len(result)):
                st.write(f"{result[i][0]}:")
                st.progress(result[i][1])

    elif prediksi and input_kata == "":
        st.error("Masukkan kalimat untuk diprediksi bahasa daerahnya.")