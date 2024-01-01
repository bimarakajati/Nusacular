import streamlit as st
from streamlit_option_menu import option_menu
from nusacular.about import about_us
from nusacular.chatbot import chatbot
from nusacular.deteksi import deteksi
from nusacular.sentimen import sentimen
from nusacular.suara import text2speech
from nusacular.terjemahan import translate

st.set_page_config(
    page_title="Nusacular",
    page_icon="✨"
)

with st.sidebar:
    selected = option_menu(
        "Nusacular",
        ['Deteksi Bahasa Daerah', 'Chatbot', 'Terjemahan', 'Suara', 'Sentimen', 'Tentang Kami'],
        icons=['flag', 'robot', 'translate', 'soundwave', 'emoji-smile', 'person-fill'],
        default_index=0
    )

if selected == "Deteksi Bahasa Daerah":
    deteksi()

elif selected == "Chatbot":
    chatbot()

elif selected == "Terjemahan":
    translate()

elif selected == "Suara":
    text2speech()

elif selected == "Sentimen":
    sentimen()

else:
    about_us()