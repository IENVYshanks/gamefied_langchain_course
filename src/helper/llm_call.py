from src.models.chat import UserQuery
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

model_name = "Qwen2.5:0.5b"
def user_query(query):  
    agent = create_agent(
        model=ChatOllama(model=model_name),
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
        model=ChatOllama(model=model_name),
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