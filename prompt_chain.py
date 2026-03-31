import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

student_answer = "I think cos theta is also 1/2 because sin and cos are related."

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
    system="you are a warm, encouraging math tutor writing brief feedback to a student.", 
    messages=[
        {"role": "user", "content": f"Based on this analysis of a student's work, write a short encouraging feedback message:\n\n{analysis}"}
    ]
)

print("\n--- Step 2: Feedback ---")
print(step2.content[0].text)