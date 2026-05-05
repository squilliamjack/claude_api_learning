""" 
This script compares the differences in output from Sonnet and Haiku 
Claude API models.
"""

import  anthropic
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = "A 9th grade student is struggling with solving two-step equations. Explain the concept and give one example."
model_haiku = "claude-haiku-4-5-20251001"
model_sonnet = "claude-sonnet-4-6"

haiku_response = client.messages.create(
    model = model_haiku,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

sonnet_response = client.messages.create(
    model = model_sonnet,
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("---\n")
print(haiku_response.content[0].text)
print("---\n")
print(f"INPUT TOKENS: {haiku_response.usage.input_tokens}")
print("---\n")
print(f"OUTPUT TOKENS: {haiku_response.usage.output_tokens}")
print("---\n")
print("---\n")
print("---\n")
print(sonnet_response.content[0].text)
print("---\n")
print(f"INPUT TOKENS: {sonnet_response.usage.input_tokens}")
print("---\n")
print(f"OUTPUT TOKENS: {sonnet_response.usage.output_tokens}")

def log_call(prompt, response):

    """
    This function takes a prompt and the AI-generated response and writes the model name, 
    number of input and output tokens, timestamp and prompt itself to call_log.json
    """

    log_entry = {
        "model name": response.model,
        "input tokens": response.usage.input_tokens,
        "output tokens": response.usage.output_tokens,
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt
    }
    
    try:
        with open("call_log.json", "r") as f:
            log = json.load(f)
    except FileNotFoundError:
            log=[]

    log.append(log_entry)

    with open("call_log.json", "w") as f:
        json.dump(log, f, indent=4)

log_call(prompt, haiku_response)
log_call(prompt, sonnet_response)

