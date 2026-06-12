import random
import streamlit as st

st.set_page_config(page_title="Mental Math", page_icon="🧮")

# ---------------------------------------------------------------------------
# Your original game used `while True:` + input(). A web app can't block and
# wait for input the way a terminal does — Streamlit re-runs this file top to
# bottom every time the user does something. So instead of a loop, we keep the
# score and the current question in st.session_state (memory that survives
# between those re-runs). The math logic below is unchanged from your script.
# ---------------------------------------------------------------------------

# set up the remembered values the first time the app loads
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.feedback = ""


def new_question():
    """This is your original question logic, lifted straight from your loop."""
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 9)
    c = random.choice(["+", "-", "x"])

    if c == "-":
        ans = num1 - num2
    if c == "x":
        ans = num1 * num2
    if c == "+":
        ans = num1 + num2

    # stash the question so it stays the same until the user answers it
    st.session_state.num1 = num1
    st.session_state.num2 = num2
    st.session_state.c = c
    st.session_state.ans = ans


# make sure there's a question ready on first load
if "num1" not in st.session_state:
    new_question()


# ---------------------------- the page itself ----------------------------
st.title("🧮 Mental Math")
st.metric("Score", st.session_state.score)

# this replaces your print(str(num1)+c+str(num2))
st.header(f"{st.session_state.num1}  {st.session_state.c}  {st.session_state.num2}")

# a form lets the user press Enter to submit, and clears the box afterwards
with st.form("answer_form", clear_on_submit=True):
    userinput = st.text_input("Your answer", placeholder="type a number")
    submitted = st.form_submit_button("Submit")

if submitted:
    # guard against blank / non-number input so the hosted app never crashes
    # (your terminal version would have errored on int("") )
    try:
        guess = int(userinput)
    except ValueError:
        st.session_state.feedback = "⚠️ Please type a whole number."
    else:
        if guess == st.session_state.ans:                 # your scoring rules
            st.session_state.score += 1
            st.session_state.feedback = "✅ Correct!"
        else:
            st.session_state.score -= 1
            st.session_state.feedback = f"❌ Wrong — the answer was {st.session_state.ans}"
        new_question()
    st.rerun()

# show the result of the last answer
if st.session_state.feedback:
    st.write(st.session_state.feedback)

# "exit" from your script becomes a reset button
if st.button("End game / reset score"):
    st.session_state.score = 0
    st.session_state.feedback = ""
    new_question()
    st.rerun()
