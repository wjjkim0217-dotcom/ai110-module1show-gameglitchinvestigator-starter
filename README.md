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

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```
===================================== 65 passed in 6.05s =====================================

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
