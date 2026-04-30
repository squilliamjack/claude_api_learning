"""
This script takes example_math_problem.png image file, encodes it and shares it with Claude. 
It then asked claude to analyze the image and solve the problem and then print the response as plain text.
"""

import anthropic
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import base64

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    with open("example_math_problem.png", "rb") as f:
       image = f.read()
       image_data = base64.b64encode(image).decode("utf-8")
except FileNotFoundError:
    print("Image not found.")

model = "claude-sonnet-4-6"
tokens = 1024
prompt_v1 = "Identify the math topic in the given image. Extract the problem(s) present in the image. Assess the approximate grade level of the extracted problem(s)."
prompt_v2 = "Identify the math topic in the given image. Extract the problem(s) present in the image. Assess the approximate grade level of the extracted problem(s). " \
            "Ignore visual appearance when formulating your answer. Take all given information and use your understanding of math properties and principles to formulate your answer"
prompt_v3 = """
            Your job is to identify the math problem in the given image and solve.

            Follow these steps exactly:
            <steps>
            1. Extract the math problem
            2. Identify the math topic
            3. List the given information from the extracted problem
            4. Identify concepts/properties/formulas that relate to the problem
            5. Use those concepts/properties/formulas to set up the solution process
            6. Double check the setup concept and the specific numerical values entered against the math properties related to the topic
            7. Solve for the answer requested
            </steps>

            adhere to the following additional instructions:
            <additional_instructions>
            1. Ignore visual appearance when formulating your answer. 
            2. Take all given information and use your understanding of math properties and principles to formulate your answer
            </additional_instructions>
"""

image_assessment = client.messages.create(
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
                    "text": prompt_v3
                }

            ]
        }
    ]
)

print(image_assessment.content[0].text)