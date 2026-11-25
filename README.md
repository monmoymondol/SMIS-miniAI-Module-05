# SMIS miniAI — AI Productivity Assistant

SMIS miniAI is a Streamlit-based AI productivity application
developed as the Module 05 submission for AI Tools & Mini Project.

It integrates Google's Gemini API and demonstrates how generative
AI can help with programming, research, writing, and productivity.

## Features

- General AI assistant
- Coding assistant
- Research assistant
- Productivity assistant
- Content writing assistant
- Configurable Gemini model
- Adjustable creativity and output length
- Conversation history during the session
- Markdown conversation export
- Light, dark, and default appearance options
- Secure API key configuration

## Technology Stack

- Python
- Streamlit
- Google Gen AI SDK
- Gemini API
- python-dotenv

## Installation

### 1. Clone the repository

git clone https://github.com/monmoymondol/SMIS-miniAI-Module-05.git

cd SMIS-miniAI-Module-05

### 2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure the API key

Copy `.env.example` to `.env`.

Windows:

copy .env.example .env

Linux / macOS:

cp .env.example .env

Open `.env` and replace the placeholder with your Gemini API key.

You may also enter the key in the application sidebar for the
current session.

Never commit `.env` or your API key to GitHub.

### 5. Run the application

streamlit run app.py

The application will open in your browser.

## How to Use

1. Select an assistant mode.
2. Select an available Gemini model.
3. Enter your prompt.
4. Review the generated response.
5. Continue the conversation or export it as Markdown.

## Project Structure

```
SMIS-miniAI-Module-05/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
└── docs/
    ├── MODULE05_LEARNING_NOTES.md
    ├── AI_TOOLS_COMPARISON.md
    └── VIVA_QUESTIONS.md
```
## Learning Outcomes

Through this project, I practiced:

- Using an AI API from Python.
- Designing a Streamlit user interface.
- Creating role-based prompt instructions.
- Managing conversation context.
- Handling API errors and configuration.
- Protecting API credentials.
- Preparing a project for GitHub.

## Limitations

- Requires internet access and a valid Gemini API key.
- Model availability and usage limits depend on the API account.
- Chat history is stored in the active Streamlit session.
- Responses may contain inaccuracies and need verification.
- This educational prototype does not provide authentication
  or persistent multi-user conversation storage.

## Deployment

The app can be deployed through Streamlit Community Cloud.
Configure `GEMINI_API_KEY` in the deployment Secrets settings.

## Academic Submission

Module: 05 — AI Tools & Mini Project  
Project: SMIS miniAI — AI Productivity Assistant  
Student: Sagor Mondol  
Department: Computer Science and Engineering  
Institution: Canadian University of Bangladesh
