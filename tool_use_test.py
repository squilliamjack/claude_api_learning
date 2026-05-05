"""
This script is used to request and write info to and from SQL DB using Claude API
"""


import anthropic
import os
from dotenv import load_dotenv
import json
import sqlite3
from datetime import datetime

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

model = "claude-sonnet-4-6"
tokens = 1024

def get_student_info(student_name):
    
    """
    This function takes student_name as an argument and connects to 
    students.db and pulls all info for provided student name
    """
    
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

def log_student_session(student_id, topic, performance):
    
    """
    This function takes student_id, topic, and performance as arguments
    and connects to students.db and adds a new row in sessions based on 
    the provided information
    """
    
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (student_id, date, topic, performance)
        VALUES (?, ?, ?, ?)                           
    """, (student_id, datetime.now().strftime("%Y-%m-%d"), topic, performance))
    conn.commit()
    conn.close()
    
def run_tool(tool_name, tool_input):
    if tool_name == "get_student_info":
        result = get_student_info(tool_input["student_name"])
        return result
    elif tool_name == "log_student_session":
        result = log_student_session(tool_input["student_id"], tool_input["topic"], tool_input["performance"])
        return result
    else:
        print("Invalid tool request.")

tools = [
    {
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
    },
    {
        "name": "log_student_session",
        "description": "Connects to students.db and adds a new row based on input arguments",
        "input_schema": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "integer",
                    "description": "ID that corresponds to student"
                    },
                "topic": {
                    "type": "string",
                    "description": "Topic covered during the session."
                    },
                "performance": {
                    "type": "string",
                    "description": "General assessment of performance during the session."
                    }
            },
            "required": ["student_id", "topic", "performance"]
        }
    }
]
    
# messages = [
#         {"role": "user", "content": "Give me the info for student Elisa Gallardo."}   
# ]

messages = [
    {"role": "user", "content": "Log a session for student ID 2. Topic was Triangle Congruence. Performance was strong understanding of CPCTC but struggled with algebraic setup."}
]
   
def run_conversation(messages):
    message = client.messages.create(
        model=model,
        max_tokens=tokens,
        tools=tools,
        messages=messages
    )
    
    while message.stop_reason == "tool_use":
        tool_use_block = next(block for block in message.content if block.type == "tool_use")
        tool_request = run_tool(tool_use_block.name, tool_use_block.input)
        messages.append({"role": "assistant", "content": message.content})
        messages.append({"role": "user", "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": str(tool_request)
            }
        ]})
        response = client.messages.create(
            model=model,
            max_tokens=tokens,
            tools=tools,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})
        message = response
    return message

final_response = run_conversation(messages)
print(final_response.content[0].text)






