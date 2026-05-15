import streamlit as st

USER_PAGES = {
    "Chatbot": {"key": "chat",    "icon": "ti-message-circle"},
    "Profil":  {"key": "profile", "icon": "ti-user"},
}

_CSS = """
<style>
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');

section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] { display:none !important; }
section[data-testid="stSidebar"] .stButton { display:none !important; }

/* Toute la chaîne parente doit être height:100% */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div > div,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > div {
    height: 100% !important;
    max-height: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
}

section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 0.5px solid rgba(0,0,0,.08) !important;
}

/* Wrapper principal */
.sb-wrap {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: white;
    overflow: hidden;
}

.sb-head {
    padding: 16px 14px;
    border-bottom: 0.5px solid rgba(0,0,0,.07);
    display: flex; align-items: center; gap: 10px;
    flex-shrink: 0;
}
.sb-logo {
    width: 34px; height: 34px; border-radius: 10px;
    background: #E1F5EE;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.sb-title { font-size: 13px; font-weight: 600; color: #1a1a18; line-height: 1.2; }
.sb-sub   { font-size: 11px; color: #9b9b97; margin-top: 2px; }

.sb-section {
    font-size: 10px; font-weight: 500; color: #b0b0aa;
    letter-spacing: .07em; text-transform: uppercase;
    padding: 14px 14px 6px; flex-shrink: 0;
}

.sb-nav { padding: 0 8px; flex: 1; overflow-y: auto; }

.sb-item {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 10px; margin-bottom: 2px;
    border-radius: 8px; cursor: pointer;
    font-size: 13px; color: #6b6b67;
    text-decoration: none;
}
.sb-item i { font-size: 15px; color: #b0b0aa; flex-shrink: 0; }
.sb-item:hover { background: #f5f5f3; }
.sb-item.active { background: #E1F5EE; }
.sb-item.active .sb-label { color: #085041; font-weight: 600; }
.sb-item.active i { color: #0F6E56; }
.sb-dot {
    margin-left: auto; width: 6px; height: 6px;
    border-radius: 50%; background: #1D9E75; flex-shrink: 0;
}

.sb-footer {
    padding: 10px;
    border-top: 0.5px solid rgba(0,0,0,.07);
    flex-shrink: 0; background: white;
}
.sb-user-card {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 10px; border-radius: 8px;
    background: #f5f5f3; margin-bottom: 8px;
}
.sb-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    background: #E1F5EE; color: #085041;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 600; flex-shrink: 0;
}
.sb-u-name  { font-size: 12px; font-weight: 500; color: #1a1a18; }
.sb-u-email { font-size: 10px; color: #9b9b97; margin-top: 1px; }
.sb-logout {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; padding: 8px; border-radius: 8px;
    border: 0.5px solid rgba(0,0,0,.12);
    background: white; cursor: pointer;
    font-size: 12px; color: #6b6b67;
    font-family: inherit; box-sizing: border-box;
    text-decoration: none;
}
.sb-logout:hover { background: #FCEBEB; color: #A32D2D; border-color: #F09595; }
.sb-logout i { font-size: 14px; }
</style>
"""


def render_user_sidebar() -> str:
    with st.sidebar:
        st.markdown(_CSS, unsafe_allow_html=True)

        if "user_page" not in st.session_state:
            st.session_state.user_page = "chat"

        params = st.query_params

        if "logout" in params:
            st.query_params.clear()
            st.session_state.clear()
            st.switch_page("app.py")

        if "nav" in params:
            nav_val    = params["nav"]
            valid_keys = [v["key"] for v in USER_PAGES.values()]
            if nav_val in valid_keys and nav_val != st.session_state.user_page:
                st.session_state.user_page = nav_val
                st.query_params.clear()
                st.rerun()
            else:
                st.query_params.clear()

        nav_items = ""
        for label, cfg in USER_PAGES.items():
            key    = cfg["key"]
            icon   = cfg["icon"]
            active = st.session_state.user_page == key
            cls    = "sb-item active" if active else "sb-item"
            dot    = '<span class="sb-dot"></span>' if active else ""
            nav_items += (
                f'<a href="?nav={key}" target="_self" class="{cls}">'
                f'<i class="ti {icon}" aria-hidden="true"></i>'
                f'<span class="sb-label">{label}</span>'
                f'{dot}'
                f'</a>'
            )

        nom       = st.session_state.get("nom", "Utilisateur")
        email     = st.session_state.get("email", "")
        initiales = "".join(w[0].upper() for w in nom.split()[:2]) if nom else "U"

        st.markdown(f"""
        <div class="sb-wrap">
            <div class="sb-head">
                <div class="sb-logo">💧</div>
                <div>
                    <div class="sb-title">Assistant TDE</div>
                    <div class="sb-sub">Eau potable au Togo</div>
                </div>
            </div>
            <div class="sb-section">Menu</div>
            <div class="sb-nav">{nav_items}</div>
            <div class="sb-footer">
                <div class="sb-user-card">
                    <div class="sb-avatar">{initiales}</div>
                    <div>
                        <div class="sb-u-name">{nom}</div>
                        <div class="sb-u-email">{email}</div>
                    </div>
                </div>
                <a href="?logout=1" target="_self" class="sb-logout">
                    <i class="ti ti-logout" aria-hidden="true"></i>
                    Déconnexion
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.get("user_page", "chat")