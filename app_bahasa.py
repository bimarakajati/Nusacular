import streamlit as st
from nusacular import *
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Nusacular",
    page_icon="✨"
)

with st.sidebar:
    selected = option_menu(
        "Nusacular",
        ['Deteksi Bahasa Daerah', 'Chatbot', 'Sentimen', 'About Us'],
        icons=['flag', 'robot', 'emoji-smile', 'person-fill'],
        default_index=0
    )

if selected == "Deteksi Bahasa Daerah":
    deteksi()

elif selected == "Chatbot":
    chatbot()

elif selected == "Sentimen":
    sentimen()

else:
    about_us()