import streamlit as st
import requests
from helper.auth import require_role

if "role" not in st.session_state:
    st.session_state.role = None
    
require_role("admin", "user")
st.set_page_config(
    page_title="tools",
    page_icon="🛠️",
    layout="wide"
)
st.info("""👋 Welcome to the Tools section.""")

st.title("Tools")

st.write("""
Tools extend what agents can do—letting them fetch real-time data, execute code, query external databases, and take actions in the world.
Under the hood, tools are callable functions with well-defined inputs and outputs that get passed to a chat model. The model decides when to invoke a tool based on the conversation context, and what input arguments to provide.""")

st.header("Create Tools")

st.subheader(" Define a function")
st.markdown("""Tools extend what agents can do—letting them fetch real-time data, execute code, query external databases, and take actions in the world.
Under the hood, tools are callable functions with well-defined inputs and outputs that get passed to a chat model. The model decides when to invoke a tool based on the conversation context, and what input arguments to provide.""")

st.code('''
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
''', language="python")

st.header("Customize tool properties")
st.subheader("Custom tool name")
st.write("By default, the tool name is the same as the function name. You can customize it by passing a name argument to the @tool decorator:")
st.code('''
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search''', language="python")

st.subheader("Custom tool description")
st.write("The tool description is used by the model to understand when and how to use the tool. You can provide a custom description by passing a description argument to the @tool decorator:")
st.code('''
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))''', language="python")

st.subheader('Advanced schema definition')
st.write("Define complex inputs with Pydantic models or JSON schemas:")
st.code('''
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result''',language ="python")


st.header("Tool calling in action")
st.write("When a model calls a tool, it generates a structured message that includes the tool name and input arguments. The agent framework then executes the corresponding function and passes the result back to the model as part of the conversation history.")
st.code('''
@tool()
def current_time() -> str:
    """Get the current time."""
    import datetime
    return datetime.datetime.now().isoformat()


def agent_call():
    agent = create_agent(
    ChatOpenAI(model="ollama:qwen2:0.5b"),
    tools=[ current_time],
)

    result = agent.invoke({
    "messages": [{"role": "user", "content": "What is the time right now and what is the date ? "}]
    
})

    return result['content']''', language="python")
if st.button("Run tool example"):
    repsonse = requests.post("http://localhost:8000/query/agent", json={"query": "What is the time right now and what is the date ? "})
    st.write(repsonse.json())
