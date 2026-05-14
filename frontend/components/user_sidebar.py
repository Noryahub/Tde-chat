import streamlit as st


USER_PAGES = {
    "Chatbot": "chat",
    "Profil":  "profile",
}


def render_user_sidebar() -> str:
    """
    Affiche la sidebar utilisateur et retourne la page sélectionnée.
    """
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 16px 0 8px;">
            <div style="font-size:32px;">🤖</div>
            <div style="font-size:15px; font-weight:600; color:#1a1a18;">Assistant TDE</div>
            <div style="font-size:11px; color:#a0a09c; margin-top:2px;">Eau potable au Togo</div>
        </div>
        <hr style="border:none; border-top:0.5px solid rgba(0,0,0,.1); margin:8px 0 16px;">
        """, unsafe_allow_html=True)

        if "user_page" not in st.session_state:
            st.session_state.user_page = "chat"

        for label, page_key in USER_PAGES.items():
            is_active = st.session_state.user_page == page_key
            if st.button(
                label,
                key=f"user_nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.user_page = page_key
                st.rerun()

        st.markdown("<hr style='border:none; border-top:0.5px solid rgba(0,0,0,.1); margin-top:auto;'>",
                    unsafe_allow_html=True)

        nom = st.session_state.get("nom") or "Utilisateur"
        st.markdown(f"""
        <div style="padding: 8px 4px; font-size:12px; color:#6b6b67;">
            Connecté en tant que<br>
            <strong style="color:#1a1a18;">{nom}</strong>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Déconnexion", use_container_width=True):
            for key in ["user_id", "token", "role", "nom",
                        "session_id", "messages", "user_page"]:
                st.session_state.pop(key, None)
            st.rerun()

    return st.session_state.get("user_page", "chat")