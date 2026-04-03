"""
SQL + Claude integration.
Queries a SQLite student database for session history,
then passes the results to Claude to generate a progress summary.
"""

import anthropic
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_student_sessions(student_name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.name, sessions.date, sessions.topic, sessions.performance
        FROM students
        INNER JOIN sessions ON sessions.student_id = students.id
        WHERE students.name = ?
    """, (student_name,))
    results = cursor.fetchall()
    conn.close()
    return results

student_name = "Elisa Gallardo"
sessions = get_student_sessions(student_name)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="You are a helpful math tutor assistant. Summarize a student's progress based on their session history.",
    messages=[
        {"role": "user", "content": f"Here are the sessions for {student_name}: {sessions}. Please summarize their progress."}
    ]
)

print(message.content[0].text)
