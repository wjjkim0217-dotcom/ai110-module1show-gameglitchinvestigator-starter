# Bug fixes in this file were made with the help of an AI agent (Claude Code).
# Comments tagged FIX mark where a bug was found and fixed.

import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: start at 0 so Normal gives 8 guesses, not 7.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_id" not in st.session_state:
    st.session_state.game_id = 0


# FIX: New Game now resets all state (status, score, history) as a callback,
# so the state is clean before the widgets draw.
def start_new_game(low, high):
    st.session_state.attempts = 0
    # FIX: use the difficulty's range (was hardcoded 1-100).
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_id += 1
    st.session_state.just_started = True


st.subheader("Make a guess")

# Filled in after the guess is processed so they never show stale values.
# FIX: filled in at the bottom so the counters aren't a guess behind.
info_box = st.container()
debug_box = st.container()

# FIX: form makes one click or Enter submit (was needing two).
with st.form("guess_form", clear_on_submit=True):
    raw_guess = st.text_input(
        "Enter your guess:",
        # game_id changes on New Game so the box is cleared.
        key=f"guess_input_{difficulty}_{st.session_state.game_id}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    st.button("New Game 🔁", on_click=start_new_game, args=(low, high))
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: message was hidden by st.rerun(); shown once via a flag instead.
if st.session_state.pop("just_started", False):
    st.success("New game started.")

if st.session_state.status == "playing" and submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIX: invalid input no longer costs an attempt (it could push attempts
        # past the limit and the game never ended).
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: pass the secret as an int (it was cast to str on some attempts).
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

# Drawn on every run so the result stays visible until New Game is clicked.
# FIX: drawn every run so the result survives reruns until New Game.
if st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! "
        f"The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Start a new game to try again."
    )

with info_box:
    # FIX: show the real range (was hardcoded "1 and 100").
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )

with debug_box:
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
