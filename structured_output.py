import anthropic 
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

student_answer = "Name: Wil Jackson. Topic: Trigonometry. Answer: I think cos theta is also 1/2 because sin and cos are related."

step1 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="you are analyzing a student's answer to a math problem and identifying what they got right, what they got wrong, and what concept they're missing. ", 
    messages=[
        {"role": "user", "content": f"The question is: given sin theta is 1/2 and theta is in Q1, what is cos theta? The student answered: {student_answer}"}
    ]
)

analysis = step1.content[0].text
print("--- Step 1: Analysis ---")
print(analysis)

step2 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="You must return only raw JSON with no markdown formatting, no code fences, and no other text.", 
    messages=[
        {"role": "user", "content": f"return a JSON file that contains the followwing based on {analysis}: student_name, topic, score, strengths, gaps, feedback, next_steps"}
    ]
)

raw = step2.content[0].text
raw = raw.strip()
if raw.startswith("```"):
    raw = raw.split("\n", 1)[1]
if raw.endswith("```"):
    raw = raw.rsplit("```", 1)[0]
raw = raw.strip()

print("\n--- Step 2: Structured Output ---")
print(raw)

result = json.loads(raw)

with open("student_feedback.json", "w") as f:
    json.dump(result, f, indent=4)

print("\nSaved to student_feedback.json")