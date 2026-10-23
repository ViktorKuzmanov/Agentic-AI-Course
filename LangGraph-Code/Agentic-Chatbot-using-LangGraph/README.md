# Agentic Chatbot

The gemini model is a little slow in the chatbot .najposlednat komanda gledaj a so taa se run kodot

## Technology Stack & Dependencies

- Python 3
- virtualenv (.venv)
- pip (Python package installer)
- LangGraph / LangChain
- OpenAI / Groq / Google GenAI / LiteLLM providers
- Pydantic, Pandas

## Getting Started

### 1. Clone/Download the Repository

### 2. Create and activate the virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```
python -m pip install -r requirements.txt
```
### 3.1 Setup env, check env example
```
OPENAI_API_KEY=
GOOGLE_API_KEY=

TAVILY_API_KEY="your-api-key"
OPENWEATHER_API_KEY="your-api-key"

LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="za kursot Agentic Chatbot"
```


### 4. Run the project
```
streamlit run app_db.py  
```
