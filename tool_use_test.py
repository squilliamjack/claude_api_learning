import anthropic
import os
from dotenv import load_dotenv
import json
import sqlite3

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

model = "claude-sonnet-4-6"
tokens = 1024

def get_student_info(student_name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.id, students.name, students.grade, students.subject
        FROM students
        WHERE students.name = ?
    """, (student_name,))
    results = cursor.fetchall()
    conn.close()
    return results

tool_schema = {
    "name": "get_student_info",
    "description": "Connects to and pulls all info from students.db where name matches",
    "input_schema": {
        "type": "object",
        "properties": {
            "student_name": {
                "type": "string",
                "description": "Name of the student for whom students.db info is desired"
            }
        },
        "required": ["student_name"]
    }
}

message = client.messages.create(
    model=model,
    max_tokens=tokens,
    tools=[tool_schema],
    messages=[
        {"role": "user", "content": "Give me the info for student Elisa Gallardo."}
    ]
)

tool_use_block = next(block for block in message.content if block.type == "tool_use")
result = get_student_info(tool_use_block.input['student_name'])

response = client.messages.create(
    model=model,
    max_tokens=tokens,
    tools=[tool_schema],
    messages=[
        {"role": "user", "content": "Give me the info for student Elisa Gallardo."},
        {"role": "assistant", "content": message.content},
        {"role": "user", "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": str(result)
                }
            ]
         }
    ]
)

print(response.content[0].text)