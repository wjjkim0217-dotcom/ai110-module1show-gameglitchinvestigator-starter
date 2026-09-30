import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# ---------- check_guess ----------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    # A too-high guess should tell the player to go lower
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    # A too-low guess should tell the player to go higher
    assert "HIGHER" in message

@pytest.mark.parametrize("guess, secret, expected", [
    (9, 50, "Too Low"),     # as strings "9" > "50", which used to flip the hint
    (100, 20, "Too High"),  # as strings "100" < "20"
    (2, 10, "Too Low"),
    (10, 2, "Too High"),
])
def test_check_guess_compares_numbers_not_strings(guess, secret, expected):
    # Regression: the app used to turn the secret into a str on some attempts,
    # so guesses were compared as text ("9" > "50") and the hints were wrong.
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected

def test_check_guess_hint_matches_direction_at_boundaries():
    assert check_guess(51, 50)[1] == "📉 Go LOWER!"
    assert check_guess(49, 50)[1] == "📈 Go HIGHER!"

def test_check_guess_has_no_string_fallback():
    # The TypeError fallback that compared str(guess) to the secret is gone,
    # so a str secret is a caller bug and should fail loudly.
    with pytest.raises(TypeError):
        check_guess(60, "50")

# ---------- parse_guess ----------

def test_parse_valid_guess():
    assert parse_guess("42") == (True, 42, None)

def test_parse_decimal_guess_truncates():
    assert parse_guess("7.9") == (True, 7, None)

def test_parse_blank_or_none_guess():
    assert parse_guess("")[0] is False
    assert parse_guess(None)[0] is False

def test_parse_non_numeric_guess():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

# ---------- update_score ----------

@pytest.mark.parametrize("attempt, expected", [
    (1, 90),   # first-try win (used to score 70)
    (2, 80),
    (5, 50),
    (8, 20),
])
def test_win_points_decrease_by_ten_per_attempt(attempt, expected):
    assert update_score(0, "Win", attempt) == expected

@pytest.mark.parametrize("attempt", [9, 10, 20])
def test_win_points_have_a_floor_of_ten(attempt):
    assert update_score(0, "Win", attempt) == 10

def test_win_points_are_added_to_current_score():
    assert update_score(-15, "Win", 4) == -15 + 60

@pytest.mark.parametrize("attempt", [1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_wrong_guess_always_costs_five(outcome, attempt):
    # Regression: "Too High" used to give +5 on even attempts and -5 on odd.
    assert update_score(20, outcome, attempt) == 15

def test_repeated_wrong_guesses_never_raise_the_score():
    score = 0
    history = []
    for attempt in range(1, 9):
        score = update_score(score, "Too High", attempt)
        history.append(score)
    assert history == [-5, -10, -15, -20, -25, -30, -35, -40]

def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(30, "Something else", 3) == 30

# ---------- get_range_for_difficulty ----------

@pytest.mark.parametrize("difficulty, expected", [
    ("Easy", (1, 20)),
    ("Normal", (1, 100)),
    ("Hard", (1, 50)),
    ("Unknown", (1, 100)),
])
def test_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected
