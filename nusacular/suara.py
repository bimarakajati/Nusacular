from gtts import gTTS
import streamlit as st

def text2speech():
    st.title("Suara Bahasa Daerah")

    language = st.selectbox(
    'Pilih bahasa daerah:',
    ('javanese', 'sundanese'))
    
    if language == 'javanese':
        bahasa = "jw"
    elif language == 'sundanese':
        bahasa = "su"

    teks_asal = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button ("Terjemahkan")

    if prediksi:
        suara = gTTS(text=teks_asal, lang=bahasa, slow=False)
        # Simpan suara ke dalam file
        suara.save("output.mp3")

        st.write("Hasil:")
        st.audio("output.mp3")