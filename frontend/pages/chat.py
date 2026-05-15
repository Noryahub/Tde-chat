import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(BASE_DIR)

# ⚡ Tous les imports EN HAUT avant set_page_config
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from frontend.components.user_sidebar import render_user_sidebar  # ← ici
from backend.app.services.chatbot_service import process_message

# ── CONFIG — doit rester le premier appel Streamlit
st.set_page_config(page_title="Assistant TDE", page_icon="💬", layout="wide")

# ── SIDEBAR
render_user_sidebar()
# ── CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar natif */
section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid rgba(0,0,0,.08) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem !important;
}

/* Contenu principal */
.block-container {
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 760px !important;
}

.stApp { background: #f5f5f3; }

/* Header chat */
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
.ch-name   { font-size: 14px; font-weight: 500; color: white; }
.ch-status {
    font-size: 11px; color: rgba(255,255,255,.75);
    display: flex; align-items: center; gap: 5px;
}
.online-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #9FE1CB; display: inline-block;
}

/* Footer chat */
.ch-footer {
    background: #fff;
    border: 0.5px solid rgba(0,0,0,.1);
    border-top: none;
    border-radius: 0 0 14px 14px;
    padding: 6px 16px 10px;
    text-align: center;
}
.ch-footer span { font-size: 10px; color: #a0a09c; }

/* Input */
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

/* Bouton envoyer */
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

iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Bonjour ! Comment puis-je vous aider ?", "time": ""}
    ]


# ── HELPER
def build_chat_html(messages: list, show_typing: bool = False) -> str:
    bubbles = ""
    for msg in messages:
        text = (
            msg["content"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )
        t   = msg.get("time", "")
        err = msg.get("error", False)
        if msg["role"] == "bot":
            cls = "bubble bot error" if err else "bubble bot"
            bubbles += f"""
            <div class="msg-row">
              <div class="av bot">N</div>
              <div class="bwrap">
                <div class="{cls}">{text}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
        else:
            bubbles += f"""
            <div class="msg-row user">
              <div class="av user">V</div>
              <div class="bwrap user">
                <div class="bubble user">{text}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""

    typing_html = ""
    if show_typing:
        typing_html = """
        <div class="msg-row">
          <div class="av bot">N</div>
          <div class="bwrap">
            <div class="typing-bubble">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'DM Sans', sans-serif; background: #fafafa; overflow: hidden; }}
  .chat-wrapper {{ position: relative; height: 500px; }}
  .messages-zone {{
    padding: 16px; height: 500px; overflow-y: auto;
    display: flex; flex-direction: column; gap: 12px;
    scroll-behavior: smooth;
    border-left: 0.5px solid rgba(0,0,0,.1);
    border-right: 0.5px solid rgba(0,0,0,.1);
  }}
  .messages-zone::-webkit-scrollbar {{ width: 4px; }}
  .messages-zone::-webkit-scrollbar-thumb {{ background: rgba(0,0,0,0.15); border-radius: 2px; }}
  .msg-row      {{ display: flex; gap: 8px; align-items: flex-end; }}
  .msg-row.user {{ flex-direction: row-reverse; }}
  .av {{ width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 500; flex-shrink: 0; }}
  .av.bot  {{ background: #E1F5EE; color: #085041; }}
  .av.user {{ background: #eeede9; color: #6b6b67; }}
  .bwrap      {{ display: flex; flex-direction: column; max-width: 75%; }}
  .bwrap.user {{ align-items: flex-end; }}
  .bubble {{ padding: 10px 14px; border-radius: 14px; font-size: 14px; line-height: 1.55; word-break: break-word; }}
  .bubble.bot  {{ background: #fff; border: 0.5px solid rgba(0,0,0,.10); color: #1a1a18; border-bottom-left-radius: 3px; }}
  .bubble.user {{ background: #1D9E75; color: white; border-bottom-right-radius: 3px; }}
  .bubble.error {{ background: #FCEBEB; border-color: #F7C1C1; color: #A32D2D; }}
  .msg-time {{ font-size: 10px; color: #a0a09c; margin-top: 3px; padding: 0 2px; }}
  .typing-bubble {{
    background: #fff; border: 0.5px solid rgba(0,0,0,.10);
    border-radius: 14px; border-bottom-left-radius: 3px;
    padding: 12px 16px; display: inline-flex; align-items: center; gap: 5px;
  }}
  .dot {{ width: 7px; height: 7px; border-radius: 50%; background: #1D9E75; animation: bounce 1.2s infinite ease-in-out; }}
  .dot:nth-child(1) {{ animation-delay: 0s; }}
  .dot:nth-child(2) {{ animation-delay: 0.2s; }}
  .dot:nth-child(3) {{ animation-delay: 0.4s; }}
  @keyframes bounce {{
    0%, 60%, 100% {{ transform: translateY(0); opacity: 0.4; }}
    30%            {{ transform: translateY(-6px); opacity: 1; }}
  }}
  .scroll-btn {{
    position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
    width: 36px; height: 36px; border-radius: 50%;
    background: #fff; border: 0.5px solid rgba(0,0,0,.15);
    cursor: pointer; display: none; align-items: center; justify-content: center;
    box-shadow: 0 2px 10px rgba(0,0,0,.12); z-index: 100;
  }}
  .scroll-btn.visible {{ display: flex; }}
  .badge {{
    position: absolute; top: -4px; right: -4px;
    background: #e53e3e; color: white; font-size: 9px; font-weight: 700;
    width: 16px; height: 16px; border-radius: 50%;
    display: none; align-items: center; justify-content: center;
    border: 1.5px solid white;
  }}
  .badge.show {{ display: flex; }}
</style>
</head>
<body>
<div class="chat-wrapper">
  <div class="messages-zone" id="msgZone">
    {bubbles}
    {typing_html}
  </div>
  <button class="scroll-btn" id="scrollBtn" onclick="scrollToBottom()">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M8 2 L8 11" stroke="#444" stroke-width="1.6" stroke-linecap="round"/>
      <path d="M4.5 7.5 L8 11 L11.5 7.5" stroke="#444" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="3" y1="14" x2="13" y2="14" stroke="#444" stroke-width="1.6" stroke-linecap="round"/>
    </svg>
    <span class="badge" id="badge"></span>
  </button>
</div>
<script>
  const zone  = document.getElementById('msgZone');
  const btn   = document.getElementById('scrollBtn');
  const badge = document.getElementById('badge');
  const THRESHOLD = 60;
  function isAtBottom() {{ return zone.scrollHeight - zone.scrollTop - zone.clientHeight < THRESHOLD; }}
  function updateBtn()  {{ btn.classList.toggle('visible', !isAtBottom()); }}
  function scrollToBottom() {{
    zone.scrollTo({{ top: zone.scrollHeight, behavior: 'smooth' }});
    badge.classList.remove('show');
    btn.classList.remove('visible');
  }}
  zone.scrollTop = zone.scrollHeight;
  zone.addEventListener('scroll', updateBtn);
  new MutationObserver(function() {{
    if (!isAtBottom()) {{ btn.classList.add('visible'); badge.classList.add('show'); }}
    else {{ scrollToBottom(); }}
  }}).observe(zone, {{ childList: true }});
  updateBtn();
</script>
</body>
</html>"""


# ── HEADER
st.markdown("""
<div class="ch-header">
  <div class="ch-avatar">🤖</div>
  <div>
    <div class="ch-name">Assistant TDE</div>
    <div class="ch-status"><span class="online-dot"></span> En ligne</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ZONE MESSAGES
chat_placeholder = st.empty()

with chat_placeholder:
    components.html(
        build_chat_html(st.session_state.messages, show_typing=False),
        height=500,
        scrolling=False
    )

# ── FOOTER
st.markdown("""
<div class="ch-footer">
  <span>🔒 Chiffré de bout en bout</span>
</div>
""", unsafe_allow_html=True)

# ── INPUT
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_message = st.text_input(
        "message",
        label_visibility="collapsed",
        placeholder="Votre message…"
    )
with col2:
    send = st.button("Envoyer", use_container_width=True)

# ── LOGIQUE
if send and user_message.strip():
    now = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user",
        "content": user_message.strip(),
        "time": now
    })

    with chat_placeholder:
        components.html(
            build_chat_html(st.session_state.messages, show_typing=True),
            height=500,
            scrolling=False
        )

    try:
        response = process_message(
            user_message=user_message.strip(),
            session_id=st.session_state.get("session_id", "session_1"),
            user_id=st.session_state.get("user_id", "user_1")
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