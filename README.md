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

- [x] Describe the game's purpose.
      Game Glitch Investigator is a Streamlit number-guessing game. The player picks a difficulty (Easy 1-20, Normal 1-100, Hard 1-50) and tries to guess a secret number within a limited number of attempts. After each guess the game gives a "higher/lower" hint and updates a score: wrong guesses cost 5 points, and a win earns more points the fewer attempts it takes. The starter version was written by an AI and full of bugs; the goal of this project was to find, fix, and test them.
- [x] Detail which bugs you found.
      bug 1: incorrect hint logic and hacky code logic surrounding it (the secret is cast as a str when guesses are even, causing a TypeError which led to having more code to workaround it)
      bug 2: secret resets, but the state does not when clicking "New Game", preventing the game from being played (had to refresh the page to reset the game properly)
      bug 3: Too-high guesses gave +5 or -5 depending on whether the attempted number was even or odd. 
      bug 4: First guess win only gives 70 points
      bug 5: Invalid input can push attempts past the limit and never end the game
- [x] Explain what fixes you applied.
      bug 1: swapped the hint logic and removed the code which casts the secret as an str on even attempts which allowed us to remove the hacky code
      bug 2: "New Game" now resets the state and also fixed a bug where you had to submit twice in order to receive the hint
      bug 3: Every wrong guess now costs 5 points
      bug 4: First try win now gives 90 points by removing a +1 and starting the counter at 0
      bug 5: Invalid input no longer uses an attempt


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

A sample game on Normal (range 1-100, 8 attempts), where the secret number is 63:

1. The game starts with "Guess a number between 1 and 100. Attempts left: 8" and a score of 0.
2. User enters 40. The game shows "📈 Go HIGHER!". Score is now -5, attempts left: 7.
3. User enters "abc". The game shows "That is not a number." No attempt is used; attempts left is still 7.
4. User enters 80. The game shows "📉 Go LOWER!". Score is now -10, attempts left: 6.
5. User enters 63. Balloons appear and the game shows "You won! The secret was 63. Final score: 60." (A win on attempt 3 earns 100 - 10 × 3 = 70 points.)
6. Further guesses are ignored while the win message stays on screen.
7. User clicks "New Game 🔁". The game shows "New game started.", score resets to 0, attempts left resets to 8, and a new secret is picked.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
configfile: pytest.ini
testpaths: tests
collected 65 items

tests\test_app_flow.py ......................                            [ 33%]
tests\test_game_logic.py ...........................................     [100%]

============================= 65 passed in 9.19s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
