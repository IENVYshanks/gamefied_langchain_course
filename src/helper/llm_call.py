from functools import lru_cache

import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

model_name = "Qwen2.5:0.5b"
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

MODEL_NAME = "llama3.2"

# Global LLM instance
llm: ChatOllama = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm

    # ── STARTUP ──
    print(f"Initializing LangChain Ollama model: {MODEL_NAME}")
    try:
        llm = ChatOllama(
            model=MODEL_NAME,
            temperature=0.7,
            base_url="http://localhost:11434",  # default Ollama URL
        )

        # Warm-up call to load model into memory
        await asyncio.to_thread(
            llm.invoke,
            [HumanMessage(content="hi")]
        )
        print(f"Model '{MODEL_NAME}' is ready.")
        app.state.model_ready = True

    except Exception as e:
        print(f"Failed to initialize model: {e}")
        app.state.model_ready = False

    yield  # server runs here

    # ── SHUTDOWN ──
    print("Shutting down.")


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "model_ready": app.state.model_ready,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not app.state.model_ready:
        raise HTTPException(status_code=503, detail="Model not ready")

    try:
        messages = [
            SystemMessage(content=req.system_prompt),
            HumanMessage(content=req.message),
        ]

        result = await asyncio.to_thread(llm.invoke, messages)
        return ChatResponse(response=result.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@lru_cache(maxsize=1)
def get_chat_model() -> ChatOllama:
    return ChatOllama(model=model_name)


def ensure_llm_ready(timeout: float = 10.0) -> None:
    response = requests.get("http://localhost:11434/api/tags", timeout=timeout)
    response.raise_for_status()
    get_chat_model().invoke("Reply with a single word: ready.")

def user_query(query):  
    agent = create_agent(
        model=get_chat_model(),
        system_prompt="You are a concise assistant. Use tools when they help answer the user's question. Answer in a single sentence when possible. If you don't know the answer, say you don't know.",
    )
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        return getattr(last_message, "content", str(last_message))

    return ""



@tool()
def current_time() -> str:
    """Get the current time."""
    import datetime
    return datetime.datetime.now().isoformat()

def agent_call(query):
    agent = create_agent(
        model=get_chat_model(),
        tools=[current_time],
        system_prompt="You are a concise assistant. Use tools when they help answer the user's question.",
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        return getattr(last_message, "content", str(last_message))

    return ""