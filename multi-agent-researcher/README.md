# multi-agent-researcher
Preconfigured Python Project that will boost your productivity and improve your workflow

## Technology Stack & Dependencies

- Python 3
- virtualenv (.venv)
- pip (Python package installer)

## Getting Started

### 1. Clone/Download the Repository and setup 2 Env variables OPENAI_API_KEY= and TAVILY_API_KEY=

### 2. Create and activate the virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Run only the AI Agent itself
```bash
python main.py
```

### 5. Run the web app to use the AI Agent
```bash
streamlit run app.py 
```