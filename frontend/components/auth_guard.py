import streamlit as st


def require_auth():
    """Bloque la page si l'utilisateur n'est pas connecté."""
    if "user_id" not in st.session_state or not st.session_state.get("token"):
        st.warning("Vous devez être connecté pour accéder à cette page.")
        st.stop()


def require_admin():
    """Bloque la page si l'utilisateur n'est pas admin ou super_admin."""
    require_auth()
    role = st.session_state.get("role", "")
    if role not in ("admin", "super_admin"):
        st.error("Accès réservé aux administrateurs.")
        st.stop()


def require_super_admin():
    """Bloque la page si l'utilisateur n'est pas super_admin."""
    require_auth()
    if st.session_state.get("role") != "super_admin":
        st.error("Accès réservé au super administrateur.")
        st.stop()


def is_admin() -> bool:
    return st.session_state.get("role") in ("admin", "super_admin")


def is_super_admin() -> bool:
    return st.session_state.get("role") == "super_admin"


def current_user() -> dict:
    return {
        "user_id": st.session_state.get("user_id"),
        "nom":     st.session_state.get("nom"),
        "role":    st.session_state.get("role"),
        "token":   st.session_state.get("token"),
    }