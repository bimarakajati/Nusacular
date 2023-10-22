import streamlit as st
from nusacular.deteksi import deteksi
from nusacular.chatbot import chatbot
from nusacular.about import about_us
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Nusacular",
    page_icon="✨"
)

with st.sidebar:
    selected = option_menu(
        "Nusacular",
        ['Deteksi Bahasa Daerah', 'Chatbot', 'Tentang Kami'],
        icons=['flag', 'robot', "person-fill"],
        default_index=0
    )

if selected == "Deteksi Bahasa Daerah":
    deteksi()

elif selected == "Chatbot":
    chatbot()

else:
    about_us()