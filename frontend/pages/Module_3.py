import streamlit as st
from ziko_st_toc import table_of_contents
from ui_style import apply_style
from auth_utils import require_login


apply_style('Module 3 - Memory')
require_login()

st.title('Module 3 - Memory')
with st.sidebar:
   table_of_contents()

st.header('Memory in LangChain')
st.write(
    'Memory lets an agent use information from earlier interactions. '
    'LangChain separates memory into two main ideas: short-term memory for a '
    'single conversation thread, and long-term memory for information that '
    'should persist across conversations and sessions.'
)

st.markdown('''
- :blue[Short-term memory] keeps conversation state inside one thread.
- :blue[Long-term memory] stores reusable information across many threads.
- Short-term memory uses a checkpointer.
- Long-term memory uses a store.
''')

st.header('Short-term memory')
st.write(
    'Short-term memory is thread-level persistence. It remembers messages and '
    'state during a single conversation, so an agent can continue from previous '
    'turns in the same thread.'
)

st.subheader('Why short-term memory matters')
st.markdown('''
- It keeps conversation history available to the agent.
- It separates one conversation thread from another.
- It allows a thread to be resumed later.
- It helps tools and prompts access recent state.
- It needs management because long histories can exceed context limits.
''')

st.subheader('Add short-term memory')
st.write(
    'Pass a checkpointer when creating the agent. For learning and local demos, '
    'InMemorySaver is simple. For production, use a database-backed checkpointer.'
)
st.code(
    '''
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


def get_user_info() -> str:
    """Look up information about the current user."""
    return "No user profile on file."


agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

thread_config = {"configurable": {"thread_id": "1"}}

agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    thread_config,
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    thread_config,
)

print(response["messages"][-1].content)
''',
    language='python',
)

st.subheader('Production checkpointer')
st.write(
    'In production, store checkpoints in a database so conversation state '
    'survives process restarts.'
)
st.code(
    '''
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver


DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    agent = create_agent(
        model="ollama:devstral-2",
        tools=[],
        checkpointer=checkpointer,
    )
''',
    language='python',
)

st.subheader('Custom agent state')
st.write(
    'By default, agent state includes the messages list. You can extend '
    'AgentState when your app needs extra short-term fields.'
)
st.code(
    '''
from langchain.agents import AgentState, create_agent
from langgraph.checkpoint.memory import InMemorySaver


class CustomAgentState(AgentState):
    user_id: str
    preferences: dict


agent = create_agent(
    model="ollama:devstral-2",
    tools=[],
    state_schema=CustomAgentState,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",
        "preferences": {"theme": "dark"},
    },
    {"configurable": {"thread_id": "1"}},
)
''',
    language='python',
)

st.subheader('Managing long conversations')
st.write(
    'Conversation history grows over time. If it becomes too large, the model '
    'can become slower, more expensive, or distracted by old messages.'
)
st.markdown('''
- :blue[Trim messages] keeps only the most useful recent messages.
- :blue[Delete messages] removes selected messages from state.
- :blue[Summarize messages] compresses older history into a shorter summary.
- :blue[Custom strategies] filter or rewrite memory based on your app's rules.
''')

st.subheader('Trim messages before the model')
st.write(
    'Use before_model middleware to adjust state before the model call. This '
    'example keeps the first message and the most recent messages.'
)
st.code(
    '''
from typing import Any
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_model
from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.runtime import Runtime


@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep a compact message history."""
    messages = state["messages"]

    if len(messages) <= 4:
        return None

    first_message = messages[0]
    recent_messages = messages[-3:]

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            first_message,
            *recent_messages,
        ]
    }


agent = create_agent(
    model="ollama:devstral-2",
    tools=[],
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)
''',
    language='python',
)

st.subheader('Summarize old messages')
st.write(
    'Summarization keeps important information from earlier conversation turns '
    'without sending the entire history to the model.'
)
st.code(
    '''
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver


agent = create_agent(
    model="ollama:devstral-2",
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model="ollama:devstral-2",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        )
    ],
    checkpointer=InMemorySaver(),
)
''',
    language='python',
)

st.subheader('Read short-term memory in tools')
st.write(
    'Tools can read current state through ToolRuntime. The runtime argument is '
    'injected by LangChain and is hidden from the model-facing tool schema.'
)
st.code(
    '''
from langchain.agents import AgentState, create_agent
from langchain.tools import ToolRuntime, tool


class CustomState(AgentState):
    user_id: str


@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """Look up user info from current agent state."""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"


agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_user_info],
    state_schema=CustomState,
)
''',
    language='python',
)

st.subheader('Write short-term memory from tools')
st.write(
    'Tools can update short-term state by returning a Command. This is useful '
    'when one tool discovers information that later tools or prompts need.'
)
st.code(
    '''
from langchain.agents import AgentState, create_agent
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


class CustomState(AgentState):
    user_name: str


@tool
def set_user_name(name: str, runtime: ToolRuntime) -> Command:
    """Save the user's name in short-term state."""
    return Command(
        update={
            "user_name": name,
            "messages": [
                ToolMessage(
                    content=f"Saved user name: {name}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


agent = create_agent(
    model="ollama:devstral-2",
    tools=[set_user_name],
    state_schema=CustomState,
)
''',
    language='python',
)

st.header('Long-term memory')
st.write(
    'Long-term memory stores information across different conversations and '
    'sessions. It is useful for user profiles, preferences, facts the agent '
    'should remember, and application-level knowledge.'
)

st.subheader('Short-term vs long-term memory')
st.markdown('''
| Memory type | Scope | LangChain mechanism | Example use |
| --- | --- | --- | --- |
| Short-term | One thread | Checkpointer | Remember this conversation |
| Long-term | Many threads | Store | Remember user preferences |
''')

st.subheader('Add long-term memory')
st.write(
    'Create a store and pass it to create_agent. InMemoryStore is good for '
    'development; use a database-backed store for production.'
)
st.code(
    '''
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore


store = InMemoryStore()

agent = create_agent(
    model="ollama:devstral-2",
    tools=[],
    store=store,
)
''',
    language='python',
)

st.subheader('Production store')
st.write('A Postgres store can persist long-term memories outside the Python process.')
st.code(
    '''
from langchain.agents import create_agent
from langgraph.store.postgres import PostgresStore


DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

    agent = create_agent(
        model="ollama:devstral-2",
        tools=[],
        store=store,
    )
''',
    language='python',
)

st.subheader('Memory storage')
st.write(
    'LangGraph stores memories as JSON documents. Each item is saved under a '
    'namespace and key. A namespace works like a folder, while the key works '
    'like the file name.'
)
st.code(
    '''
from langgraph.store.memory import InMemoryStore


store = InMemoryStore()

namespace = ("users", "user_123")
key = "profile"

store.put(
    namespace,
    key,
    {
        "name": "John Smith",
        "language": "English",
        "style": "short and direct",
    },
)

item = store.get(namespace, key)
print(item.value)
''',
    language='python',
)

st.subheader('Search memories')
st.write(
    'Stores can be configured with an index for semantic search. This helps the '
    'agent find relevant memories without knowing the exact key.'
)
st.code(
    '''
from collections.abc import Sequence
from langgraph.store.base import IndexConfig
from langgraph.store.memory import InMemoryStore


def embed(texts: Sequence[str]) -> list[list[float]]:
    """Replace this with a real embedding model."""
    return [[1.0, 2.0] for _ in texts]


store = InMemoryStore(index=IndexConfig(embed=embed, dims=2))
namespace = ("users", "user_123")

store.put(
    namespace,
    "preference",
    {"rule": "User likes short, direct answers."},
)

results = store.search(namespace, query="communication style")
''',
    language='python',
)

st.subheader('Read long-term memory in tools')
st.write(
    'Tools read long-term memory through runtime.store. Use runtime.context to '
    'identify whose memory should be loaded.'
)
st.code(
    '''
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.store.memory import InMemoryStore


@dataclass
class Context:
    user_id: str


store = InMemoryStore()
store.put(("users",), "user_123", {"name": "John Smith", "language": "English"})


@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Look up saved user information."""
    assert runtime.store is not None
    user_info = runtime.store.get(("users",), runtime.context.user_id)
    return str(user_info.value) if user_info else "Unknown user"


agent = create_agent(
    model="ollama:devstral-2",
    tools=[get_user_info],
    store=store,
    context_schema=Context,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Look up user information"}]},
    context=Context(user_id="user_123"),
)
''',
    language='python',
)

st.subheader('Write long-term memory from tools')
st.write(
    'Tools can save user information, preferences, or facts into the store so '
    'future conversations can reuse them.'
)
st.code(
    '''
from dataclasses import dataclass
from typing_extensions import TypedDict
from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.store.memory import InMemoryStore


@dataclass
class Context:
    user_id: str


class UserInfo(TypedDict):
    name: str


store = InMemoryStore()


@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Save user info for future conversations."""
    assert runtime.store is not None
    runtime.store.put(("users",), runtime.context.user_id, dict(user_info))
    return "Successfully saved user info."


agent = create_agent(
    model="ollama:devstral-2",
    tools=[save_user_info],
    store=store,
    context_schema=Context,
)

agent.invoke(
    {"messages": [{"role": "user", "content": "My name is John Smith"}]},
    context=Context(user_id="user_123"),
)
''',
    language='python',
)

st.header('Memory best practices')
st.markdown('''
- Use short-term memory for conversation history and temporary state.
- Use long-term memory for durable user or application knowledge.
- Store only useful information, not every token of every conversation.
- Use namespaces that include user IDs, organization IDs, or app contexts.
- Summarize or trim short-term memory before it becomes too large.
- Use database-backed checkpointers and stores in production.
- Keep private or sensitive memory data protected by your app's permissions.
''')

st.info(
    'Key idea: checkpointers remember a thread; stores remember durable facts. '
    'Most real agents use both.'
)
