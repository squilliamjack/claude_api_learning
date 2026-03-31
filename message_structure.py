import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# prompt = "Give me a creative analogy to explain what a variable is in math."

# low_temp = client.messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     temperature=0.0,
#     system="respond only like a math tutor who speaks in simple terms",
#     messages=[
#         {"role": "user", "content": prompt}
#     ]

# )

# high_temp = client.messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     temperature=1.0,
#     system="respond only like a math tutor who speaks in simple terms",
#     messages=[
#         {"role": "user", "content": prompt}
#     ]

# )

# print("--- Temperature 0.0 ---")
# print(low_temp.content[0].text)
# print("--- Temperature 1.0 ---")
# print(high_temp.content[0].text)

conversation = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    temperature=0.0,
    system="You are a math tutor who only speaks in simple terms.",
    messages=[
        {"role": "user", "content": "What is a variable?"},
        {"role": "assistant", "content": "A variable is like a boax that holds a number."},
        {"role": "user", "content": "Can you give me an example suing x?"}
    ]
)

print("--- Multi-turn ---")
print(conversation.content[0].text)