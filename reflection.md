# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

When I first ran the game on Normal, it looked fine, but it wasn't playable. The hints pointed the wrong way, "Attempts left" started at 7 instead of 8, and a first-try win only scored 70. After a game ended, clicking "New Game" didn't let me play again; I had to refresh the page.

| Input / Trigger | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-----------------|-------------------|-----------------|------------------------|-------------------------|
| Guess 60, secret 50 | "Too High" with "📉 Go LOWER!" | "Too High" with "📈 Go HIGHER!" (hints swapped; a guess of 40 says "Go LOWER!") | none | `app.py`, `check_guess` (the messages for the two branches are swapped) |
| Guess 9, secret 50, on an even attempt | "Too Low" | "Too High" | none (a `TypeError` is caught internally) | `app.py` submit block casts the secret to `str` on even attempts; `check_guess`'s `except TypeError` fallback then compares strings, and `"9" > "50"` |
| Win or lose a game, then click "New Game" | A fresh game starts | Secret and attempts reset, but the game still says "You already won / Game over" and won't take guesses until the page is refreshed | none | `app.py`, `if new_game:` block (doesn't reset `status`, `score`, or `history`) |
| Wrong guess that's too high, on attempt 2 vs attempt 3 | -5 points each time | +5 on even attempts, -5 on odd attempts | none | `app.py`, `update_score`, `Too High` branch (`attempt_number % 2 == 0`) |
| Correct guess on the first try | 90 points | 70 points | none | `app.py`, `update_score` (`attempt_number + 1`) plus `attempts` starting at 1 instead of 0 |
| Type "abc" and submit | "That is not a number." with no attempt used | Error shown, but an attempt is used up; repeated bad input can run out the game | none | `app.py`, submit block (`attempts += 1` runs before `parse_guess`) |

Terminal output from calling the original starter functions directly with these inputs (`check_guess`, `update_score` from commit `f651d72`):

```
guess 60 vs secret 50: ('Too High', '📈 Go HIGHER!')
guess 9 vs secret '50' (even attempt): ('Too High', '📈 Go HIGHER!')
guess 40 vs secret 50: ('Too Low', '📉 Go LOWER!')
first-try win (attempts=2): 70
Too High on attempt 2: 5
Too High on attempt 3: -5
```

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I utilized Claude Code on Sonnet 5.5 Medium.

I utilized Claude Code to help me find the areas of code that had bugs or mistakes and I was able to see why the code was wrong and Claude gave good suggestions to fix the code.
I verified most of the bugs by going in and manually testing. 
For example, Claude helped explain that the hint messages were swapped, and that the secret was turned into a string on even attempts (the game decided too high/too low correctly, but the messages were swapped).
It suggested swapping the messages and always passing the secret as a number. As mentioned, I verified this by playing the game through the UI and by running pytest.

One example of an AI suggestion that I did not accept as is was all of the tests generated (after it went ahead and tried solving Challenge 1 on its own). I only had a question about it and it went ahead and generated tests without explanation. If completing the challenge, I would have it generate purposeful and useful tests generated after thinking through edge cases that are explained instead of accepting the tests as is. 
I verified the change by running pytest and confirming the original tests passed. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided that a bug was really fixed by manually verifying through the UI and playing the game. I also relied on passing the tests that existed.
For example, one test I ran was running pytest and ensuring that test_guess_too_high passed after fixing the bug which resulted in the wrong message being displayed.

One of the main bugs that I fixed was whether the game was offering the correct hint, depending on the inputted value and the secret. 

I had AI help explain the tests generated which were mostly used to verify the bugs we had fixed and it also generated a few additional tests that were used for general coverage. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

A rerun is when a Streamlit app reruns the whole script whenever the user does anything. This is why variables that are not stored in the session state (which is a dictionary that does not refresh on reruns) are forgotten or recalculated. 
For example, when clicking "New Game", it reset the secret number but did not reset the game status, so we could not play the game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I would definitely reuse is manually confirming the AI fixes (by both inspecting code and verifying through the UI).
One thing I would do differently next time I work with AI is to have small, separate commits so that I can better document my work.
This project made me realize that AI is very capable and generates good code, but it is always important to verify the changes. 