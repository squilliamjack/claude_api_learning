# Claude API Learning

A collection of Python scripts built while learning the Anthropic Claude API.

## Files

- **claude_test.py** - sends basic message to Claude and prints the response from Claude
- **message_structure.py** - explores different message structures, system prompts, temperature control and multi-turn conversations with Claude
- **prompt_chain.py** - 2-step prompt chain which sends basic message to Claude and uses the response to tailor a follow-up response analyzing the first
- **prompt_library.py** - stores reusable prompt templates for 3 different use cases (student feedback email, parent update email and lesson plan generator) 
- **structured_output.py** - 2-step prompt chain again, this time returning a structured JSON as the second response saved to a JSON file
- **sql_claude.py** - sends session history from an SQL student database to Claude to generate a progress summary

## Setup

1. Clone this repository
2. Install dependencies:
pip install anthropic python-dotenv requests
3. Create a `.env` file in the root folder with the following:
ANTHROPIC_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
4. Run any script with:
python script_name.py 

## Skills Demonstrated

## Skills Demonstrated

- Claude API integration from Python (messages, system prompts, temperature,   multi-turn)
- Prompt engineering using the T-C-R-E-I framework with versioned prompt library
- Multi-step prompt chaining where output of one call feeds the next
- Structured JSON output parsing from LLM responses
- SQLite database creation and querying with JOIN operations
- SQL + Python + Claude pipeline: database → Python → LLM → insight
- API key security with dotenv and .gitignore