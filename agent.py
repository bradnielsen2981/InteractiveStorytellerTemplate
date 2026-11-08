import os                  # lets us read settings from the computer, like the API key
from openai import OpenAI  # the library that sends our messages to the AI model


class Agent:
    """An agent that sends a prompt to an AI model and returns the reply."""

    # __init__ runs automatically every time we create a new agent with Agent().
    # "self" means "this particular agent".
    def __init__(self, api_key=None, model="cohere/north-mini-code:free"):
        # If no API key was given, look for one saved on the computer
        if api_key is None:
            api_key = os.getenv("OPENROUTER_API_KEY")

        # The client is the object that actually connects to the AI over the internet.
        # We use OpenRouter, which gives us access to lots of different AI models.
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        # Which AI model this agent uses
        self.model = model

        # The prompt the agent will send next time we call get_response()
        self.current_prompt = ""

        # The prompt the agent had before the current one, so we can compare them
        self.last_prompt = ""

        # A limit on how long (in tokens) the AI's reply can be.
        # A token is roughly one short word or part of a longer word.
        self.max_reply_tokens = 1024

        # Token counts from the most recent message (useful for seeing how much we used)
        self.prompt_tokens = 0  # tokens we sent to the AI
        self.reply_tokens = 0   # tokens the AI sent back
        self.total_tokens = 0   # both added together

        # The full response the AI sent back last time (includes the reply and token counts)
        self.last_response = None

    def set_current_prompt(self, prompt):
        """Give the agent a new prompt. The old one is kept in last_prompt."""
        self.last_prompt = self.current_prompt
        self.current_prompt = prompt

    def get_response(self):
        """Send the current prompt to the AI and return the AI's reply as text."""

        # Step 1: send the current prompt to the AI model and wait for an answer
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.current_prompt}],
            max_tokens=self.max_reply_tokens,
        )
        self.last_response = response  # keep a copy so we can look at it later

        # Step 2: pull the reply text out of the response
        reply = response.choices[0].message.content
        if reply is None:
            reply = ""  # sometimes the model sends back nothing

        # Step 3: record how many tokens were used (if the model told us)
        if response.usage is not None:
            self.prompt_tokens = response.usage.prompt_tokens
            self.reply_tokens = response.usage.completion_tokens
            self.total_tokens = response.usage.total_tokens

        return reply

    def get_context_window(self):
        """Ask OpenRouter how many tokens this agent's model can handle at once."""
        # Get the list of every model OpenRouter offers
        for model_info in self.client.models.list():
            # Find the one this agent is using
            if model_info.id == self.model:
                return model_info.context_length
        return None  # the model name wasn't found


def setup():
    """Get the computer ready to talk to the AI."""
    # Load the API key from the .env file so os.getenv() can find it
    from dotenv import load_dotenv
    load_dotenv()

    # Let Windows print any character the AI uses (like emojis or fancy dashes)
    import sys
    sys.stdout.reconfigure(encoding="utf-8")


def test_model(model=None):
    """Create an agent, give it a simple prompt and print the reply."""
    # Use the agent's default model if none was given
    if model is None:
        agent = Agent()
    else:
        agent = Agent(model=model)

    agent.set_current_prompt("Say hello to a class of students in one sentence.")
    reply = agent.get_response()

    print("Reply:", reply)

    # Show the full response the AI sent back, formatted as JSON
    print("Full response:")
    print(agent.last_response.model_dump_json(indent=2))
    print("Prompt tokens:", agent.prompt_tokens)
    print("Reply tokens:", agent.reply_tokens)


# This part only runs when you run this file directly (python agent.py),
# not when another file imports it.
if __name__ == "__main__":
    setup()
    test_model()
