import streamlit as st
import streamlit.components.v1 as components


CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'DM Sans', sans-serif; background: #fafafa; overflow: hidden; }

.chat-wrapper { position: relative; height: 500px; }

.messages-zone {
    padding: 16px; height: 500px; overflow-y: auto;
    display: flex; flex-direction: column; gap: 12px;
    scroll-behavior: smooth;
    border-left: 0.5px solid rgba(0,0,0,.1);
    border-right: 0.5px solid rgba(0,0,0,.1);
}
.messages-zone::-webkit-scrollbar { width: 4px; }
.messages-zone::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 2px; }

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
.bubble.user { background: #1D9E75; color: white; border-bottom-right-radius: 3px; }
.bubble.error { background: #FCEBEB; border-color: #F7C1C1; color: #A32D2D; }
.msg-time { font-size: 10px; color: #a0a09c; margin-top: 3px; padding: 0 2px; }

.typing-bubble {
    background: #fff; border: 0.5px solid rgba(0,0,0,.10);
    border-radius: 14px; border-bottom-left-radius: 3px;
    padding: 12px 16px; display: inline-flex; align-items: center; gap: 5px;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #1D9E75; animation: bounce 1.2s infinite ease-in-out;
}
.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0);   opacity: 0.4; }
    30%            { transform: translateY(-6px); opacity: 1;   }
}

.scroll-btn {
    position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
    width: 36px; height: 36px; border-radius: 50%;
    background: #fff; border: 0.5px solid rgba(0,0,0,.15);
    cursor: pointer; display: none; align-items: center; justify-content: center;
    box-shadow: 0 2px 10px rgba(0,0,0,.12);
    transition: box-shadow 0.2s; z-index: 100;
}
.scroll-btn:hover { box-shadow: 0 4px 16px rgba(0,0,0,.18); }
.scroll-btn.visible { display: flex; animation: fadeInUp 0.2s ease; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateX(-50%) translateY(8px); }
    to   { opacity: 1; transform: translateX(-50%) translateY(0);   }
}
.badge {
    position: absolute; top: -4px; right: -4px;
    background: #e53e3e; color: white;
    font-size: 9px; font-weight: 700; width: 16px; height: 16px;
    border-radius: 50%; display: none;
    align-items: center; justify-content: center; border: 1.5px solid white;
}
.badge.show { display: flex; }
"""

SCROLL_JS = """
const zone  = document.getElementById('msgZone');
const btn   = document.getElementById('scrollBtn');
const badge = document.getElementById('badge');
const THRESHOLD = 60;
function isAtBottom() {
  return zone.scrollHeight - zone.scrollTop - zone.clientHeight < THRESHOLD;
}
function updateBtn() {
  if (isAtBottom()) { btn.classList.remove('visible'); badge.classList.remove('show'); }
  else              { btn.classList.add('visible'); }
}
function scrollToBottom() {
  zone.scrollTo({ top: zone.scrollHeight, behavior: 'smooth' });
  badge.classList.remove('show');
  btn.classList.remove('visible');
}
zone.scrollTop = zone.scrollHeight;
zone.addEventListener('scroll', updateBtn);
const observer = new MutationObserver(function() {
  if (!isAtBottom()) { btn.classList.add('visible'); badge.classList.add('show'); }
  else               { scrollToBottom(); }
});
observer.observe(zone, { childList: true, subtree: false });
updateBtn();
"""


def _build_bubbles(messages: list, show_typing: bool, bot_initial: str = "N") -> str:
    html = ""
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
            html += f"""
            <div class="msg-row">
              <div class="av bot">{bot_initial}</div>
              <div class="bwrap">
                <div class="{cls}">{text}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
        else:
            user_initial = str(msg.get("initial", "V"))
            html += f"""
            <div class="msg-row user">
              <div class="av user">{user_initial}</div>
              <div class="bwrap user">
                <div class="bubble user">{text}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""

    if show_typing:
        html += f"""
        <div class="msg-row">
          <div class="av bot">{bot_initial}</div>
          <div class="bwrap">
            <div class="typing-bubble">
              <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
          </div>
        </div>"""
    return html


def build_chat_html(messages: list, show_typing: bool = False,
                    bot_initial: str = "N") -> str:
    bubbles = _build_bubbles(messages, show_typing, bot_initial)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
<div class="chat-wrapper">
  <div class="messages-zone" id="msgZone">
    {bubbles}
  </div>
  <button class="scroll-btn" id="scrollBtn" onclick="scrollToBottom()" title="Aller en bas">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M8 2 L8 11" stroke="#444" stroke-width="1.6" stroke-linecap="round"/>
      <path d="M4.5 7.5 L8 11 L11.5 7.5" stroke="#444" stroke-width="1.6"
            stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="3" y1="14" x2="13" y2="14" stroke="#444"
            stroke-width="1.6" stroke-linecap="round"/>
    </svg>
    <span class="badge" id="badge"></span>
  </button>
</div>
<script>{SCROLL_JS}</script>
</body></html>"""


def render_chat_zone(messages: list, show_typing: bool = False,
                     bot_initial: str = "N", height: int = 500):
    """Rend la zone de chat via components.html."""
    components.html(
        build_chat_html(messages, show_typing, bot_initial),
        height=height,
        scrolling=False
    )


def render_chat_header():
    """Header vert du chatbot."""
    st.markdown("""
    <div style="
        background: #1D9E75; border-radius: 14px 14px 0 0;
        padding: 14px 18px; display: flex; align-items: center; gap: 12px;
    ">
      <div style="width:38px; height:38px; border-radius:50%; background:rgba(255,255,255,.2);
                  display:flex; align-items:center; justify-content:center; font-size:18px;">🤖</div>
      <div>
        <div style="font-size:14px; font-weight:500; color:white;">Assistant TDE</div>
        <div style="font-size:11px; color:rgba(255,255,255,.75); display:flex; align-items:center; gap:5px;">
          <span style="width:6px; height:6px; border-radius:50%; background:#9FE1CB; display:inline-block;"></span>
          En ligne
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_footer():
    st.markdown("""
    <div style="background:#fff; border:0.5px solid rgba(0,0,0,.1); border-top:none;
                border-radius:0 0 14px 14px; padding:6px 16px 10px; text-align:center;">
      <span style="font-size:10px; color:#a0a09c;">🔒 Chiffré de bout en bout</span>
    </div>
    """, unsafe_allow_html=True)