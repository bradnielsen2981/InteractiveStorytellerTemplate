# Adding Choices to the Interactive Storyteller

Nov 9, 2026 · @Brad

In this activity you will make the storyteller give the player 3 numbered choices after each part of the story. The player can type a number to pick a choice, or type their own idea.

**When you finish, the game will look like this:**

```text
You stand before the enchanted Forest of Whispers...
  1. Follow the silver fox
  2. Pick the glowing moonflower
  3. Climb the tallest tree

Pick a number, type your own idea, or 'quit': 2
```

**Before you start:**

- Open `storyteller.py` and run it once (`python storyteller.py`). The story should appear and you can type what you do next.
- You will only change `storyteller.py`. Do not change `agent.py`.
- There are 4 changes to make. Run the program after each one to check it still works.

## Step 1: Ask the AI to give choices

The AI only does what the prompt asks. Right now the `TASK` tells it to ask the player what to do next, so it never gives choices.

Find this line near the top of the file:

```python
TASK = "Tell an interactive adventure story set in the magical kingdom of Eldoria. After each part, ask the player what they want to do next."
```

Change the end of it so the AI gives 3 choices:

```python
TASK = "Tell an interactive adventure story set in the magical kingdom of Eldoria. After each part, give the player 3 choices of what to do next."
```

**Check:** Run the program. The AI might now write the choices inside the story text. That's fine for now; Step 2 gives them their own place.

## Step 2: Add choices to the JSON format

`RESPONSE_FORMAT` shows the AI the shape of the reply we want. If we add a `"choices"` list, the AI sends the choices separately from the story, so our code can number them.

Find this:

```python
RESPONSE_FORMAT = {
    "story": "The next part of the story, as a string",
}
```

Add a `"choices"` line underneath `"story"`:

```python
RESPONSE_FORMAT = {
    "story": "The next part of the story, as a string",
    "choices": ["Choice 1", "Choice 2", "Choice 3"],
}
```

The square brackets `[ ]` make a **list**: one value that holds several items in order.

**Check:** Run the program. The story still prints, but you can't see the choices yet. They are hiding inside `data`.

## Step 3: Print the choices as a numbered list

`data` is a dictionary made from the AI's JSON reply. `data["story"]` is the story and `data["choices"]` is the list of choices. We use `data.get(...)` instead, because it gives a safe default if the AI forgets something.

Find Step 4 inside `main()`:

```python
        # Step 4: show the story
        print("\n" + data.get("story", ""))
```

Add the choices underneath it:

```python
        # Step 4: show the story and the choices
        print("\n" + data.get("story", ""))
        choices = data.get("choices", [])
        for number, choice in enumerate(choices, start=1):
            print(f"  {number}. {choice}")
```

How it works:

- `data.get("choices", [])` gets the list of choices, or an empty list `[]` if there are none.
- `enumerate(choices, start=1)` goes through the list and counts as it goes: 1, 2, 3.
- The `f"..."` string puts the number and the choice into one line, like `1. Follow the silver fox`.

Watch the indenting. These lines must line up with the `print` above them, inside the `while` loop.

**Check:** Run the program. You should see 3 numbered choices under the story.

## Step 4: Use the number the player types

If the player types `2`, the program currently sends just "2" to the AI. We want it to send the words of choice 2 instead.

**4a.** Change the question so the player knows they can type a number. Find:

```python
        answer = input("\nWhat do you do next? (or type 'quit'): ").strip()
```

Change it to:

```python
        answer = input("\nPick a number, type your own idea, or 'quit': ").strip()
```

**4b.** At the bottom of the loop, find:

```python
        # Send what the player typed as the next message
        user_input = answer
```

Replace it with:

```python
        # If they typed a number, use the matching choice
        if answer.isdigit() and 1 <= int(answer) <= len(choices):
            user_input = choices[int(answer) - 1]
        else:
            user_input = answer
```

How it works:

- `answer.isdigit()` is `True` only if the player typed a whole number, like `2`.
- `1 <= int(answer) <= len(choices)` checks the number is one of the choices. Typing `7` when there are 3 choices won't crash.
- `choices[int(answer) - 1]` takes away 1 because Python lists start counting at **0**. Choice 1 is `choices[0]`.
- `else` means anything else they typed, like "I run away", is sent to the AI as it is.

## Step 5: Test your game

Run `python storyteller.py` and try each of these:

- [ ] Type `1`, `2` or `3`. The story carries on with that choice.
- [ ] Type your own idea, like `I talk to the dragon`. The story follows your idea.
- [ ] Type a number that isn't a choice, like `7`. The game doesn't crash.
- [ ] Type `quit`. The game says "Thanks for playing!" and stops.

### If something goes wrong

| What you see | What to check |
| --- | --- |
| `IndentationError` | The new lines don't line up with the lines around them. Use 4 spaces for each level, not tabs. |
| `NameError: name 'choices' is not defined` | The `choices = data.get(...)` line from Step 3 is missing or misspelled. |
| `SyntaxError` | A missing `:` at the end of an `if`, `else` or `for` line, or a missing `"` or `)`. |
| No numbered choices appear | Check the `"choices"` line in `RESPONSE_FORMAT` (Step 2) and the `for` loop (Step 3). |
| "The AI didn't reply with valid JSON" | Run it again. The AI sometimes makes mistakes. If it keeps happening, check the commas in `RESPONSE_FORMAT`. |
| Typing a number picks the wrong choice | Check you wrote `int(answer) - 1`. |

### Extension challenges

1. Change the `TASK` so the AI gives 4 choices instead of 3. Do you need to change any other code?
2. Print a message like `You chose: Follow the silver fox` after the player picks a number.
3. Make the choices stand out by adding a heading such as `What will you do?` above the list.
