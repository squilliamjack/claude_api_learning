import anthropic
import os
from dotenv import load_dotenv
import json
from pypdf import PdfReader

reader = PdfReader("algebra-and-trigonometry-2e_-_WEB.pdf")
raw_text = []
for i in range(140, 154):
    page_text = reader.pages[i].extract_text()
    raw_text.append(page_text)

for i in range(0, 4):
    print(raw_text[i])
    print(len(raw_text[i]))