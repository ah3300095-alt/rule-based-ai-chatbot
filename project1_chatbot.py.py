"""
DecodeLabs - Artificial Intelligence Internship
Project 1: Rule-Based AI Chatbot (v2 - Keyword Matching)

Goal:
    Create a rule-based chatbot that responds to user inputs using
    keyword/pattern matching instead of rigid exact-match lookup,
    running inside a continuous loop until an exit command is given.

Key Requirements covered:
    - Continuous input loop (while True)
    - Input sanitization (lowercase + strip whitespace)
    - Knowledge base organized by INTENT, each with several trigger
      keywords/phrases -> much more forgiving of how the user phrases
      things than a plain dictionary of exact strings
    - Fallback response for unrecognized input
    - Clean exit strategy (break on exit command)

Why this is more "responsive" than v1:
    v1 used responses.get(user_input, ...), which only fires if the
    ENTIRE input matches a key EXACTLY. "how are you" worked, but
    "how are you doing today?" did not, because as a string it's
    different from the key.

    v2 instead loops through a list of (keywords, response) rules and
    checks if ANY keyword/phrase appears ANYWHERE inside the user's
    input (using "in", i.e. substring search). This means:
        "how are you"          -> matches
        "how are you doing"    -> matches
        "how's life going"     -> matches (via "life" keyword)
        "what are you up to"   -> matches (via "up to" keyword)
    all trigger the same intent, without needing a huge dictionary of
    every possible exact phrasing.
"""

import random
import re

# ---------------------------------------------------------
# PHASE 1: KNOWLEDGE BASE
# ---------------------------------------------------------
# Each entry is: (intent_name, [list of trigger keywords/phrases], [list of possible responses])
#
# - Keywords are checked with "in", so "life" will match "how's life",
#   "life is good", "tell me about life", etc.
# - Multiple responses per intent are picked at random so the bot
#   doesn't sound like it's reading from a script every time.

intents = [
    (
        "greeting",
        ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"],
        [
            "Hi there! How can I help you today?",
            "Hello! What can I do for you?",
            "Hey! Good to see you.",
        ],
    ),
    (
        "wellbeing",
        ["how are you", "how're you", "how you doing", "how is it going",
         "how's it going", "how's life", "how is life", "what's up", "whats up",
         "how have you been"],
        [
            "I'm just a bunch of if-else logic, but I'm doing great! How about you?",
            "Running smoothly, thanks for asking! How are you?",
            "Can't complain — I'm code, not a person, but life (or lack of it) is good!",
        ],
    ),
    (
        "activity",
        ["what are you doing", "what are you up to", "what you doing", "doing right now"],
        [
            "Right now I'm just waiting for your next message!",
            "Processing your words and figuring out how to reply — the usual.",
        ],
    ),
    (
        "identity",
        ["what is your name", "who are you", "your name"],
        ["I'm RuleBot, your friendly rule-based AI assistant."],
    ),
    (
        "capabilities",
        ["what can you do", "what do you do","can you read?" ,"your features", "capabilities"],
        ["I can respond to a few basic topics — greetings, how you're doing, "
         "my name, and more. Try 'help' to see the full list."],
    ),
    (
        "help",
        ["help", "commands", "options"],
        ["You can talk to me about: greetings, how I'm doing, what I'm up to, "
         "my name, my capabilities, or just say thanks/bye."],
    ),
    (
        "gratitude",
        ["thank you", "thanks", "appreciate it"],
        ["You're welcome!", "Anytime!", "Glad I could help!"],
    ),
    (
        "mood_bot_feelings",
        ["are you okay", "are you sad", "are you happy", "how do you feel"],
        ["As code I don't really have feelings, but thanks for checking in!"],
    ),
]

# Exit commands that will break the loop (Kill Command)
exit_commands = {"exit", "bye", "quit", "goodbye", "see you"}

FALLBACK_RESPONSES = [
    "I do not understand yet. Type 'help' to see what I can talk about.",
    "Hmm, I'm not trained to answer that one. Try 'help' for topics I know.",
]


def get_response(user_input: str) -> str:
    """
    PHASE 2: PROCESS
    Scans the sanitized input for known keywords/phrases belonging to
    each intent. Returns a (random) response for the first matching
    intent, or a fallback if nothing matches.
    """
    for intent_name, keywords, possible_replies in intents:
        for keyword in keywords:
            # \b = word boundary, so "hi" matches "hi there" but NOT
            # the "hi" hidden inside "this" or "hire".
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, user_input):
                return random.choice(possible_replies)

    return random.choice(FALLBACK_RESPONSES)


def run_chatbot():
    """
    PHASE 3: THE HEARTBEAT (Infinite Loop)
    Keeps the chatbot alive until the user issues a Kill Command.
    """
    print("RuleBot: Hello! I'm your rule-based chatbot. Type 'bye' to exit.")

    while True:
        # ---- INPUT ----
        raw_input_text = input("You: ")

        # ---- SANITIZATION ----
        clean_input = raw_input_text.lower().strip()

        # ---- EXIT STRATEGY ----
        if clean_input in exit_commands or any(cmd in clean_input for cmd in exit_commands):
            print("RuleBot: Goodbye! Have a great day.")
            break

        # ---- OUTPUT ----
        reply = get_response(clean_input)
        print(f"RuleBot: {reply}")


if __name__ == "__main__":
    run_chatbot()
