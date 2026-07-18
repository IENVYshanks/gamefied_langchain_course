import streamlit as st
from ziko_st_toc import table_of_contents
from ui_style import apply_style
from auth_utils import require_login
from quiz import render_module_quiz


apply_style('Module 2 - Agents and Tools')
require_login()


st.title('Module 2 - Agents and Tools')
with st.sidebar:
   table_of_contents()

st.header('Agents')
st.write('An agent is a model calling tools in a loop until a given task is complete.')
try:
    st.image("frontend/files/core_agent_loop.svg")
except Exception as e:
    print("image not found")
st.write('A harness is everything around that loop: the model, its prompt, its tools, and any middleware that shapes its behavior.')
st.write(':blue[create_agent] is a highly configurable harness. At its simplest, you can create one with:')
st.code(
    '''
from langchain.agents import create_agent

agent = create_agent(model="ollama:devstral-2", tools=tools)

''',language='python'
)

st.subheader('Model')
st.write(
    'Pass a model identifier string ("provider:model") or an initialized model '
    'instance to select the model for your agent. See Models for parameters, '
    'provider setup, and dynamic model selection.'
)
st.markdown('''
:blue[Google]
:blue[OpenAI]
:blue[Anthropic]
:blue[OpenRouter]
:blue[Fireworks]
:blue[Baseten]
:blue[Ollama]
''')
st.code(
    '''
from langchain.agents import create_agent

agent = create_agent(model="ollama:devstral-2", tools=tools)
''',
    language='python',
)

st.subheader('Tools')
st.write(
    'To provide the agent with tools, pass any Python callable, LangChain tool, '
    'or tool dict. See Tools for tool definition, context access, and dynamic '
    'tool selection.'
)
st.markdown('''
:blue[Google]
:blue[OpenAI]
:blue[Anthropic]
:blue[OpenRouter]
:blue[Fireworks]
:blue[Baseten]
:blue[Ollama]
''')
st.code(
    '''
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


agent = create_agent(model="ollama:devstral-2", tools=[search])
''',
    language='python',
)

st.subheader('System prompt')
st.write(
    'Shape how the agent approaches tasks. The system prompt parameter accepts '
    'a string or SystemMessage. For dynamic prompts at runtime, use middleware.'
)
st.markdown('''
:blue[Google]
:blue[OpenAI]
:blue[Anthropic]
:blue[OpenRouter]
:blue[Fireworks]
:blue[Baseten]
:blue[Ollama]
''')
st.code(
    '''
agent = create_agent(
    model="ollama:devstral-2",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
''',
    language='python',
)

st.subheader('Structured output')
st.write(
    'Return a validated schema from the agent using response_format=. See '
    'Structured output for strategies and examples.'
)
st.markdown('''
:blue[Google]
:blue[OpenAI]
:blue[Anthropic]
:blue[OpenRouter]
:blue[Fireworks]
:blue[Baseten]
:blue[Ollama]
''')
st.code(
    '''
from pydantic import BaseModel
from langchain.agents import create_agent


class Answer(BaseModel):
    summary: str
    confidence: float


agent = create_agent(model="ollama:devstral-2", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
''',
    language='python',
)
st.header('Tools')
st.write(
    'Tools extend what agents can do. They let an agent fetch data, call APIs, '
    'query databases, execute code, or take actions outside the model. In '
    'LangChain, a tool is a callable with a clear input schema, output, name, '
    'and description so the model can decide when and how to use it.'
)

st.subheader('Create tools')
st.write(
    'The easiest way to create a tool is with the @tool decorator. Type hints '
    'define the input schema, and the docstring tells the model what the tool '
    'is for.'
)
st.code(
    '''
from langchain.tools import tool


@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search records that match a query."""
    return f"Found {limit} results for: {query}"
''',
    language='python',
)

st.markdown('''
- Use clear, concise docstrings.
- Prefer `snake_case` tool names.
- Keep tool names alphanumeric with underscores or hyphens for provider compatibility.
- Avoid vague tools. A tool should do one understandable job.
''')

st.subheader('Customize tool properties')
st.write('You can override the default function name and description.')
st.code(
    '''
from langchain.tools import tool


@tool("web_search")
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"


@tool(
    "calculator",
    description="Evaluate arithmetic expressions. Use this for math questions.",
)
def calc(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))
''',
    language='python',
)

st.subheader('Advanced schema definition')
st.write(
    'For more complex inputs, define an args schema with Pydantic. Field '
    'descriptions help the model provide the right arguments.'
)
st.code(
    '''
from typing import Literal
from pydantic import BaseModel, Field
from langchain.tools import tool


class WeatherInput(BaseModel):
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(default="celsius")
    include_forecast: bool = Field(default=False)


@tool(args_schema=WeatherInput)
def get_weather(
    location: str,
    units: str = "celsius",
    include_forecast: bool = False,
) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees"
    if include_forecast:
        result += "\\nForecast: sunny for the next 5 days"
    return result
''',
    language='python',
)

st.warning(
    'Reserved argument names: do not use config or runtime as normal tool '
    'arguments. Use ToolRuntime when the tool needs runtime information.'
)

st.subheader('Access context with ToolRuntime')
st.write(
    'Tools become more useful when they can read conversation state, per-run '
    'context, long-term memory, streaming callbacks, and execution metadata. '
    'Add a ToolRuntime parameter to access those values. LangChain injects it '
    'automatically, so the model does not see it as a tool input.'
)

st.markdown('''
- `runtime.state` reads short-term conversation state.
- `runtime.context` reads immutable per-run configuration such as user ID.
- `runtime.store` reads and writes long-term memory.
- `runtime.stream_writer` emits progress updates during long-running tools.
- `runtime.execution_info` exposes IDs and retry information.
- `runtime.server_info` is available when running on LangGraph Server.
''')

st.code(
    '''
from langchain.messages import HumanMessage
from langchain.tools import ToolRuntime, tool


@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Return the most recent user message."""
    messages = runtime.state["messages"]

    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content

    return "No user message found."
''',
    language='python',
)

st.subheader('Update state from a tool')
st.write(
    'Return a Command when a tool needs to mutate agent state. Include a '
    'ToolMessage when the model should see the result of the update.'
)
st.code(
    '''
from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


class CustomState(AgentState):
    user_name: str


@tool
def set_user_name(
    new_name: str,
    runtime: ToolRuntime[None, CustomState],
) -> Command:
    """Set the user's name in conversation state."""
    return Command(
        update={
            "user_name": new_name,
            "messages": [
                ToolMessage(
                    content=f"User name set to {new_name}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
''',
    language='python',
)

st.subheader('Pass runtime context')
st.write(
    'Use context for values that should be available during a run but should '
    'not be changed by the tool, such as user IDs, roles, or session settings.'
)
st.code(
    '''
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool


USER_DATABASE = {
    "user123": {"name": "Alice", "account_type": "Premium", "balance": 5000},
    "user456": {"name": "Bob", "account_type": "Standard", "balance": 1200},
}


@dataclass
class UserContext:
    user_id: str


@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get account information for the current user."""
    user = USER_DATABASE.get(runtime.context.user_id)
    if user is None:
        return "User not found."

    return (
        f"Account holder: {user['name']}\\n"
        f"Type: {user['account_type']}\\n"
        f"Balance: {user['balance']}"
    )


agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_account_info],
    context_schema=UserContext,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my balance?"}]},
    context=UserContext(user_id="user123"),
)
''',
    language='python',
)

st.subheader('Long-term memory')
st.write(
    'A store lets tools persist information across conversations. State is '
    'short-term; store is long-term.'
)
st.code(
    '''
from typing import Any
from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.store.memory import InMemoryStore


@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up saved user information."""
    item = runtime.store.get(("users",), user_id)
    return str(item.value) if item else "Unknown user."


@tool
def save_user_info(
    user_id: str,
    user_info: dict[str, Any],
    runtime: ToolRuntime,
) -> str:
    """Save user information."""
    runtime.store.put(("users",), user_id, user_info)
    return "Saved user information."


store = InMemoryStore()
agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_user_info, save_user_info],
    store=store,
)
''',
    language='python',
)

st.subheader('Stream progress from tools')
st.write(
    'For long-running tools, use stream_writer to send progress updates while '
    'the tool runs.'
)
st.code(
    '''
from langchain.tools import ToolRuntime, tool


@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a city."""
    writer = runtime.stream_writer
    writer(f"Looking up weather for {city}")
    writer(f"Finished weather lookup for {city}")
    return f"It is sunny in {city}."
''',
    language='python',
)

st.subheader('Tool return values')
st.write('A tool can return different kinds of values depending on what it needs to do.')
st.markdown('''
- Return a `str` for simple human-readable output.
- Return a `dict` or object when the model should inspect structured fields.
- Return a `Command` when the tool should update graph or agent state.
- Use `return_direct=True` when the tool output is already the final answer.
''')

st.code(
    '''
from langchain.tools import tool


@tool
def get_weather_text(city: str) -> str:
    """Get weather as plain text."""
    return f"It is currently sunny in {city}."


@tool
def get_weather_data(city: str) -> dict:
    """Get weather as structured data."""
    return {
        "city": city,
        "temperature_c": 22,
        "conditions": "sunny",
    }


@tool(return_direct=True)
def fetch_order_status(order_id: str) -> str:
    """Fetch the current status of an order."""
    return f"Order {order_id} is shipped and will arrive in 2 days."
''',
    language='python',
)

st.subheader('Error handling')
st.write(
    'Tool errors can be handled with middleware. This lets you convert Python '
    'exceptions into ToolMessages that the model can recover from.'
)
st.code(
    '''
from collections.abc import Callable
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    """Convert tool exceptions into model-readable messages."""
    try:
        return handler(request)
    except Exception as error:
        return ToolMessage(
            content=f"Tool error: check the input and try again. ({error})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model="ollama:devstral-2",
    tools=[],
    middleware=[handle_tool_errors],
)
''',
    language='python',
)

st.subheader('Dynamic tool selection')
st.write(
    'Dynamic tool selection changes the tools available to the model at '
    'runtime. This is useful for permissions, authentication, feature flags, '
    'or conversation stages.'
)
st.code(
    '''
from collections.abc import Callable
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call


@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Filter tools using conversation state."""
    is_authenticated = request.state.get("authenticated", False)

    if not is_authenticated:
        tools = [tool for tool in request.tools if tool.name.startswith("public_")]
        request = request.override(tools=tools)

    return handler(request)


agent = create_agent(
    model="ollama:devstral-2",
    tools=[public_search, private_search],
    middleware=[state_based_tools],
)
''',
    language='python',
)

st.subheader('Runtime tool registration')
st.write(
    'When tools are discovered at runtime, middleware can add the tool before '
    'the model call and route execution when the model calls it.'
)
st.code(
    '''
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ToolCallRequest
from langchain.tools import tool


@tool
def calculate_tip(bill_amount: float, tip_percentage: float = 20.0) -> str:
    """Calculate a tip and total bill amount."""
    tip = bill_amount * (tip_percentage / 100)
    return f"Tip: {tip:.2f}, Total: {bill_amount + tip:.2f}"


class DynamicToolMiddleware(AgentMiddleware):
    def wrap_model_call(self, request: ModelRequest, handler):
        updated = request.override(tools=[*request.tools, calculate_tip])
        return handler(updated)

    def wrap_tool_call(self, request: ToolCallRequest, handler):
        if request.tool_call["name"] == "calculate_tip":
            return handler(request.override(tool=calculate_tip))
        return handler(request)


agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_weather],
    middleware=[DynamicToolMiddleware()],
)
''',
    language='python',
)

st.subheader('Headless tools')
st.write(
    'Headless tools are schema-only tools. The model can call them, but the '
    'actual implementation runs somewhere else, such as a browser, another '
    'service, or a human review step.'
)
st.markdown('''
Use headless tools when the action depends on a client-only environment:

- Browser APIs such as geolocation, clipboard, file pickers, canvas, or IndexedDB.
- Privacy-sensitive local data that should stay on the device.
- UI actions where the frontend should perform the effect.
- Small, typed actions that are safer than asking the browser to run arbitrary code.
''')

st.subheader('Prebuilt and server-side tools')
st.write(
    'LangChain also provides prebuilt tools and toolkits for common jobs such '
    'as web search, code execution, and database access. Some model providers '
    'also offer server-side tools, where the provider runs built-in capabilities '
    'like search or code interpreters without you hosting the implementation.'
)

st.info(
    'Key idea: define tools with precise schemas and descriptions, expose only '
    'the tools needed for the current task, and use ToolRuntime when a tool '
    'needs state, context, memory, streaming, or execution metadata.'
)

render_module_quiz("module_2")
