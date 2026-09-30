"""End-to-end checks of the Streamlit app using Streamlit's AppTest harness."""
import pytest
from streamlit.testing.v1 import AppTest

NORMAL_LIMIT = 8


@pytest.fixture
def at():
    return AppTest.from_file("app.py", default_timeout=30).run()


def guess(at, value):
    at.text_input[0].set_value(str(value))
    next(b for b in at.button if "Submit" in b.label).click().run()


def new_game(at):
    next(b for b in at.button if "New Game" in b.label).click().run()


def wrong_guess(at):
    secret = at.session_state.secret
    return 100 if secret < 100 else 1


def lose_round(at, limit=NORMAL_LIMIT):
    for _ in range(limit):
        guess(at, wrong_guess(at))


# ---------- attempts ----------

def test_game_starts_with_full_attempts(at):
    # Regression: attempts used to start at 1, giving 7 guesses instead of 8.
    assert at.session_state.attempts == 0
    assert "Attempts left: 8" in at.info[0].value


@pytest.mark.parametrize("bad_input", ["", "abc", "1,5", "!!"])
def test_invalid_input_does_not_use_an_attempt(at, bad_input):
    guess(at, bad_input)
    assert at.session_state.attempts == 0
    assert at.error  # the player still gets an error message


def test_invalid_input_cannot_push_attempts_past_the_limit(at):
    # Regression: invalid guesses used to burn attempts without ever
    # checking the limit, leaving "Attempts left: -5" and a game that never ended.
    for _ in range(NORMAL_LIMIT + 4):
        guess(at, "abc")
    assert at.session_state.status == "playing"
    assert at.session_state.attempts == 0
    assert "Attempts left: 8" in at.info[0].value


def test_attempts_left_updates_immediately_after_a_guess(at):
    # Regression: the counter used to render before the guess was processed.
    guess(at, wrong_guess(at))
    assert "Attempts left: 7" in at.info[0].value


# ---------- ending the game ----------

def test_game_ends_after_the_attempt_limit(at):
    lose_round(at)
    assert at.session_state.status == "lost"
    assert at.session_state.attempts == NORMAL_LIMIT


def test_no_loss_before_the_last_attempt(at):
    for _ in range(NORMAL_LIMIT - 1):
        guess(at, wrong_guess(at))
    assert at.session_state.status == "playing"


def test_loss_message_shows_secret_and_score(at):
    secret = at.session_state.secret
    lose_round(at)
    message = at.error[0].value
    assert "Out of attempts" in message
    assert f"secret was {secret}" in message
    assert f"Score: {at.session_state.score}" in message


def test_loss_message_persists_across_reruns(at):
    # Regression: the message used to be drawn only on the run that processed
    # the last guess, so any later rerun replaced it with a generic line.
    lose_round(at)
    at.checkbox[0].uncheck().run()
    assert "Out of attempts" in at.error[0].value
    assert f"secret was {at.session_state.secret}" in at.error[0].value


def test_win_message_shows_score_and_persists(at):
    guess(at, at.session_state.secret)
    assert at.session_state.status == "won"
    assert "You won!" in at.success[0].value
    assert "Final score: 90" in at.success[0].value
    at.checkbox[0].uncheck().run()
    assert "Final score: 90" in at.success[0].value


def test_guesses_after_the_game_is_over_are_ignored(at):
    lose_round(at)
    score, attempts = at.session_state.score, at.session_state.attempts
    guess(at, at.session_state.secret)
    assert at.session_state.status == "lost"
    assert at.session_state.score == score
    assert at.session_state.attempts == attempts


# ---------- scoring in the app ----------

def test_first_try_win_scores_ninety(at):
    guess(at, at.session_state.secret)
    assert at.session_state.score == 90


def test_wrong_guesses_each_cost_five_in_the_app(at):
    scores = []
    for _ in range(4):
        guess(at, wrong_guess(at))
        scores.append(at.session_state.score)
    assert scores == [-5, -10, -15, -20]


# ---------- hints in the app ----------

def test_hint_points_the_right_way(at):
    secret = at.session_state.secret
    if secret < 100:
        guess(at, 100)
        assert "LOWER" in at.warning[0].value
    if secret > 1:
        guess(at, 1)
        assert "HIGHER" in at.warning[0].value


def test_secret_does_not_change_between_guesses(at):
    secret = at.session_state.secret
    for _ in range(4):
        guess(at, wrong_guess(at))
        assert at.session_state.secret == secret


# ---------- New Game ----------

def test_new_game_resets_everything(at):
    lose_round(at)
    new_game(at)
    assert at.session_state.status == "playing"
    assert at.session_state.attempts == 0
    assert at.session_state.score == 0
    assert at.session_state.history == []
    assert not at.error
    assert "New game started." in [s.value for s in at.success]
    assert "Attempts left: 8" in at.info[0].value


def test_new_game_clears_the_input_box(at):
    guess(at, wrong_guess(at))
    new_game(at)
    assert at.text_input[0].value == ""


def test_can_lose_again_after_new_game(at):
    # Regression: after New Game the status stayed "lost" and the ending
    # message was missing on the following round.
    lose_round(at)
    new_game(at)
    secret = at.session_state.secret
    lose_round(at)
    assert at.session_state.status == "lost"
    assert f"secret was {secret}" in at.error[0].value
    assert f"Score: {at.session_state.score}" in at.error[0].value


def test_can_win_after_losing_and_starting_a_new_game(at):
    lose_round(at)
    new_game(at)
    guess(at, at.session_state.secret)
    assert at.session_state.status == "won"
    assert at.session_state.score == 90


def test_new_game_secret_respects_the_difficulty_range(at):
    at.sidebar.selectbox[0].select("Easy").run()
    for _ in range(15):
        new_game(at)
        assert 1 <= at.session_state.secret <= 20


# ---------- edge cases ----------

def set_difficulty(at, name):
    at.sidebar.selectbox[0].select(name).run()
    new_game(at)  # regenerate the secret inside the new range


@pytest.mark.parametrize("blank", ["   ", "\t"])
def test_whitespace_only_input_does_not_use_an_attempt(at, blank):
    guess(at, blank)
    assert at.session_state.attempts == 0
    assert at.error


@pytest.mark.parametrize("value, word", [(-5, "HIGHER"), (0, "HIGHER"), (999, "LOWER")])
def test_out_of_range_guesses_are_accepted_and_hinted(at, value, word):
    # Documents current behaviour: out-of-range numbers are valid guesses
    # that use an attempt and get a normal hint.
    guess(at, value)
    assert at.session_state.attempts == 1
    assert word in at.warning[0].value


def test_decimal_guess_is_truncated_and_counted(at):
    guess(at, "5.9")
    assert at.session_state.history == [5]
    assert at.session_state.attempts == 1


def test_winning_on_the_last_attempt_is_a_win_not_a_loss(at):
    for _ in range(NORMAL_LIMIT - 1):
        guess(at, wrong_guess(at))
    guess(at, at.session_state.secret)
    assert at.session_state.status == "won"
    assert at.session_state.attempts == NORMAL_LIMIT
    assert at.session_state.score == -5 * (NORMAL_LIMIT - 1) + 20
    assert not at.error


@pytest.mark.parametrize("difficulty, limit, high", [("Easy", 6, 20), ("Hard", 5, 50)])
def test_attempt_limit_and_range_follow_the_difficulty(at, difficulty, limit, high):
    set_difficulty(at, difficulty)
    assert 1 <= at.session_state.secret <= high
    assert f"Attempts left: {limit}" in at.info[0].value
    for _ in range(limit - 1):
        guess(at, wrong_guess(at))
    assert at.session_state.status == "playing"
    guess(at, wrong_guess(at))
    assert at.session_state.status == "lost"


def test_repeated_new_game_clicks_are_safe(at):
    for _ in range(5):
        new_game(at)
    assert at.session_state.attempts == 0
    assert at.session_state.status == "playing"
    assert not at.exception


def test_new_game_in_the_middle_of_a_round_discards_progress(at):
    for _ in range(3):
        guess(at, wrong_guess(at))
    new_game(at)
    assert at.session_state.attempts == 0
    assert at.session_state.score == 0
    assert "Attempts left: 8" in at.info[0].value


def test_hint_checkbox_off_hides_the_hint_but_still_scores(at):
    at.checkbox[0].uncheck().run()
    guess(at, wrong_guess(at))
    assert not at.warning
    assert at.session_state.score == -5
    assert at.session_state.attempts == 1


def test_history_records_valid_and_invalid_input_in_order(at):
    guess(at, "abc")
    guess(at, wrong_guess(at))
    assert at.session_state.history[0] == "abc"
    assert len(at.session_state.history) == 2
