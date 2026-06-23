# Gamified LangChain

A learning and demo project for LangChain, Ollama, and Streamlit.
This repository includes a FastAPI backend with LangChain agents and chains,
and a Streamlit frontend that guides learners through key LangChain concepts.

## What’s included

- `src/app.py` — FastAPI backend demonstrating simple LangChain agents, tool calling, sequential/parallel/branch/custom chains, and Ollama model integration.
- `frontend/main.py` — Streamlit app that presents course-style pages and an interactive demo for the backend.
- `frontend/pages/` — instructional pages covering models, prompts, chains, agents, tools, memory, RAG, and agent workflows.
- `agent_demo.py` — minimal example of a LangChain agent using Ollama.

## Key features

- LangChain agent with tool calling
- FastAPI backend endpoints for agent and chain demos
- Streamlit frontend for interactive learning and experiments
- Ollama model support via `ollama:<model>` identifiers
- Example use of `langchain_core` prompt templates, runnables, and output parsers
- RAG and embeddings examples in the frontend pages

## Prerequisites

- Python 3.11+ recommended
- [Ollama](https://ollama.com/) installed and running locally
- A supported Ollama model available on your machine

## Install

From the project root:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you prefer, create a virtual environment first:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the demo

1. Start the Ollama server (if not already running):

```powershell
ollama serve
```

2. Run the backend API:

```powershell
python -m uvicorn src.app:app --reload --port 8000
```

3. Run the Streamlit frontend:

```powershell
python -m streamlit run frontend/main.py
```

4. Open the Streamlit app in your browser and use the sidebar to explore the modules.

## Recommended workflow

- Start with the Streamlit modules to learn about models, prompts, and chains.
- Use the interactive module to run the FastAPI backend and inspect agent behavior.
- Explore `frontend/pages/Module_4.py` for RAG examples and `Module_5.py` for agentic workflows.

## Notes

- The backend expects an Ollama model identifier such as `ollama:Qwen2.5:0.5b`.
- The frontend `Try_IT` page uses the backend endpoints to show live demo interactions.
- `.gitignore` already excludes common local environment and build artifacts such as `.venv/`, `env/`, `__pycache__/`, `*.pyc`, `.env`, and `.vscode/`.

## Project structure

```
agent_demo.py
src/app.py
frontend/main.py
frontend/pages/
frontend/ui_style.py
LICENSE
README.md
```

## License

This repository includes a `LICENSE` file for license details.
