import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../"
        )
    )
)

import streamlit as st

from frontend.services.auth_client import (
    login,
    register
)

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="TDE Chatbot",
    page_icon="💧",
    layout="centered"
)
st.markdown("""
<style>

/* Cache complètement le sidebar Streamlit */
[data-testid="stSidebar"] {
    display: none;
}

/* Supprime l’espace laissé par le sidebar */
[data-testid="stAppViewContainer"] {
    margin-left: 0rem;
}

</style>
""", unsafe_allow_html=True)
# =========================================
# SESSION STATE
# =========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "role" not in st.session_state:
    st.session_state.role = None

if "token" not in st.session_state:
    st.session_state.token = None

# =========================================
# REDIRECTION
# =========================================

if st.session_state.authenticated:

    # ADMIN
    if st.session_state.role == "admin":

        st.switch_page(
            "pages/dashboard.py"
        )

    # USER
    else:

        st.switch_page(
            "pages/chat.py"
        )

# =========================================
# HEADER
# =========================================

st.markdown("""
<div style='text-align:center; padding-top:40px;'>

<h1>
💧 Assistant Virtuel TDE
</h1>

<p>
Plateforme intelligente d’assistance client
</p>

</div>
""", unsafe_allow_html=True)

# =========================================
# TABS
# =========================================

tab_login, tab_register = st.tabs(
    [
        "Connexion",
        "Inscription"
    ]
)

# =========================================
# LOGIN
# =========================================

with tab_login:

    st.subheader("Connexion")

    login_email = st.text_input(
        "Email",
        key="login_email"
    )

    login_password = st.text_input(
        "Mot de passe",
        type="password",
        key="login_password"
    )

    if st.button(
        "Se connecter",
        use_container_width=True
    ):

        if not login_email or not login_password:

            st.warning(
                "Veuillez remplir tous les champs"
            )

        else:

            result = login(
                email=login_email,
                password=login_password
            )

            if (
                result and
                result.get("status") == "success"
            ):

                user = result["user"]

                st.session_state.authenticated = True

                st.session_state.user_id = user["id"]

                st.session_state.role = user["role"]

                # futur JWT
                st.session_state.token = result.get(
                    "token"
                )

                st.success(
                    "Connexion réussie"
                )

                st.rerun()

            else:

                message = (
                    result.get("message")
                    if result
                    else "Serveur inaccessible"
                )

                st.error(message)

# =========================================
# REGISTER
# =========================================

with tab_register:

    st.subheader("Créer un compte")

    register_nom = st.text_input(
        "Nom",
        key="register_nom"
    )

    register_email = st.text_input(
        "Email",
        key="register_email"
    )

    register_password = st.text_input(
        "Mot de passe",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirmer le mot de passe",
        type="password",
        key="confirm_password"
    )

    if st.button(
        "Créer un compte",
        use_container_width=True
    ):

        if (
            not register_nom or
            not register_email or
            not register_password
        ):

            st.warning(
                "Veuillez remplir tous les champs"
            )

        elif register_password != confirm_password:

            st.warning(
                "Les mots de passe ne correspondent pas"
            )

        else:

            result = register(
                nom=register_nom,
                email=register_email,
                password=register_password
            )

            if (
                result and
                result.get("status") == "success"
            ):

                st.success(
                    "Compte créé avec succès"
                )

                st.info(
                    "Vous pouvez maintenant vous connecter."
                )

            else:

                message = (
                    result.get("message")
                    if result
                    else "Serveur inaccessible"
                )

                st.error(message)

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "© 2026 - Société Togolaise des Eaux"
)