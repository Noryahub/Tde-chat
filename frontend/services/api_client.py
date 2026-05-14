import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:5000"

TIMEOUT = 10


def _headers() -> dict:

    token = st.session_state.get(
        "token",
        ""
    )

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# =========================================
# POST
# =========================================

def post(
    endpoint: str,
    payload: dict,
    auth: bool = False
) -> dict | None:

    try:

        headers = (
            _headers()
            if auth
            else {"Content-Type": "application/json"}
        )

        resp = requests.post(
            f"{BASE_URL}{endpoint}",
            json=payload,
            headers=headers,
            timeout=TIMEOUT
        )

        return resp.json()

    except Exception as e:

        st.error(
            f"Erreur réseau : {e}"
        )

        return None


# =========================================
# GET
# =========================================

def get(endpoint: str) -> dict | None:

    try:

        resp = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=_headers(),
            timeout=TIMEOUT
        )

        return resp.json()

    except Exception as e:

        st.error(
            f"Erreur réseau : {e}"
        )

        return None


# =========================================
# PATCH
# =========================================

def patch(
    endpoint: str,
    payload: dict
) -> dict | None:

    try:

        resp = requests.patch(
            f"{BASE_URL}{endpoint}",
            json=payload,
            headers=_headers(),
            timeout=TIMEOUT
        )

        return resp.json()

    except Exception as e:

        st.error(
            f"Erreur réseau : {e}"
        )

        return None


# =========================================
# DELETE
# =========================================

def delete(endpoint: str) -> dict | None:

    try:

        resp = requests.delete(
            f"{BASE_URL}{endpoint}",
            headers=_headers(),
            timeout=TIMEOUT
        )

        return resp.json()

    except Exception as e:

        st.error(
            f"Erreur réseau : {e}"
        )

        return None