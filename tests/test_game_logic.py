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

# ---------- edge cases: parse_guess ----------

@pytest.mark.parametrize("raw, expected", [
    (" 5 ", 5),        # surrounding whitespace is tolerated
    ("+7", 7),         # explicit plus sign
    ("0", 0),
    ("-3", -3),        # negatives parse; range is not enforced here
    ("5.", 5),         # trailing dot
    (".5", 0),         # decimals truncate toward zero
    ("-0.5", 0),
    ("7.999", 7),      # truncates, does not round
])
def test_parse_accepts_unusual_but_numeric_input(raw, expected):
    assert parse_guess(raw) == (True, expected, None)

@pytest.mark.parametrize("raw", [
    "1e3", "inf", "nan", "0x10", "5 5", "1.2.3", "--5", "5-", "five", "1,5", "!!",
])
def test_parse_rejects_non_numeric_input(raw):
    ok, value, err = parse_guess(raw)
    assert (ok, value) == (False, None)
    assert err == "That is not a number."

@pytest.mark.parametrize("raw", ["   ", "\t", "\n"])
def test_parse_rejects_whitespace_only_input(raw):
    ok, value, err = parse_guess(raw)
    assert (ok, value) == (False, None)
    assert err  # the player always gets some error message

def test_parse_huge_number_does_not_crash():
    ok, value, _ = parse_guess("9" * 30)
    assert ok is True
    assert value == int("9" * 30)

def test_parse_always_returns_a_three_tuple():
    for raw in [None, "", "abc", "5", "5.5", " ", "-1"]:
        result = parse_guess(raw)
        assert isinstance(result, tuple) and len(result) == 3
        ok, value, err = result
        # a valid parse has a value and no error; an invalid one is the reverse
        if ok:
            assert isinstance(value, int) and err is None
        else:
            assert value is None and isinstance(err, str)

# ---------- edge cases: check_guess ----------

@pytest.mark.parametrize("guess, secret, expected", [
    (1, 1, "Win"),              # lowest possible secret
    (100, 100, "Win"),          # highest Normal secret
    (1, 100, "Too Low"),
    (100, 1, "Too High"),
    (0, 1, "Too Low"),          # just below the range
    (101, 100, "Too High"),     # just above the range
    (-5, 1, "Too Low"),         # negative guess
    (10**30, 50, "Too High"),   # huge guess
    (-1, -2, "Too High"),       # negatives on both sides
])
def test_check_guess_edge_values(guess, secret, expected):
    assert check_guess(guess, secret)[0] == expected

def test_check_guess_always_returns_outcome_and_message():
    for guess, secret in [(1, 2), (2, 1), (3, 3)]:
        outcome, message = check_guess(guess, secret)
        assert outcome in {"Win", "Too High", "Too Low"}
        assert isinstance(message, str) and message

def test_check_guess_is_consistent_with_its_message():
    for guess in range(0, 11):
        outcome, message = check_guess(guess, 5)
        if outcome == "Too High":
            assert "LOWER" in message
        elif outcome == "Too Low":
            assert "HIGHER" in message
        else:
            assert guess == 5

# ---------- edge cases: update_score ----------

def test_win_points_are_exactly_ten_at_the_floor_boundary():
    assert update_score(0, "Win", 9) == 10   # 100 - 90
    assert update_score(0, "Win", 10) == 10  # 100 - 100 = 0, floored to 10

def test_score_can_go_negative_and_recover():
    score = 0
    for attempt in range(1, 4):
        score = update_score(score, "Too Low", attempt)
    assert score == -15
    assert update_score(score, "Win", 4) == -15 + 60

def test_win_on_the_last_attempt_still_scores_points():
    # Normal allows 8 attempts; the last one is still worth 20 points
    assert update_score(-35, "Win", 8) == -35 + 20

def test_update_score_does_not_mutate_or_depend_on_history():
    assert update_score(10, "Too High", 1) == update_score(10, "Too High", 2)
