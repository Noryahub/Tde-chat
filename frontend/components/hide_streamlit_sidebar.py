import streamlit as st


def hide_streamlit_sidebar():

    st.markdown("""
    <style>

    /* Cache navigation automatique Streamlit */
    section[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Cache bouton collapse */
    button[kind="header"] {
        display: none !important;
    }

    </style>
    """, unsafe_allow_html=True)
