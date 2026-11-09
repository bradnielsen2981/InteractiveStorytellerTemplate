# This file is the interactive story game. It decides WHAT to say to the AI
# (by building the prompt) and uses an Agent from agent.py to actually send it.

import sys     # lets us fix how text is printed on Windows
import json    # lets us turn the AI's JSON reply into a Python dictionary

from agent import Agent  # our simple agent that talks to the AI


# These four pieces of text describe the storyteller's personality and job.
# Try changing them to make a completely different story!
ROLE = "You are a friendly narrator of a fantasy adventure story."
TASK = "Tell an interactive adventure story set in the magical kingdom of Eldoria. After each part, ask the player what they want to do next."
CONSTRAINTS = "Keep each part of the story under 100 words and suitable for school students."
BEHAVIOUR = "Speak in a warm, exciting storytelling voice."

# The shape of the JSON we want the AI to reply with.
# Asking for JSON means our code can easily pull out each piece (like the story).
RESPONSE_FORMAT = {
    "story": "The next part of the story, as a string",
}


def build_prompt(user_input, history, response_format):
    """Join the storyteller's description, the history, the new message
    and the JSON format into one piece of text for the agent."""
    prompt = (
        f"Role: {ROLE}\n"
        f"Task: {TASK}\n"
        f"Constraints: {CONSTRAINTS}\n"
        f"Behaviour: {BEHAVIOUR}\n\n"
        f"Reply ONLY with JSON in exactly this format, and nothing else:\n"
        f"{json.dumps(response_format, indent=2)}\n\n"
        f"Conversation history:\n{history}\n\n"
        f"User: {user_input}\n"
        f"Assistant:"
    )
    return prompt


def read_json_reply(reply):
    """Turn the AI's reply text into a Python dictionary.
    Returns None if the AI didn't send valid JSON."""
    # Some models wrap JSON in ```json ... ``` so we cut out just the { ... } part
    start = reply.find("{")
    end = reply.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(reply[start:end + 1])
    except json.JSONDecodeError:
        return None


def main():
    # Let Windows print any character the AI uses (like emojis or fancy dashes)
    sys.stdout.reconfigure(encoding="utf-8")

    # Create the agent (it uses the API key saved in agent.py)
    narrator = Agent()

    # The conversation so far. The AI has no memory of its own,
    # so we send the whole history inside every new prompt.
    history = ""

    user_input = "Begin the story."

    while True:
        # Step 1: build the prompt and hand it to the agent
        prompt = build_prompt(user_input, history, RESPONSE_FORMAT)
        narrator.set_current_prompt(prompt)

        # Step 2: ask the agent to send it and get the reply
        reply = narrator.get_response()

        # Step 3: turn the JSON reply into a dictionary
        data = read_json_reply(reply)
        if data is None:
            print("\n(The AI didn't reply with valid JSON. Here is what it said:)")
            print(reply)
            break

        # Step 4: show the story
        print("\n" + data.get("story", ""))

        # Step 5: remember this exchange for next time
        history = history + f"\nUser: {user_input}\nAssistant: {reply}"

        # Step 6: ask the player what to do next
        answer = input("\nWhat do you do next? (or type 'quit'): ").strip()
        if answer.lower() == "quit":
            print("Thanks for playing!")
            break

        # Send what the player typed as the next message
        user_input = answer


# Only start the game when this file is run directly (python storyteller.py)
if __name__ == "__main__":
    main()
