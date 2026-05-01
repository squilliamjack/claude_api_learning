"""
This script takes example_math_problem.png, encodes it and passes it to the Claude API. It then asks Claude to respond with a JSON that includes the 
topic, grade_level, difficulty, and the problem itself. This JSON is parsed and passed back to Claude. Claude is then asked to generate 3 practice problems
based on the example given with varying difficulties and format the response in md format.
"""

import anthropic
import os
from dotenv import load_dotenv
import json
import base64
import sys

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

file_name = input("Please type the name of the file you wish to upload: ")

try:
    with open(file_name, "rb") as f:
        image = f.read()
        image_data = base64.b64encode(image).decode("utf-8")
except FileNotFoundError:
    print("Image not found.")
    sys.exit()

model = "claude-sonnet-4-6"
tokens = 1024

prompt1 = """
            Your job is to identify the math problem in the given image and return raw JSON only as your response with the given paramaters: topic, grade_level, difficulty, extracted_problem.

            Follow these steps exactly:
            <steps>
            1. Extract the math problem
            2. Identify the math topic
            3. Identify the grade level
            4. Identify the difficulty on a scale of 1-10 (1 being the least difficult, 10 being the most difficult)
            5. Format your response as a JSON
            </steps>

            Example JSON format to follow:
            <JSON_example>
            {
                "topic": "Triangle Congruence",
                "grade_level": "8th-10th Grade Geometry",
                "difficulty": "6",
                "extracted_problem": "Given △XPS ≅ △DNF, find the values of x and y. △XPS ≅ △DNF. Side XS = 17x + 3. Side XP = 4y - 3. Side DN = 57. Side NF = 51. Side FD = 54"
            }

            Respond with raw JSON only. No markdown, no code fences, no explanation.

""" 

error_prompt = """
                You were asked to respond in raw JSON only with no markdown and no code fences and no explanation. 
                Your response triggered json.JSONDecodeError which means you did not do this properly. 
                Retry and follow these exact instructions:
                
                <instructions>
                Respond in raw JSON only 
                </instructions>

                <DO_NOT_INCLUDE>
                1. Markdown
                2. Code fences
                3. Explaination 
                </DO_NOT_INCLUDE>
"""

image_input = client.messages.create(
    model = model,
    max_tokens = tokens,
    messages = [
        {
            "role": "user", "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": prompt1
                }

            ],
         }
    ]
)

raw_response1 = image_input.content[0].text

t = 0
while t < 3:
    try:
        parsed_response1 = json.loads(raw_response1)
        break
    except json.JSONDecodeError:
        t += 1
        image_input = client.messages.create(
            model = model,
            max_tokens = tokens,
            messages = [
                {
                    "role": "user", "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt1
                        }

                    ],
                },
                {
                    "role": "assistant", "content": image_input.content[0].text
                },
                {
                    "role": "user", "content": error_prompt
                }
            ]
        )
        raw_response1 = image_input.content[0].text

if t == 3:
    print("Error: Failed to get valid JSON after 3 attempts.")
    sys.exit()



prompt2 = f"""
            Your job is to respond with 3 practice problems in md format based on an example problem given by the following dictionary:

            <example_problem>
            {parsed_response1}
            </example_problem>

            Generate the practice problems with the following parameters:
            <practice_problem_parameters>
            1. Generate 3 problems
            2. Each problem should be the same math topic as the example problem
            3. Each problem should be the same grade level as the example problem
            4. Of the 3 practice problems, one should be two levels of difficulty below the example problem, one should be the same difficulty as the example problem and one should be two levels of difficulty above the example problem.
            </practice_problem_parameters>

            Adhere to the following instructions when generating your response: 
            <response_instructions>
            1. Your response should be in md format
            2. Your response should be formatted to be easily readable
            </response_instructions>
"""

practice_problems = client.messages.create(
    model=model,
    max_tokens=tokens,
    messages=[
        {"role": "user", "content": prompt2}
    ]
)

print(practice_problems.content[0].text)

with open("practice_problems.md", "w", encoding="utf-8") as f:
    f.write(practice_problems.content[0].text)