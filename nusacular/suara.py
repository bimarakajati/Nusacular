from gtts import gTTS
import streamlit as st

def text2speech():
    st.title("Suara Bahasa Daerah")

    language = st.selectbox(
    'Pilih bahasa daerah:',
    ('Jawa', 'Sunda'))
    
    if language == 'Jawa':
        bahasa = "jw"
    elif language == 'Sunda':
        bahasa = "su"

    teks_asal = st.text_input(label="Masukkan kalimat:")
    prediksi = st.button ("Suarakan")

    if prediksi or teks_asal != "":
        suara = gTTS(text=teks_asal, lang=bahasa, slow=False)
        # Simpan suara ke dalam file
        suara.save("output.mp3")

        st.write("Hasil:")
        st.audio("output.mp3")