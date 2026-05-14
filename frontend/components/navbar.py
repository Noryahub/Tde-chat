import streamlit as st


def render_navbar(title: str = "Assistant TDE"):
    nom  = st.session_state.get("nom") or st.session_state.get("email", "Utilisateur")
    role = st.session_state.get("role", "user")

    role_badge = {
        "super_admin": ("⭐Super Admin", "#7C3AED"),
        "admin":       ("🛡️Admin",       "#1D9E75"),
        "user":        ("👤Utilisateur", "#6b6b67"),
    }.get(role, ("👤 Utilisateur", "#6b6b67"))

    st.markdown(f"""
    <div style="
        background: #1D9E75;
        padding: 12px 24px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    ">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:22px;">🤖</span>
            <span style="color:white; font-size:16px; font-weight:600;">{title}</span>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="
                background: rgba(255,255,255,0.15);
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">{role_badge[0]}</span>
            <span style="color: rgba(255,255,255,0.9); font-size:13px;">{nom}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)