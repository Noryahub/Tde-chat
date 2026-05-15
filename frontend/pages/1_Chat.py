import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)

import streamlit as st
from frontend.components.user_sidebar import render_user_sidebar

# ── CONFIG
st.set_page_config(page_title="Assistant TDE", page_icon="💬", layout="wide")

# ── SIDEBAR
render_user_sidebar()

# ── CONTENU
st.title("Chat utilisateur")
st.write("Bienvenue")