import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)

import streamlit as st
from backend.app.services.chatbot_service import process_message
from datetime import datetime

# ── CONFIG ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Assistant", page_icon="💬", layout="centered")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1rem 0 !important; max-width: 700px !important; }
.stApp { background: #f5f5f3; }

/* header chat */
.ch-header {
    background: #1D9E75;
    border-radius: 14px 14px 0 0;
    padding: 14px 18px;
    display: flex; align-items: center; gap: 12px;
}
.ch-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(255,255,255,.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.ch-name  { font-size: 14px; font-weight: 500; color: white; }
.ch-status { font-size: 11px; color: rgba(255,255,255,.75); display: flex; align-items: center; gap: 5px; }
.online-dot { width: 6px; height: 6px; border-radius: 50%; background: #9FE1CB; display: inline-block; }

/* zone messages */
.messages-zone {
    background: #fafafa;
    border-left: 0.5px solid rgba(0,0,0,.1);
    border-right: 0.5px solid rgba(0,0,0,.1);
    padding: 16px;
    min-height: 380px;
    max-height: 500px;
    overflow-y: auto;
    display: flex; flex-direction: column; gap: 12px;
    scroll-behavior: smooth;
}
.messages-zone::-webkit-scrollbar { width: 4px; }
.messages-zone::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 2px; }
.messages-zone::-webkit-scrollbar-track { background: transparent; }

/* bulles */
.msg-row      { display: flex; gap: 8px; align-items: flex-end; }
.msg-row.user { flex-direction: row-reverse; }
.av {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 500; flex-shrink: 0;
}
.av.bot  { background: #E1F5EE; color: #085041; }
.av.user { background: #eeede9; color: #6b6b67; }
.bwrap      { display: flex; flex-direction: column; max-width: 75%; }
.bwrap.user { align-items: flex-end; }
.bubble {
    padding: 10px 14px; border-radius: 14px;
    font-size: 14px; line-height: 1.55; word-break: break-word;
}
.bubble.bot  {
    background: #fff; border: 0.5px solid rgba(0,0,0,.10);
    color: #1a1a18; border-bottom-left-radius: 3px;
}
.bubble.user {
    background: #1D9E75; color: white;
    border-bottom-right-radius: 3px;
}
.bubble.error { background: #FCEBEB; border-color: #F7C1C1; color: #A32D2D; }
.msg-time { font-size: 10px; color: #a0a09c; margin-top: 3px; padding: 0 2px; }

/* footer panel */
.ch-footer {
    background: #fff;
    border: 0.5px solid rgba(0,0,0,.1);
    border-top: none;
    border-radius: 0 0 14px 14px;
    padding: 6px 16px 10px;
    text-align: center;
}
.ch-footer span { font-size: 10px; color: #a0a09c; }

/* input Streamlit */
.stTextInput > div > div > input {
    border-radius: 24px !important;
    border: 0.5px solid rgba(0,0,0,.18) !important;
    padding: 10px 18px !important;
    font-size: 14px !important;
    background: #f5f5f3 !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1D9E75 !important;
    box-shadow: 0 0 0 2px rgba(29,158,117,.12) !important;
}
.stButton > button {
    border-radius: 24px !important;
    background: #1D9E75 !important;
    color: white !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    box-shadow: none !important;
}
.stButton > button:hover { background: #0F6E56 !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Bonjour ! Comment puis-je vous aider ?", "time": ""}
    ]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ch-header">
  <div class="ch-avatar">🤖</div>
  <div>
    <div class="ch-name">Assistant</div>
    <div class="ch-status"><span class="online-dot"></span> En ligne</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MESSAGES ──────────────────────────────────────────────────────────────────
html = '<div class="messages-zone">'
for msg in st.session_state.messages:
    text = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    t    = msg.get("time", "")
    err  = msg.get("error", False)
    if msg["role"] == "bot":
        html += f"""
        <div class="msg-row">
          <div class="av bot">N</div>
          <div class="bwrap">
            <div class="bubble bot{' error' if err else ''}">{text}</div>
            <div class="msg-time">{t}</div>
          </div>
        </div>"""
    else:
        html += f"""
        <div class="msg-row user">
          <div class="av user">V</div>
          <div class="bwrap user">
            <div class="bubble user">{text}</div>
            <div class="msg-time">{t}</div>
          </div>
        </div>"""
html += "</div>"
st.markdown(html, unsafe_allow_html=True)

# Auto-scroll vers le dernier message
st.markdown("""
<script>
  const zone = document.querySelector('.messages-zone');
  if (zone) zone.scrollTop = zone.scrollHeight;
</script>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ch-footer">
  <span>🔒 Chiffré de bout en bout</span>
</div>
""", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_message = st.text_input("message", label_visibility="collapsed", placeholder="Votre message…")
with col2:
    send = st.button("Envoyer", use_container_width=True)

# ── LOGIQUE ───────────────────────────────────────────────────────────────────
if send and user_message.strip():
    now = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user",
        "content": user_message.strip(),
        "time": now
    })

    try:
        response = process_message(
            user_message=user_message.strip(),
            session_id="session_1",
            user_id="user_1"
        )
        st.session_state.messages.append({
            "role": "bot",
            "content": response,
            "time": datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        st.session_state.messages.append({
            "role": "bot",
            "content": f"Erreur : {str(e)}",
            "time": datetime.now().strftime("%H:%M"),
            "error": True
        })

    st.rerun()
