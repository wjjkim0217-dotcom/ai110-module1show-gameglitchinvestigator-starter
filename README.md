# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
      bug 1: incorrect hint logic and hacky code logic surrounding it (the secret is cast as a str when guesses are even, causing a TypeError which led to having more code to workaround it)
      bug 2: secret resets, but the state does not when clicking "New Game", preventing the game from being played (had to refresh the page to reset the game properly)
      bug 3: Too-high guesses gave +5 or -5 depending on whether the attempted number was even or odd. 
      bug 4: First guess win only gives 70 points
      bug 5: Invalid input can push attempts past the limit and never end the game
- [ ] Explain what fixes you applied.
      bug 1: swapped the hint logic and removed the code which casts the secret as an str on event attempts which allowed us to remove the hacky code
      bug 2: "New Game" now resets the state and also fixed a bug where you had to submit twice in order to receive the hint
      bug 3: Every wrong guess now costs 5 points
      bug 4: First try win now gives 90 points by removing a +1 and starting the counter at 1
      bug 5: Invalid input no longer uses an attempt


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Enter a number between 1 and 100
2. Follow the hint and guess lower or higher
3. Try 7 more times 
4. Click "New Game" to start again!

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

Challenge 1 (Advanced Edge-Case Testing): `pytest -v` output, including the edge-case tests
for `parse_guess`, `check_guess`, `update_score` and the full app flow.

```
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\wjkim\Documents\ai110-module1show-gameglitchinvestigator-starter\.venv\Scripts\python.exe
rootdir: C:\Users\wjkim\Documents\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1
collecting ... collected 117 items
tests/test_app_flow.py::test_game_starts_with_full_attempts PASSED       [  0%]
tests/test_app_flow.py::test_invalid_input_does_not_use_an_attempt[] PASSED [  1%]
tests/test_app_flow.py::test_invalid_input_does_not_use_an_attempt[abc] PASSED [  2%]
tests/test_app_flow.py::test_invalid_input_does_not_use_an_attempt[1,5] PASSED [  3%]
tests/test_app_flow.py::test_invalid_input_does_not_use_an_attempt[!!] PASSED [  4%]
tests/test_app_flow.py::test_invalid_input_cannot_push_attempts_past_the_limit PASSED [  5%]
tests/test_app_flow.py::test_attempts_left_updates_immediately_after_a_guess PASSED [  5%]
tests/test_app_flow.py::test_game_ends_after_the_attempt_limit PASSED    [  6%]
tests/test_app_flow.py::test_no_loss_before_the_last_attempt PASSED      [  7%]
tests/test_app_flow.py::test_loss_message_shows_secret_and_score PASSED  [  8%]
tests/test_app_flow.py::test_loss_message_persists_across_reruns PASSED  [  9%]
tests/test_app_flow.py::test_win_message_shows_score_and_persists PASSED [ 10%]
tests/test_app_flow.py::test_guesses_after_the_game_is_over_are_ignored PASSED [ 11%]
tests/test_app_flow.py::test_first_try_win_scores_ninety PASSED          [ 11%]
tests/test_app_flow.py::test_wrong_guesses_each_cost_five_in_the_app PASSED [ 12%]
tests/test_app_flow.py::test_hint_points_the_right_way PASSED            [ 13%]
tests/test_app_flow.py::test_secret_does_not_change_between_guesses PASSED [ 14%]
tests/test_app_flow.py::test_new_game_resets_everything PASSED           [ 15%]
tests/test_app_flow.py::test_new_game_clears_the_input_box PASSED        [ 16%]
tests/test_app_flow.py::test_can_lose_again_after_new_game PASSED        [ 17%]
tests/test_app_flow.py::test_can_win_after_losing_and_starting_a_new_game PASSED [ 17%]
tests/test_app_flow.py::test_new_game_secret_respects_the_difficulty_range PASSED [ 18%]
tests/test_app_flow.py::test_whitespace_only_input_does_not_use_an_attempt[   ] PASSED [ 19%]
tests/test_app_flow.py::test_whitespace_only_input_does_not_use_an_attempt[\t] PASSED [ 20%]
tests/test_app_flow.py::test_out_of_range_guesses_are_accepted_and_hinted[-5-HIGHER] PASSED [ 21%]
tests/test_app_flow.py::test_out_of_range_guesses_are_accepted_and_hinted[0-HIGHER] PASSED [ 22%]
tests/test_app_flow.py::test_out_of_range_guesses_are_accepted_and_hinted[999-LOWER] PASSED [ 23%]
tests/test_app_flow.py::test_decimal_guess_is_truncated_and_counted PASSED [ 23%]
tests/test_app_flow.py::test_winning_on_the_last_attempt_is_a_win_not_a_loss PASSED [ 24%]
tests/test_app_flow.py::test_attempt_limit_and_range_follow_the_difficulty[Easy-6-20] PASSED [ 25%]
tests/test_app_flow.py::test_attempt_limit_and_range_follow_the_difficulty[Hard-5-50] PASSED [ 26%]
tests/test_app_flow.py::test_repeated_new_game_clicks_are_safe PASSED    [ 27%]
tests/test_app_flow.py::test_new_game_in_the_middle_of_a_round_discards_progress PASSED [ 28%]
tests/test_app_flow.py::test_hint_checkbox_off_hides_the_hint_but_still_scores PASSED [ 29%]
tests/test_app_flow.py::test_history_records_valid_and_invalid_input_in_order PASSED [ 29%]
tests/test_game_logic.py::test_winning_guess PASSED                      [ 30%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 31%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 32%]
tests/test_game_logic.py::test_check_guess_compares_numbers_not_strings[9-50-Too Low] PASSED [ 33%]
tests/test_game_logic.py::test_check_guess_compares_numbers_not_strings[100-20-Too High] PASSED [ 34%]
tests/test_game_logic.py::test_check_guess_compares_numbers_not_strings[2-10-Too Low] PASSED [ 35%]
tests/test_game_logic.py::test_check_guess_compares_numbers_not_strings[10-2-Too High] PASSED [ 35%]
tests/test_game_logic.py::test_check_guess_hint_matches_direction_at_boundaries PASSED [ 36%]
tests/test_game_logic.py::test_check_guess_has_no_string_fallback PASSED [ 37%]
tests/test_game_logic.py::test_parse_valid_guess PASSED                  [ 38%]
tests/test_game_logic.py::test_parse_decimal_guess_truncates PASSED      [ 39%]
tests/test_game_logic.py::test_parse_blank_or_none_guess PASSED          [ 40%]
tests/test_game_logic.py::test_parse_non_numeric_guess PASSED            [ 41%]
tests/test_game_logic.py::test_win_points_decrease_by_ten_per_attempt[1-90] PASSED [ 41%]
tests/test_game_logic.py::test_win_points_decrease_by_ten_per_attempt[2-80] PASSED [ 42%]
tests/test_game_logic.py::test_win_points_decrease_by_ten_per_attempt[5-50] PASSED [ 43%]
tests/test_game_logic.py::test_win_points_decrease_by_ten_per_attempt[8-20] PASSED [ 44%]
tests/test_game_logic.py::test_win_points_have_a_floor_of_ten[9] PASSED  [ 45%]
tests/test_game_logic.py::test_win_points_have_a_floor_of_ten[10] PASSED [ 46%]
tests/test_game_logic.py::test_win_points_have_a_floor_of_ten[20] PASSED [ 47%]
tests/test_game_logic.py::test_win_points_are_added_to_current_score PASSED [ 47%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-1] PASSED [ 48%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-2] PASSED [ 49%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-3] PASSED [ 50%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-4] PASSED [ 51%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-5] PASSED [ 52%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-6] PASSED [ 52%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-7] PASSED [ 53%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too High-8] PASSED [ 54%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-1] PASSED [ 55%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-2] PASSED [ 56%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-3] PASSED [ 57%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-4] PASSED [ 58%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-5] PASSED [ 58%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-6] PASSED [ 59%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-7] PASSED [ 60%]
tests/test_game_logic.py::test_wrong_guess_always_costs_five[Too Low-8] PASSED [ 61%]
tests/test_game_logic.py::test_repeated_wrong_guesses_never_raise_the_score PASSED [ 62%]
tests/test_game_logic.py::test_unknown_outcome_leaves_score_unchanged PASSED [ 63%]
tests/test_game_logic.py::test_range_for_difficulty[Easy-expected0] PASSED [ 64%]
tests/test_game_logic.py::test_range_for_difficulty[Normal-expected1] PASSED [ 64%]
tests/test_game_logic.py::test_range_for_difficulty[Hard-expected2] PASSED [ 65%]
tests/test_game_logic.py::test_range_for_difficulty[Unknown-expected3] PASSED [ 66%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[ 5 -5] PASSED [ 67%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[+7-7] PASSED [ 68%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[0-0] PASSED [ 69%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[-3--3] PASSED [ 70%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[5.-5] PASSED [ 70%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[.5-0] PASSED [ 71%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[-0.5-0] PASSED [ 72%]
tests/test_game_logic.py::test_parse_accepts_unusual_but_numeric_input[7.999-7] PASSED [ 73%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[1e3] PASSED [ 74%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[inf] PASSED [ 75%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[nan] PASSED [ 76%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[0x10] PASSED [ 76%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[5 5] PASSED [ 77%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[1.2.3] PASSED [ 78%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[--5] PASSED [ 79%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[5-] PASSED [ 80%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[five] PASSED [ 81%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[1,5] PASSED [ 82%]
tests/test_game_logic.py::test_parse_rejects_non_numeric_input[!!] PASSED [ 82%]
tests/test_game_logic.py::test_parse_rejects_whitespace_only_input[   ] PASSED [ 83%]
tests/test_game_logic.py::test_parse_rejects_whitespace_only_input[\t] PASSED [ 84%]
tests/test_game_logic.py::test_parse_rejects_whitespace_only_input[\n] PASSED [ 85%]
tests/test_game_logic.py::test_parse_huge_number_does_not_crash PASSED   [ 86%]
tests/test_game_logic.py::test_parse_always_returns_a_three_tuple PASSED [ 87%]
tests/test_game_logic.py::test_check_guess_edge_values[1-1-Win] PASSED   [ 88%]
tests/test_game_logic.py::test_check_guess_edge_values[100-100-Win] PASSED [ 88%]
tests/test_game_logic.py::test_check_guess_edge_values[1-100-Too Low] PASSED [ 89%]
tests/test_game_logic.py::test_check_guess_edge_values[100-1-Too High] PASSED [ 90%]
tests/test_game_logic.py::test_check_guess_edge_values[0-1-Too Low] PASSED [ 91%]
tests/test_game_logic.py::test_check_guess_edge_values[101-100-Too High] PASSED [ 92%]
tests/test_game_logic.py::test_check_guess_edge_values[-5-1-Too Low] PASSED [ 93%]
tests/test_game_logic.py::test_check_guess_edge_values[1000000000000000000000000000000-50-Too High] PASSED [ 94%]
tests/test_game_logic.py::test_check_guess_edge_values[-1--2-Too High] PASSED [ 94%]
tests/test_game_logic.py::test_check_guess_always_returns_outcome_and_message PASSED [ 95%]
tests/test_game_logic.py::test_check_guess_is_consistent_with_its_message PASSED [ 96%]
tests/test_game_logic.py::test_win_points_are_exactly_ten_at_the_floor_boundary PASSED [ 97%]
tests/test_game_logic.py::test_score_can_go_negative_and_recover PASSED  [ 98%]
tests/test_game_logic.py::test_win_on_the_last_attempt_still_scores_points PASSED [ 99%]
tests/test_game_logic.py::test_update_score_does_not_mutate_or_depend_on_history PASSED [100%]
============================= 117 passed in 8.24s =============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
