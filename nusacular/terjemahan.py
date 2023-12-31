from googletrans import Translator
import streamlit as st

def terjemahkan(teks, bahasa_sumber, bahasa_target):
    translator = Translator()
    terjemahan = translator.translate(teks, src=bahasa_sumber, dest=bahasa_target)
    return terjemahan.text

bahasa_sumber = "id"  # Bahasa sumber (Indonesia)

def translate():
    st.title("Terjemahan Bahasa Daerah")

    language = st.selectbox(
    'Pilih bahasa daerah:',
    ('Jawa', 'Sunda'))
    
    if language == 'Jawa':
        bahasa_target = "jw"
    elif language == 'Sunda':
        bahasa_target = "su"

    teks_asal = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button ("Terjemahkan")

    if prediksi or teks_asal != "":
        terjemahan = terjemahkan(teks_asal, bahasa_sumber, bahasa_target)

        # print('Selected language:', bahasa_target)
        # st.write('Selected language:', bahasa_target)
        print("Terjemahan:", terjemahan)
        st.write("Terjemahan:", terjemahan)