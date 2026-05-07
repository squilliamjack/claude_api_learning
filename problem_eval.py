import anthropic
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

model = "claude-sonnet-4-6"
tokens = 1024

topic = "Triangle Congruence"
grade_level = "8th-10th Grade Geometry"
difficulty = "4"

problems_md = """
# Triangle Congruence Practice Problems
---
## Problem 1 — Difficulty: 2/10 (Easier)
**Given:** △ABC ≅ △DEF
The following side lengths and angle measures are provided:
- Side AB = 12
- Side BC = 15
- Side CA = 9
- ∠A = 40°
- ∠B = 75°
**Find:** The values of DE, EF, FD, ∠D, and ∠E.
> *Hint: Corresponding parts of congruent triangles are congruent (CPCTC).*
---
## Problem 2 — Difficulty: 4/10 (Same)
**Given:** △MNP ≅ △QRS
The following measurements are provided:
- Side MN = 5x + 7
- Side MP = 3y + 2
- Side QR = 47
- Side RS = 38
- Side QS = 62
**Find:** The values of x and y.
> *Hint: Match corresponding sides using the order of vertices in the congruence statement, then set up and solve equations.*
---
## Problem 3 — Difficulty: 6/10 (Harder)
**Given:** △ABD ≅ △CBE, where E is a point on AD and B is a point on EC.
The following measurements are provided:
- Side AB = 6x + 5
- Side BD = 4x + 2y
- Side AD = 10x - 1
- Side CB = 8x - 7
- Side BE = 3x + y + 4
- Side CE = 12x - 9
**Find:** The values of x and y, then calculate the **perimeter** of △ABD.
> *Hint: First use corresponding sides to solve for x, then substitute back to find y. Don't forget to calculate all three side lengths for the perimeter.*
---
"""

problems_raw = problems_md.split("## Problem")
problems = problems_raw[1:]

def load_prompt(use_case, version):
    with open("prompt_library.json", "r") as f:
        library = json.load(f)
    for entry in library:
        if entry["use_case"] == use_case:
            return entry.get(version)
    return None

def grade_problem(problem, topic, grade_level, difficulty):
    prompt = load_prompt("practice_problem_grader", "v1")
    prompt = prompt.replace("{practice_problem}", problem)
    prompt = prompt.replace("{topic}", topic)
    prompt = prompt.replace("{grade_level}", grade_level)
    prompt = prompt.replace("{difficulty}", difficulty)
    
    message = client.messages.create(
        model=model,
        max_tokens=tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
        
    raw = message.content[0].text
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()
    
    return raw

results = []
for problem in problems:
    raw = grade_problem(problem, topic, grade_level, difficulty)
    results.append(json.loads(raw))
        
print(results)

with open("practice_problem_eval.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nSaved to practice_problem_eval.json")