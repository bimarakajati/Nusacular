import pickle
import streamlit as st

with open('model/mnbmodel.sav', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

def deteksi():
    st.title("Deteksi Bahasa Daerah")

    input_kata = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button("Deteksi")

    if prediksi or input_kata != "":
        predicted_language = loaded_model.predict([input_kata])
        print("Predicted language:", predicted_language)
        st.write("Predicted Language:", predicted_language[0])

        class_probabilities = loaded_model.predict_proba([input_kata])
        print("Class probabilities:", class_probabilities)

        confidence_score = max(class_probabilities[0])
        st.write("Confidence Score:", confidence_score)

        with st.expander("Lihat detail"):
            bahasa = ['Aceh', 'Bali', 'Banjar', 'Bugis', 'Jawa', 'Madura', 'Minang', 'Ngaju', 'Sunda', 'Batak']
            for i in range(len(bahasa)):
                st.write(f'{bahasa[i]}:')
                st.progress(class_probabilities[0][i])
