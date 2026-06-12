import random
import streamlit as st

st.set_page_config(page_title="Math Buddy", page_icon="🧮", layout="centered")

# ===========================================================================
#  LOOK & FEEL — all the cute styling lives in this CSS block. It doesn't
#  touch your game; it just paints Streamlit's buttons pink/blue, rounds
#  everything off with a thick cartoon outline, and loads a chunky font.
# ===========================================================================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap');

  .stApp{ background:#eafaf1; }
  [data-testid="stHeader"]{display:none}
  #MainMenu, footer{visibility:hidden}
  .block-container, [data-testid="stMainBlockContainer"]{
    max-width:430px; padding-top:1.6rem; padding-bottom:2rem;
  }
  html, body, [class*="css"]{ font-family:'Fredoka',sans-serif; }

  /* tighten spacing so the keypad feels like one unit */
  [data-testid="stVerticalBlock"]{ gap:.55rem; }
  [data-testid="stHorizontalBlock"]{ gap:.55rem; }

  /* ---- title + score pill ---- */
  .title{ text-align:center; font-weight:700; font-size:30px; color:#3a7d5c;
          letter-spacing:.01em; margin-bottom:10px; }
  .scorepill{ display:flex; justify-content:center; margin-bottom:14px; }
  .scorepill span{
    background:#ffffff; border:3px solid #2a2a2a; border-radius:999px;
    padding:6px 18px; font-weight:700; font-size:18px; color:#2a2a2a;
    box-shadow:0 3px 0 #2a2a2a;
  }
  .scorepill span.up{ background:#d8f5c2; }
  .scorepill span.down{ background:#ffd6dd; }

  /* ---- calculator body + screen ---- */
  .calc{
    background:#a9e8c8; border:4px solid #2a2a2a; border-radius:30px;
    padding:22px; box-shadow:0 8px 0 #2a2a2a; margin-bottom:20px;
  }
  .screen{
    background:#cdeaa0; border:4px solid #2a2a2a; border-radius:20px;
    padding:16px 14px 18px; text-align:center;
  }
  .equation{ font-weight:700; font-size:46px; color:#2a2a2a; line-height:1.1; }
  .equation .op{ color:#e86a8e; }
  .typed{ font-weight:600; font-size:26px; color:#3a7d5c; margin-top:4px; min-height:32px; }
  .typed .ph{ color:#8bbf9a; }

  /* ---- keypad buttons (secondary = pink) ---- */
  .stButton button, .stButton button[kind="secondary"],
  .stButton button[data-testid="stBaseButton-secondary"]{
    background:#fac6d3 !important; color:#2a2a2a !important;
    border:3px solid #2a2a2a !important; border-radius:20px !important;
    font-family:'Fredoka',sans-serif !important; font-weight:700 !important;
    font-size:24px !important; min-height:56px !important;
    box-shadow:0 4px 0 #2a2a2a !important; transition:transform .05s, box-shadow .05s;
  }
  .stButton button:hover{ background:#ffb6c8 !important; }
  .stButton button:active{ transform:translateY(4px) !important; box-shadow:0 0 0 #2a2a2a !important; }

  /* ---- the = / enter key (primary = blue) ---- */
  .stButton button[kind="primary"],
  .stButton button[data-testid="stBaseButton-primary"]{
    background:#a7d8ee !important; color:#2a2a2a !important;
    border:3px solid #2a2a2a !important; border-radius:20px !important;
    font-family:'Fredoka',sans-serif !important; font-weight:700 !important;
    font-size:24px !important; min-height:58px !important;
    box-shadow:0 4px 0 #2a2a2a !important;
  }
  .stButton button[kind="primary"]:hover,
  .stButton button[data-testid="stBaseButton-primary"]:hover{ background:#8ccdec !important; }

  .reset{ text-align:center; margin-top:8px; }
</style>
""", unsafe_allow_html=True)


# ---- the three kawaii faces (drawn with SVG, no logic — just decoration) ----
FACE_HAPPY = """
<svg viewBox="0 0 150 70" width="120" style="margin-bottom:2px">
  <ellipse cx="46" cy="30" rx="8" ry="11" fill="#2a2a2a"/>
  <circle cx="43" cy="26" r="2.6" fill="#fff"/>
  <ellipse cx="104" cy="30" rx="8" ry="11" fill="#2a2a2a"/>
  <circle cx="101" cy="26" r="2.6" fill="#fff"/>
  <path d="M62 40 Q75 54 88 40" fill="none" stroke="#2a2a2a" stroke-width="5" stroke-linecap="round"/>
  <path d="M71 46 Q75 56 79 46 Z" fill="#e86a8e"/>
</svg>"""

FACE_GREAT = """
<svg viewBox="0 0 150 70" width="120" style="margin-bottom:2px">
  <path d="M36 32 Q46 20 56 32" fill="none" stroke="#2a2a2a" stroke-width="5" stroke-linecap="round"/>
  <path d="M94 32 Q104 20 114 32" fill="none" stroke="#2a2a2a" stroke-width="5" stroke-linecap="round"/>
  <path d="M58 38 Q75 62 92 38 Z" fill="#e86a8e" stroke="#2a2a2a" stroke-width="4" stroke-linejoin="round"/>
  <path d="M22 18 l3 6 6 3 -6 3 -3 6 -3 -6 -6 -3 6 -3 z" fill="#fff2a8" stroke="#2a2a2a" stroke-width="2"/>
  <path d="M122 16 l2.5 5 5 2.5 -5 2.5 -2.5 5 -2.5 -5 -5 -2.5 5 -2.5 z" fill="#fff2a8" stroke="#2a2a2a" stroke-width="2"/>
</svg>"""

FACE_SAD = """
<svg viewBox="0 0 150 70" width="120" style="margin-bottom:2px">
  <ellipse cx="46" cy="32" rx="7" ry="9" fill="#2a2a2a"/>
  <ellipse cx="104" cy="32" rx="7" ry="9" fill="#2a2a2a"/>
  <path d="M34 20 Q46 16 56 22" fill="none" stroke="#2a2a2a" stroke-width="4" stroke-linecap="round"/>
  <path d="M94 22 Q104 16 116 20" fill="none" stroke="#2a2a2a" stroke-width="4" stroke-linecap="round"/>
  <path d="M62 52 Q75 40 88 52" fill="none" stroke="#2a2a2a" stroke-width="5" stroke-linecap="round"/>
  <path d="M116 40 q5 9 0 13 q-5 -4 0 -13 z" fill="#7ec8e3" stroke="#2a2a2a" stroke-width="2"/>
</svg>"""


# ===========================================================================
#  YOUR GAME — the rules are exactly your original script.
#  The terminal loop / input() / print() became session_state + buttons
#  because a web page can't loop-and-wait, but the maths below is yours.
# ===========================================================================
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.answer_str = ""     # what the player has tapped so far
    st.session_state.fb_kind = "happy"   # which face to show
    st.session_state.last_dir = ""       # colours the score pill


def new_question():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 9)
    c = random.choice(["+", "-", "x"])

    if c == "-":
        ans = num1 - num2
    if c == "x":
        ans = num1 * num2
    if c == "+":
        ans = num1 + num2

    st.session_state.num1 = num1
    st.session_state.num2 = num2
    st.session_state.c = c
    st.session_state.ans = ans


if "num1" not in st.session_state:
    new_question()


# ---- keypad callbacks (these just build the typed-in answer string) ----
def tap_digit(d):
    st.session_state.answer_str += d

def tap_sign():
    s = st.session_state.answer_str
    st.session_state.answer_str = s[1:] if s.startswith("-") else "-" + s

def tap_delete():
    st.session_state.answer_str = st.session_state.answer_str[:-1]

def tap_enter():
    s = st.session_state.answer_str
    if s in ("", "-"):
        return                                   # nothing typed yet
    guess = int(s)
    if guess == st.session_state.ans:            # <-- your scoring rules
        st.session_state.score += 1
        st.session_state.fb_kind = "great"
        st.session_state.last_dir = "up"
    else:
        st.session_state.score -= 1
        st.session_state.fb_kind = "sad"
        st.session_state.last_dir = "down"
    st.session_state.answer_str = ""
    new_question()

def reset_game():
    st.session_state.score = 0
    st.session_state.answer_str = ""
    st.session_state.fb_kind = "happy"
    st.session_state.last_dir = ""
    new_question()


# ------------------------------ draw the page ------------------------------
st.markdown('<div class="title">🧮 Math Buddy</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="scorepill"><span class="{st.session_state.last_dir}">'
    f'⭐ Score&nbsp; {st.session_state.score}</span></div>',
    unsafe_allow_html=True,
)

face = {"happy": FACE_HAPPY, "great": FACE_GREAT, "sad": FACE_SAD}[st.session_state.fb_kind]
op_display = "×" if st.session_state.c == "x" else st.session_state.c
typed = st.session_state.answer_str
typed_html = typed if typed else '<span class="ph">tap a number…</span>'

st.markdown(f"""
<div class="calc">
  <div class="screen">
    {face}
    <div class="equation">
      {st.session_state.num1}<span class="op"> {op_display} </span>{st.session_state.num2}
    </div>
    <div class="typed">{typed_html}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# keypad: numbers in pink, = in blue, just like your picture
r1 = st.columns(3)
r1[0].button("7", use_container_width=True, on_click=tap_digit, args=("7",))
r1[1].button("8", use_container_width=True, on_click=tap_digit, args=("8",))
r1[2].button("9", use_container_width=True, on_click=tap_digit, args=("9",))

r2 = st.columns(3)
r2[0].button("4", use_container_width=True, on_click=tap_digit, args=("4",))
r2[1].button("5", use_container_width=True, on_click=tap_digit, args=("5",))
r2[2].button("6", use_container_width=True, on_click=tap_digit, args=("6",))

r3 = st.columns(3)
r3[0].button("1", use_container_width=True, on_click=tap_digit, args=("1",))
r3[1].button("2", use_container_width=True, on_click=tap_digit, args=("2",))
r3[2].button("3", use_container_width=True, on_click=tap_digit, args=("3",))

r4 = st.columns(3)
r4[0].button("±", use_container_width=True, on_click=tap_sign)
r4[1].button("0", use_container_width=True, on_click=tap_digit, args=("0",))
r4[2].button("⌫", use_container_width=True, on_click=tap_delete)

st.button("=", type="primary", use_container_width=True, on_click=tap_enter)

st.markdown('<div class="reset"></div>', unsafe_allow_html=True)
st.button("🔄 New game", use_container_width=True, on_click=reset_game)
