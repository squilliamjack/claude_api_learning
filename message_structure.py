"""
Message structure exploration.
Demonstrates system prompts, temperature control, and multi-turn conversation
using the Claude API.
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    temperature=0.0,
    system="You are a math tutor who only speaks in simple terms.",
    messages=[
        {"role": "user", "content": "What is a variable?"},
        {"role": "assistant", "content": "A variable is like a box that holds a number."},
        {"role": "user", "content": "Can you give me an example using x?"}
    ]
)

print("--- Multi-turn ---")
print(conversation.content[0].text)