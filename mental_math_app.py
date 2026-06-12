import random
import streamlit as st

st.set_page_config(page_title="Quickfire — Mental Math", page_icon="🧮", layout="centered")

# ===========================================================================
#  STYLING ONLY — this big CSS block is what makes the app look good.
#  None of it touches your game logic; it just restyles Streamlit's defaults
#  and gives us a few custom pieces (the equation card, the scoreboard, the
#  feedback banner). Your Python is further down, unchanged.
# ===========================================================================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

  /* page background + hide Streamlit chrome */
  .stApp{
    background:radial-gradient(120% 90% at 50% -10%,#241d40 0%,#14111f 55%);
  }
  [data-testid="stHeader"]{display:none}
  #MainMenu, footer{visibility:hidden}
  .block-container, [data-testid="stMainBlockContainer"]{
    max-width:460px; padding-top:2.2rem; padding-bottom:2rem;
  }

  /* brand + score row */
  .bar{display:flex;align-items:flex-end;justify-content:space-between;
       margin-bottom:16px;padding:0 2px;font-family:'Space Grotesk',sans-serif;}
  .brand{font-weight:700;font-size:15px;letter-spacing:.16em;
         text-transform:uppercase;color:#8e88b0;}
  .brand b{color:#b6f35c;}
  .stat{text-align:right;line-height:1.05;}
  .stat .label{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8e88b0;}
  .stat .val{font-family:'JetBrains Mono',monospace;font-weight:800;font-size:34px;
             color:#ece9ff;font-variant-numeric:tabular-nums;}
  .stat .val.up{color:#b6f35c;}
  .stat .val.down{color:#fb7185;}

  /* equation card */
  .card{
    background:linear-gradient(180deg,#1f1b34,#1a1530);
    border:1px solid #322c50;border-radius:22px;
    padding:40px 26px 34px;
    box-shadow:0 30px 60px -30px rgba(0,0,0,.8), inset 0 1px 0 rgba(255,255,255,.04);
  }
  .equation{font-family:'JetBrains Mono',monospace;font-weight:800;
    font-size:clamp(48px,15vw,70px);text-align:center;color:#ece9ff;
    font-variant-numeric:tabular-nums;letter-spacing:.02em;}
  .equation .op{color:#b6f35c;margin:0 .12em;}

  /* feedback banner */
  .fb{margin-top:16px;text-align:center;font-family:'Space Grotesk',sans-serif;
      font-weight:500;font-size:15px;}
  .fb.good{color:#b6f35c;}
  .fb.bad{color:#fb7185;}
  .fb.warn{color:#f5c451;}

  /* answer input */
  .stTextInput input{
    background:#100d1c !important;border:1.5px solid #322c50 !important;
    border-radius:14px !important;color:#ece9ff !important;
    font-family:'JetBrains Mono',monospace !important;font-weight:700 !important;
    font-size:26px !important;text-align:center !important;
    padding:14px !important;
  }
  .stTextInput input::placeholder{color:#4b456b !important;font-weight:500 !important;}
  .stTextInput input:focus{
    border-color:#b6f35c !important;
    box-shadow:0 0 0 4px rgba(182,243,92,.30) !important;
  }

  /* submit button (primary, lime) */
  .stFormSubmitButton button{
    background:#b6f35c !important;color:#16210a !important;border:none !important;
    border-radius:13px !important;font-family:'Space Grotesk',sans-serif !important;
    font-weight:700 !important;font-size:17px !important;padding:13px !important;
  }
  .stFormSubmitButton button:hover{background:#c9ff6b !important;}

  /* reset button (secondary, ghost) */
  .stButton button{
    background:transparent !important;color:#8e88b0 !important;
    border:1px solid #322c50 !important;border-radius:12px !important;
    font-family:'Space Grotesk',sans-serif !important;font-weight:600 !important;
    font-size:13px !important;letter-spacing:.12em !important;text-transform:uppercase !important;
    padding:11px !important;
  }
  .stButton button:hover{color:#ece9ff !important;border-color:#473e6e !important;}

  /* tighten the form container */
  [data-testid="stForm"]{border:none !important;padding:14px 0 0 0 !important;}
</style>
""", unsafe_allow_html=True)


# ===========================================================================
#  YOUR GAME — same rules as your original script.
#  The while-loop became session_state because a web app re-runs top to
#  bottom on each click instead of looping. The math is yours, untouched.
# ===========================================================================
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.fb_kind = ""      # good / bad / warn — just for colour
    st.session_state.last_dir = ""     # up / down — colours the score


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


# ----------------------------- draw the page -----------------------------
# scoreboard row (custom HTML so it looks the way we want)
score_class = st.session_state.last_dir  # "up", "down", or ""
st.markdown(f"""
<div class="bar">
  <div class="brand">Quick<b>fire</b></div>
  <div class="stat">
    <div class="label">Score</div>
    <div class="val {score_class}">{st.session_state.score}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# the equation card (× shown instead of x, but the logic still uses "x")
op_display = "×" if st.session_state.c == "x" else st.session_state.c
feedback_html = ""
if st.session_state.feedback:
    feedback_html = f'<div class="fb {st.session_state.fb_kind}">{st.session_state.feedback}</div>'

st.markdown(f"""
<div class="card">
  <div class="equation">
    <span>{st.session_state.num1}</span><span class="op">{op_display}</span><span>{st.session_state.num2}</span>
  </div>
  {feedback_html}
</div>
""", unsafe_allow_html=True)

# the answer form — Enter or the button submits, box clears each time
with st.form("answer_form", clear_on_submit=True):
    userinput = st.text_input("Your answer", placeholder="type a number",
                              label_visibility="collapsed")
    submitted = st.form_submit_button("Submit", use_container_width=True)

if submitted:
    try:
        guess = int(userinput)
    except ValueError:
        st.session_state.feedback = "Type a whole number."
        st.session_state.fb_kind = "warn"
    else:
        if guess == st.session_state.ans:                 # your scoring rules
            st.session_state.score += 1
            st.session_state.feedback = "Correct!"
            st.session_state.fb_kind = "good"
            st.session_state.last_dir = "up"
        else:
            st.session_state.score -= 1
            st.session_state.feedback = f"Wrong — the answer was {st.session_state.ans}"
            st.session_state.fb_kind = "bad"
            st.session_state.last_dir = "down"
        new_question()
    st.rerun()

# reset (your original "exit")
if st.button("End game / reset score", use_container_width=True):
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.fb_kind = ""
    st.session_state.last_dir = ""
    new_question()
    st.rerun()
