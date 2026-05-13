import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import streamlit as st

st.set_page_config(page_title="TDE Chatbot", page_icon="💧", layout="centered")

st.markdown("""
<div style="text-align:center; padding: 40px;">
    <h2>💧 Assistant Virtuel TDE</h2>
    <p>Choisissez une section dans le menu à gauche</p>
</div>
""", unsafe_allow_html=True)