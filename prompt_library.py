import anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# prompt1 = "generating a personalized feedback email for a student after a tutoring session. " \

# message1 = client.messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     messages=[
#         {"role": "user", "content": prompt1}
#     ]
# )


# print(message1.content[0].text)

# prompt2 = "generating a personalized feedback email for a student after a tutoring session. " \
# "student name: Wil Jackson. " \
# "grade: 10. " \
# "class: high school geometry. " \
# "topic  covered: basic trig functions. " \
# "strengths: core algebra and arithmetic. " \
# "struggles: implementation of trig functions. " \
# "my name: John Smith. " \
# "session date: 3/30/2026. " \
# "homework assigned: 3.1 #1-11 odd" \
# "next session date: 4/6/2026. "


# message2 = client.messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     messages=[
#         {"role": "user", "content": prompt2}
#     ]
# )

# print(message2.content[0].text)

prompt3 = "generating a personalized feedback email for a student after a tutoring session. " \
"student name: Wil Jackson. " \
"grade: 10. " \
"class: high school geometry. " \
"topic  covered: basic trig functions. " \
"strengths: core algebra and arithmetic. " \
"struggles: implementation of trig functions. " \
"my name: John Smith. " \
"session date: 3/30/2026. " \
"homework assigned: 3.1 #1-11 odd" \
"next session date: 4/6/2026. " \
"tone preference: warm and encouraging. not too formal. " \
"tone reference example: hey Wil! just wanted to say again how great you did during our first session. i really hope we can keep getting you to feel more and more confident in math. i know you can get the hang of it, and you were already starting to catch on to those trig functions even in the first hour!"


message3 = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt3}
    ]
)

print(message3.content[0].text)

library_entry = {
    "use_case": "student_feedback_email",
    "v1": "generating a personalized feedback email for a student after a tutoring session.",
    "v2": "generating a personalized feedback email for a student after a tutoring session. " \
"student name: Wil Jackson. " \
"grade: 10. " \
"class: high school geometry. " \
"topic  covered: basic trig functions. " \
"strengths: core algebra and arithmetic. " \
"struggles: implementation of trig functions. " \
"my name: John Smith. " \
"session date: 3/30/2026. " \
"homework assigned: 3.1 #1-11 odd" \
"next session date: 4/6/2026. ",
    "v3": "generating a personalized feedback email for a student after a tutoring session. " \
"student name: Wil Jackson. " \
"grade: 10. " \
"class: high school geometry. " \
"topic  covered: basic trig functions. " \
"strengths: core algebra and arithmetic. " \
"struggles: implementation of trig functions. " \
"my name: John Smith. " \
"session date: 3/30/2026. " \
"homework assigned: 3.1 #1-11 odd" \
"next session date: 4/6/2026. " \
"tone preference: warm and encouraging. not too formal. " \
"tone reference example: hey Wil! just wanted to say again how great you did during our first session. i really hope we can keep getting you to feel more and more confident in math. i know you can get the hang of it, and you were already starting to catch on to those trig functions even in the first hour!",
    "notes": "v3 produces best results — warm tone, specific details, reference example included"
}

with open("prompt_library.json", "w") as f:
    json.dump(library_entry, f, indent=4)

print("Prompt library saved.")