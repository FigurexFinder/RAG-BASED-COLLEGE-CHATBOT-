import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Chat Assistant", page_icon="🤖", layout="centered")

API_URL = "http://localhost:8000/chat"

# ── Session state ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark = st.session_state.dark_mode

# ── Theme tokens ────────────────────────────────────────────────────────────────
if dark:
    BG               = "#0f1623"
    DOODLE_STROKE    = "#3b82f6"
    DOODLE_OPACITY   = "0.18"
    HEADER_BG        = "rgba(255,255,255,0.04)"
    HEADER_BORD      = "rgba(255,255,255,0.08)"
    TITLE_COL        = "#e2e8f0"
    STATUS_COL       = "#60a5fa"
    AI_BUBBLE        = "rgba(255,255,255,0.06)"
    AI_BORD          = "rgba(255,255,255,0.10)"
    AI_TEXT          = "#e2e8f0"
    HU_BUBBLE        = "rgba(59,130,246,0.18)"
    HU_BORD          = "1px solid rgba(59,130,246,0.30)"
    HU_TEXT          = "#dbeafe"
    HU_SHADOW        = "0 2px 12px rgba(59,130,246,0.15)"
    INPUT_BG         = "#ffffff"
    INPUT_TEXT       = "#0f172a"
    INPUT_PH         = "#4b5563"
    INPUT_BORD       = "rgba(255,255,255,0.10)"
    INPUT_FOCUS      = "rgba(96,165,250,0.50)"
    INPUT_FOCUS_GLOW = "rgba(59,130,246,0.10)"
    SEND_BTN         = "#2563eb"
    CARET            = "#60a5fa"
    SCROLL_THUMB     = "rgba(96,165,250,0.15)"
    AV_AI_BG         = "#1d4ed8"
    AV_HU_BG         = "rgba(255,255,255,0.08)"
    AV_HU_BR         = "rgba(255,255,255,0.15)"
    TOGGLE_LABEL     = "#60a5fa"
    TOGGLE_ICON      = "☀️"
else:
    BG               = "#e8f0f8"
    DOODLE_STROKE    = "#7bafd4"
    DOODLE_OPACITY   = "0.22"
    HEADER_BG        = "#ffffff"
    HEADER_BORD      = "rgba(0,0,0,0.07)"
    TITLE_COL        = "#0f172a"
    STATUS_COL       = "#2563eb"
    AI_BUBBLE        = "#ffffff"
    AI_BORD          = "rgba(0,0,0,0.07)"
    AI_TEXT          = "#1e293b"
    HU_BUBBLE        = "#dbeafe"
    HU_BORD          = "1px solid rgba(59,130,246,0.20)"
    HU_TEXT          = "#1e3a5f"
    HU_SHADOW        = "0 2px 10px rgba(59,130,246,0.10)"
    INPUT_BG         = "#ffffff"
    INPUT_TEXT       = "#1e293b"
    INPUT_PH         = "#94a3b8"
    INPUT_BORD       = "rgba(0,0,0,0.10)"
    INPUT_FOCUS      = "rgba(37,99,235,0.40)"
    INPUT_FOCUS_GLOW = "rgba(37,99,235,0.08)"
    SEND_BTN         = "#2563eb"
    CARET            = "#2563eb"
    SCROLL_THUMB     = "rgba(0,0,0,0.12)"
    AV_AI_BG         = "#2563eb"
    AV_HU_BG         = "rgba(0,0,0,0.04)"
    AV_HU_BR         = "rgba(0,0,0,0.10)"
    TOGGLE_LABEL     = "#2563eb"
    TOGGLE_ICON      = "🌙"

# ── Build the SVG doodle tile ───────────────────────────────────────────────────
s  = DOODLE_STROKE
op = DOODLE_OPACITY

_svg_raw = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">
<g fill="none" stroke="{s}" stroke-width="1.5" stroke-linecap="round"
   stroke-linejoin="round" opacity="{op}">

  <!-- Network graph nodes top-left -->
  <circle cx="80"  cy="80"  r="6"/>
  <circle cx="130" cy="55"  r="6"/>
  <circle cx="155" cy="95"  r="6"/>
  <circle cx="105" cy="115" r="6"/>
  <line x1="80"  y1="80"  x2="130" y2="55"/>
  <line x1="130" y1="55"  x2="155" y2="95"/>
  <line x1="155" y1="95"  x2="105" y2="115"/>
  <line x1="105" y1="115" x2="80"  y2="80"/>
  <line x1="80"  y1="80"  x2="155" y2="95"/>

  <!-- Robot face top-right -->
  <rect x="460" y="45" width="80" height="70" rx="12"/>
  <rect x="475" y="62" width="20" height="14" rx="4"/>
  <rect x="507" y="62" width="20" height="14" rx="4"/>
  <path d="M479,95 Q500,108 521,95"/>
  <line x1="500" y1="45" x2="500" y2="35"/>
  <circle cx="500" cy="31" r="5"/>
  <line x1="460" y1="78" x2="450" y2="78"/>
  <line x1="540" y1="78" x2="550" y2="78"/>

  <!-- Server stack left-mid -->
  <rect x="30" y="240" width="90" height="20" rx="4"/>
  <rect x="30" y="266" width="90" height="20" rx="4"/>
  <rect x="30" y="292" width="90" height="20" rx="4"/>
  <circle cx="108" cy="250" r="3" fill="{s}" stroke="none"/>
  <circle cx="108" cy="276" r="3" fill="{s}" stroke="none"/>
  <circle cx="108" cy="302" r="3" fill="{s}" stroke="none"/>
  <line x1="42" y1="250" x2="60" y2="250"/>
  <line x1="42" y1="276" x2="60" y2="276"/>
  <line x1="42" y1="302" x2="60" y2="302"/>

  <!-- Arrow sequence center-top -->
  <line x1="220" y1="70" x2="250" y2="70"/>
  <polyline points="246,64 255,70 246,76"/>
  <line x1="264" y1="70" x2="294" y2="70"/>
  <polyline points="290,64 299,70 290,76"/>
  <line x1="308" y1="70" x2="338" y2="70"/>
  <polyline points="334,64 343,70 334,76"/>

  <!-- Binary numbers right-mid -->
  <text x="490" y="220" font-family="monospace" font-size="11"
        fill="{s}" stroke="none" opacity="{op}">1 0 1 0</text>
  <text x="490" y="236" font-family="monospace" font-size="11"
        fill="{s}" stroke="none" opacity="{op}">0 1 1 0</text>
  <text x="490" y="252" font-family="monospace" font-size="11"
        fill="{s}" stroke="none" opacity="{op}">1 1 0 1</text>

  <!-- CPU chip center -->
  <rect x="250" y="240" width="70" height="70" rx="6"/>
  <rect x="260" y="250" width="50" height="50" rx="3"/>
  <line x1="260" y1="236" x2="260" y2="240"/>
  <line x1="275" y1="236" x2="275" y2="240"/>
  <line x1="290" y1="236" x2="290" y2="240"/>
  <line x1="305" y1="236" x2="305" y2="240"/>
  <line x1="260" y1="310" x2="260" y2="314"/>
  <line x1="275" y1="310" x2="275" y2="314"/>
  <line x1="290" y1="310" x2="290" y2="314"/>
  <line x1="305" y1="310" x2="305" y2="314"/>
  <line x1="236" y1="260" x2="250" y2="260"/>
  <line x1="236" y1="275" x2="250" y2="275"/>
  <line x1="236" y1="290" x2="250" y2="290"/>
  <line x1="320" y1="260" x2="334" y2="260"/>
  <line x1="320" y1="275" x2="334" y2="275"/>
  <line x1="320" y1="290" x2="334" y2="290"/>
  <line x1="268" y1="275" x2="312" y2="275"/>
  <line x1="285" y1="258" x2="285" y2="292"/>

  <!-- Tree hierarchy bottom-right -->
  <circle cx="510" cy="390" r="8"/>
  <circle cx="480" cy="430" r="8"/>
  <circle cx="540" cy="430" r="8"/>
  <circle cx="460" cy="465" r="8"/>
  <circle cx="500" cy="465" r="8"/>
  <line x1="510" y1="398" x2="480" y2="422"/>
  <line x1="510" y1="398" x2="540" y2="422"/>
  <line x1="480" y1="438" x2="460" y2="457"/>
  <line x1="480" y1="438" x2="500" y2="457"/>

  <!-- Gear settings top-center-right -->
  <circle cx="390" cy="90" r="16"/>
  <circle cx="390" cy="90" r="8"/>
  <line x1="390" y1="68" x2="390" y2="74"/>
  <line x1="390" y1="106" x2="390" y2="112"/>
  <line x1="368" y1="90" x2="374" y2="90"/>
  <line x1="406" y1="90" x2="412" y2="90"/>
  <line x1="374" y1="74" x2="378" y2="78"/>
  <line x1="402" y1="102" x2="406" y2="106"/>
  <line x1="406" y1="74" x2="402" y2="78"/>
  <line x1="378" y1="102" x2="374" y2="106"/>

  <!-- Database cylinder bottom-center -->
  <ellipse cx="280" cy="440" rx="38" ry="12"/>
  <ellipse cx="280" cy="480" rx="38" ry="12"/>
  <line x1="242" y1="440" x2="242" y2="480"/>
  <line x1="318" y1="440" x2="318" y2="480"/>
  <path d="M242,456 Q280,468 318,456"/>

  <!-- Line chart bottom-left -->
  <polyline points="40,520 70,495 100,510 130,475 160,490 190,460"/>
  <circle cx="40"  cy="520" r="3" fill="{s}" stroke="none"/>
  <circle cx="70"  cy="495" r="3" fill="{s}" stroke="none"/>
  <circle cx="100" cy="510" r="3" fill="{s}" stroke="none"/>
  <circle cx="130" cy="475" r="3" fill="{s}" stroke="none"/>
  <circle cx="160" cy="490" r="3" fill="{s}" stroke="none"/>
  <circle cx="190" cy="460" r="3" fill="{s}" stroke="none"/>

  <!-- Small robot left area -->
  <rect x="60"  y="155" width="50" height="44" rx="8"/>
  <rect x="71"  y="164" width="12" height="10" rx="3"/>
  <rect x="87"  y="164" width="12" height="10" rx="3"/>
  <path d="M72,185 Q85,193 98,185"/>
  <line x1="85"  y1="155" x2="85"  y2="148"/>
  <circle cx="85" cy="145" r="4"/>

  <!-- Scatter connected dots center-left -->
  <circle cx="200" cy="160" r="3" fill="{s}" stroke="none"/>
  <circle cx="215" cy="175" r="2" fill="{s}" stroke="none"/>
  <circle cx="230" cy="155" r="4" fill="{s}" stroke="none"/>
  <line x1="200" y1="160" x2="215" y2="175"/>
  <line x1="215" y1="175" x2="230" y2="155"/>

  <!-- Hexagon right-mid -->
  <polygon points="440,300 460,288 480,300 480,324 460,336 440,324"/>
  <circle cx="460" cy="312" r="8"/>

  <!-- Workflow arrows center-bottom -->
  <rect x="210" y="390" width="36" height="24" rx="5"/>
  <line x1="246" y1="402" x2="262" y2="402"/>
  <polyline points="258,396 267,402 258,408"/>
  <rect x="267" y="390" width="36" height="24" rx="5"/>
  <line x1="303" y1="402" x2="319" y2="402"/>
  <polyline points="315,396 324,402 315,408"/>
  <rect x="324" y="390" width="36" height="24" rx="5"/>

  <!-- Diamond top-center -->
  <polygon points="390,170 408,188 390,206 372,188"/>
  <circle cx="390" cy="188" r="5"/>

  <!-- Neural net nodes mid-left -->
  <circle cx="170" cy="310" r="5"/>
  <circle cx="170" cy="335" r="5"/>
  <circle cx="170" cy="360" r="5"/>
  <circle cx="205" cy="320" r="5"/>
  <circle cx="205" cy="348" r="5"/>
  <circle cx="240" cy="334" r="5"/>
  <line x1="175" y1="310" x2="200" y2="320"/>
  <line x1="175" y1="310" x2="200" y2="348"/>
  <line x1="175" y1="335" x2="200" y2="320"/>
  <line x1="175" y1="335" x2="200" y2="348"/>
  <line x1="175" y1="360" x2="200" y2="320"/>
  <line x1="175" y1="360" x2="200" y2="348"/>
  <line x1="210" y1="320" x2="235" y2="334"/>
  <line x1="210" y1="348" x2="235" y2="334"/>

  <!-- Cloud outline top-mid-left -->
  <path d="M200,130 Q200,115 215,115 Q218,105 230,107 Q235,98 247,102 Q260,98 262,110 Q275,110 275,122 Q275,133 262,133 Z"/>

  <!-- Brackets / code snippet right-bottom -->
  <text x="400" y="470" font-family="monospace" font-size="13"
        fill="{s}" stroke="none" opacity="{op}">if</text>
  <text x="418" y="470" font-family="monospace" font-size="13"
        fill="{s}" stroke="none" opacity="{op}">(ai)</text>
  <text x="400" y="488" font-family="monospace" font-size="13"
        fill="{s}" stroke="none" opacity="{op}">&#123; run(); &#125;</text>

  <!-- Waveform / signal right-top area -->
  <polyline points="340,150 350,130 360,170 370,120 380,160 390,140 400,155"/>

  <!-- Lock icon bottom-mid -->
  <rect x="345" y="490" width="28" height="22" rx="4"/>
  <path d="M350,490 Q350,478 359,478 Q368,478 368,490"/>
  <circle cx="359" cy="502" r="3"/>

</g>
</svg>"""

# ── Encode SVG to data URI properly ────────────────────────────────────────────
# Use base64 encoding — far more reliable than URL encoding in Streamlit
import base64
_svg_b64 = base64.b64encode(_svg_raw.encode("utf-8")).decode("utf-8")
DOODLE_DATA_URI = f"data:image/svg+xml;base64,{_svg_b64}"

# ── Inject doodle as a FIXED positioned div — bypasses Streamlit's CSS overrides
st.markdown(f"""
<div id="doodle-bg" style="
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
    background-color: {BG};
    background-image: url('{DOODLE_DATA_URI}');
    background-repeat: repeat;
    background-size: 600px 600px;
"></div>
""", unsafe_allow_html=True)

# ── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Force all Streamlit backgrounds transparent so doodle div shows through */
html, body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div {{
    background-color: transparent !important;
    background-image: none !important;
}}

/* Keep bottom bar visually separated but transparent bg */
[data-testid="stBottom"] {{
    border-top: 1px solid {INPUT_BORD} !important;
    box-shadow: none !important;
}}

/* Ensure the fixed doodle bg color applies to full page */
body {{
    background-color: {BG} !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}

.block-container {{
    max-width: 780px !important;
    padding-top: 1.2rem !important;
    padding-bottom: 0.5rem !important;
    position: relative !important;
    z-index: 1 !important;
}}

[data-testid="stChatMessage"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 0 !important;
}}
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] {{ display: none !important; }}
[data-testid="stChatMessageContent"] {{
    width: 100% !important;
    background: transparent !important;
    padding: 0 !important;
}}
[data-testid="stChatMessageContent"] p {{ margin: 0 !important; }}

.msg-row {{
    display: flex;
    align-items: flex-end;
    gap: 10px;
    margin-bottom: 14px;
    width: 100%;
    animation: fadeUp 0.22s ease;
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.msg-row.ai    {{ justify-content: flex-start; }}
.msg-row.human {{ justify-content: flex-end; }}

.avatar {{
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}}
.avatar.ai {{
    border-radius: 10px;
    background: {AV_AI_BG};
    font-size: 20px;
}}
.avatar.human {{
    background: {AV_HU_BG};
    border: 1px solid {AV_HU_BR};
}}

.bubble {{
    max-width: 62%;
    padding: 11px 16px;
    font-family: 'Inter', sans-serif;
    font-size: 14px; line-height: 1.6;
    white-space: pre-wrap; word-break: break-word;
}}
.bubble.ai {{
    background: {AI_BUBBLE};
    border: 1px solid {AI_BORD};
    border-radius: 16px 16px 16px 4px;
    color: {AI_TEXT};
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    backdrop-filter: blur(6px);
}}
.bubble.human {{
    background: {HU_BUBBLE};
    border: {HU_BORD};
    border-radius: 16px 16px 4px 16px;
    color: {HU_TEXT};
    box-shadow: {HU_SHADOW};
}}

[data-testid="stToggle"] {{ margin-top: 20px; }}
[data-testid="stToggle"] label,
[data-testid="stToggle"] > label > div[data-testid="stMarkdownContainer"] p {{
    color: {TOGGLE_LABEL} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.04em !important;
}}

[data-testid="stChatInput"] {{
    background: {INPUT_BG} !important;
    border: 1.5px solid {INPUT_BORD} !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: {INPUT_FOCUS} !important;
    box-shadow: 0 0 0 3px {INPUT_FOCUS_GLOW} !important;
}}
[data-testid="stChatInput"] textarea {{
    background: {INPUT_BG} !important;
    color: {INPUT_TEXT} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    caret-color: {CARET} !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: {INPUT_PH} !important;
    opacity: 1 !important;
}}
[data-testid="stChatInput"] button {{
    background: {SEND_BTN} !important;
    border-radius: 10px !important;
    color: white !important;
    border: none !important;
}}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {SCROLL_THUMB}; border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)

# ── Header + Toggle ─────────────────────────────────────────────────────────────
col_head, col_toggle = st.columns([5, 1])

with col_head:
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:12px;
        padding:13px 18px;
        background:{HEADER_BG};
        border:1px solid {HEADER_BORD};
        border-radius:16px; margin-bottom:16px;
        backdrop-filter: blur(8px);
        position: relative; z-index: 2;
    ">
        <div style="
            width:42px; height:42px; border-radius:10px;
            background:{AV_AI_BG};
            display:flex; align-items:center; justify-content:center;
            font-size:22px; flex-shrink:0;
        ">🤖</div>
        <div>
            <div style="
                font-family:'Inter',sans-serif; font-size:15px; font-weight:600;
                color:{TITLE_COL}; letter-spacing:0.01em;
            ">Chat Assistant</div>
            <div style="
                font-size:11px; color:{STATUS_COL};
                display:flex; align-items:center; gap:5px; margin-top:2px;
                font-family:'JetBrains Mono',monospace; letter-spacing:0.05em;
            ">
                <span style="
                    width:6px;height:6px;border-radius:50%;background:#22c55e;
                    display:inline-block;box-shadow:0 0 5px #22c55e;
                "></span>
                online &nbsp;·&nbsp; rag powered
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_toggle:
    new_dark = st.toggle(f"{TOGGLE_ICON}", value=dark, key="theme_toggle")
    if new_dark != dark:
        st.session_state.dark_mode = new_dark
        st.rerun()

# ── Bubble renderer ─────────────────────────────────────────────────────────────
def render_bubble(role: str, content: str):
    safe = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if role == "assistant":
        st.markdown(f"""
        <div class="msg-row ai">
            <div class="avatar ai">🤖</div>
            <div class="bubble ai">{safe}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row human">
            <div class="bubble human">{safe}</div>
            <div class="avatar human">👤</div>
        </div>""", unsafe_allow_html=True)

# ── Render chat history ─────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    render_bubble(msg["role"], msg["content"])

# ── Chat input ──────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your message…"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_bubble("user", user_input)

    with st.spinner("Thinking…"):
        try:
            resp = requests.post(API_URL, json={"message": user_input}, timeout=30)
            resp.raise_for_status()
            reply = resp.json().get("response", "Sorry, I couldn't generate a response.")
        except requests.exceptions.ConnectionError:
            reply = "⚠️ Could not connect to the backend. Is your FastAPI server running on port 8000?"
        except requests.exceptions.Timeout:
            reply = "⚠️ Request timed out. Please try again."
        except Exception as e:
            reply = f"⚠️ Something went wrong: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    render_bubble("assistant", reply)