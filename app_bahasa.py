import streamlit as st
from nusacular.deteksi import deteksi
from nusacular.chatbot import chatbot
# from nusacular.sentimen import sentimen
from nusacular.terjemahan import translate
from nusacular.suara import text2speech
from nusacular.about import about_us
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Nusacular",
    page_icon="✨"
)

with st.sidebar:
    selected = option_menu(
        "Nusacular",
        ['Deteksi Bahasa Daerah', 'Terjemahan', 'Suara', 'Chatbot', 'Tentang Kami'],
        icons=['flag', 'translate', 'soundwave', 'robot', 'person-fill'],
        # ['Deteksi Bahasa Daerah', 'Terjemahan', 'Suara', 'Chatbot', 'Sentimen', 'Tentang Kami'],
        # icons=['flag', 'translate', 'soundwave', 'robot', 'emoji-smile', 'person-fill'],
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

# elif selected == "Sentimen":
#     sentimen()

else:
    about_us()