import streamlit as st
from ziko_st_toc import table_of_contents
from ui_style import apply_style


apply_style('Module 5 - Agentic AI')

st.title('Module 5 - Agentic AI')
with st.sidebar:
   table_of_contents()

st.header('Module 5 - Agentic AI')
st.write(
    'Agentic AI systems use models, tools, memory, and control flow to solve '
    'tasks over multiple steps. Instead of making one model call and stopping, '
    'an agent can reason, call tools, observe results, update state, and decide '
    'what to do next.'
)

st.markdown('''
- :blue[Single-agent systems] keep one model in charge of the whole task.
- :blue[Multi-agent systems] split work across specialized agents or workflows.
- :blue[LangGraph] gives you lower-level control over state, nodes, edges, and execution.
- :blue[Agentic workflows] mix deterministic code with model-driven decisions.
''')

st.header('Multi-agent systems')
st.write(
    'A multi-agent system coordinates multiple specialized components to solve '
    'a larger workflow. Each agent can have its own prompt, tools, memory, and '
    'domain knowledge.'
)

st.subheader('Why use multiple agents?')
st.markdown('''
- :blue[Context management] - Give each agent only the knowledge it needs.
- :blue[Specialization] - Use different prompts and tools for different jobs.
- :blue[Distributed development] - Let separate teams maintain separate capabilities.
- :blue[Parallelization] - Run independent subtasks at the same time.
- :blue[Control] - Enforce routing, review, approval, or ordering constraints.
''')

st.warning(
    'Not every complex task needs multiple agents. A single agent with a good '
    'prompt, focused tools, and dynamic tool selection is often simpler and cheaper.'
)

st.subheader('Common multi-agent patterns')
st.markdown('''
| Pattern | How it works | Good for |
| --- | --- | --- |
| Subagents | A main agent calls specialized agents as tools | Centralized control and isolated context |
| Handoffs | One agent transfers control to another agent | Conversations that shift between specialists |
| Skills | A single agent loads specialized instructions on demand | Keeping one controller while adding deep context |
| Router | A router classifies the request and sends it to the right agent | Clear categories like billing, support, or technical help |
| Custom workflow | LangGraph nodes and edges define the exact flow | Complex systems that need deterministic control |
''')

st.subheader('Choosing a pattern')
st.write(
    'Choose based on control, latency, context size, and whether agents must run '
    'in parallel or talk directly to the user.'
)
st.markdown('''
- Use :blue[subagents] when each specialist needs isolated context.
- Use :blue[handoffs] when the active specialist should continue the conversation.
- Use :blue[skills] when one agent should stay in charge but load extra knowledge.
- Use a :blue[router] when the first step is classification.
- Use :blue[LangGraph] when you need custom loops, validation, retries, or state transitions.
''')

st.subheader('Subagents as tools')
st.write(
    'In the subagent pattern, the main agent treats other agents like tools. '
    'The main agent decides which specialist to call and combines the results.'
)
st.code(
    '''
from langchain.agents import create_agent
from langchain.tools import tool


research_agent = create_agent(
    model="ollama:devstral-2",
    tools=[web_search],
    system_prompt="You are a research specialist. Find relevant facts.",
)

writing_agent = create_agent(
    model="ollama:devstral-2",
    tools=[],
    system_prompt="You are a writing specialist. Create clear summaries.",
)


@tool
def research_topic(topic: str) -> str:
    """Use the research specialist to gather facts."""
    result = research_agent.invoke(
        {"messages": [{"role": "user", "content": topic}]}
    )
    return result["messages"][-1].content


@tool
def write_summary(notes: str) -> str:
    """Use the writing specialist to turn notes into a summary."""
    result = writing_agent.invoke(
        {"messages": [{"role": "user", "content": notes}]}
    )
    return result["messages"][-1].content


manager = create_agent(
    model="ollama:devstral-2",
    tools=[research_topic, write_summary],
    system_prompt="Break the task into specialist steps, then answer the user.",
)
''',
    language='python',
)

st.subheader('Router pattern')
st.write(
    'A router uses the model or rules to classify the request, then sends the '
    'input to the best specialist.'
)
st.code(
    '''
from typing import Literal
from pydantic import BaseModel, Field


class Route(BaseModel):
    destination: Literal["billing", "technical", "general"] = Field(
        description="The specialist that should handle the request."
    )


router = model.with_structured_output(Route)


def route_request(user_input: str):
    decision = router.invoke(
        f"Route this user request to billing, technical, or general: {user_input}"
    )

    if decision.destination == "billing":
        return billing_agent.invoke({"messages": user_input})
    if decision.destination == "technical":
        return technical_agent.invoke({"messages": user_input})
    return general_agent.invoke({"messages": user_input})
''',
    language='python',
)

st.subheader('Orchestrator-worker pattern')
st.write(
    'An orchestrator breaks a task into subtasks, sends subtasks to workers, '
    'then synthesizes the worker outputs. This is useful when the subtasks are '
    'not known until runtime.'
)
st.code(
    '''
def orchestrator(task: str) -> list[str]:
    """Plan subtasks for workers."""
    return [
        "Research the topic",
        "Find implementation risks",
        "Write a final recommendation",
    ]


def worker(subtask: str) -> str:
    """Complete one assigned subtask."""
    return specialist_agent.invoke({"messages": subtask})["messages"][-1].content


def synthesize(results: list[str]) -> str:
    """Combine worker results into one answer."""
    return "\\n\\n".join(results)


subtasks = orchestrator("Compare RAG and fine-tuning for support bots")
results = [worker(subtask) for subtask in subtasks]
final_answer = synthesize(results)
''',
    language='python',
)

st.header('LangGraph basics')
st.write(
    'LangGraph is a low-level orchestration framework for building stateful, '
    'long-running agents and workflows. It is useful when you need more control '
    'than a prebuilt agent loop gives you.'
)

st.subheader('When to use LangGraph')
st.markdown('''
- You need explicit nodes and edges.
- You need durable execution and resumable state.
- You need human review or approval during execution.
- You need streaming, persistence, time travel, or debugging visibility.
- You need custom routing, retries, validation, or multi-agent coordination.
''')

st.subheader('Core LangGraph concepts')
st.markdown('''
| Concept | Meaning |
| --- | --- |
| State | Shared data that moves through the graph |
| Node | A function that reads state and returns state updates |
| Edge | A connection from one node to another |
| Conditional edge | Routing logic that chooses the next node |
| START | Entry point of the graph |
| END | Exit point of the graph |
| Compile | Turns the graph definition into a runnable app |
''')

st.subheader('Hello world graph')
st.write(
    'A basic graph defines state, adds nodes, connects edges, compiles, and invokes.'
)
st.code(
    '''
from langgraph.graph import StateGraph, MessagesState, START, END


def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}


graph = StateGraph(MessagesState)
graph.add_node("mock_llm", mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)

app = graph.compile()
result = app.invoke({"messages": [{"role": "user", "content": "hi!"}]})
''',
    language='python',
)

st.subheader('Define state')
st.write(
    'State is the memory of the graph during execution. A node receives the '
    'current state and returns only the updates it wants to make.'
)
st.code(
    '''
import operator
from typing_extensions import Annotated, TypedDict
from langchain.messages import AnyMessage


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
''',
    language='python',
)

st.subheader('Build a tool-calling loop')
st.write(
    'A classic agent loop has a model node, a tool node, and routing logic. '
    'The model decides whether to call a tool. If it does, the graph runs the '
    'tool node and loops back to the model. If not, the graph ends.'
)
st.code(
    '''
from typing import Literal
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, ToolMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END


model = init_chat_model("ollama:devstral-2", temperature=0)


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


tools = [add, multiply]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)


def llm_call(state: MessagesState):
    """Ask the model what to do next."""
    response = model_with_tools.invoke(
        [
            SystemMessage(content="You are a helpful math assistant.")
        ]
        + state["messages"]
    )
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


def tool_node(state: MessagesState):
    """Run tools requested by the model."""
    results = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": results}


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Route to tools or finish."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END


builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "llm_call")

agent = builder.compile()
''',
    language='python',
)

st.subheader('Prompt chaining')
st.write(
    'Prompt chaining runs steps in a known order. Each node works on the output '
    'of the previous node.'
)
st.code(
    '''
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class JokeState(TypedDict):
    topic: str
    joke: str
    improved_joke: str


def generate_joke(state: JokeState):
    msg = model.invoke(f"Write a short joke about {state['topic']}")
    return {"joke": msg.content}


def improve_joke(state: JokeState):
    msg = model.invoke(f"Make this joke funnier: {state['joke']}")
    return {"improved_joke": msg.content}


workflow = StateGraph(JokeState)
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_edge(START, "generate_joke")
workflow.add_edge("generate_joke", "improve_joke")
workflow.add_edge("improve_joke", END)

chain = workflow.compile()
result = chain.invoke({"topic": "programming"})
''',
    language='python',
)

st.subheader('Parallelization')
st.write(
    'Parallel graphs start multiple independent nodes from START and combine '
    'their results later. This can reduce latency when subtasks do not depend '
    'on each other.'
)
st.code(
    '''
class ContentState(TypedDict):
    topic: str
    joke: str
    story: str
    poem: str
    combined_output: str


def write_joke(state: ContentState):
    return {"joke": model.invoke(f"Write a joke about {state['topic']}").content}


def write_story(state: ContentState):
    return {"story": model.invoke(f"Write a story about {state['topic']}").content}


def write_poem(state: ContentState):
    return {"poem": model.invoke(f"Write a poem about {state['topic']}").content}


def aggregator(state: ContentState):
    return {
        "combined_output": (
            f"STORY:\\n{state['story']}\\n\\n"
            f"JOKE:\\n{state['joke']}\\n\\n"
            f"POEM:\\n{state['poem']}"
        )
    }


parallel_builder = StateGraph(ContentState)
parallel_builder.add_node("write_joke", write_joke)
parallel_builder.add_node("write_story", write_story)
parallel_builder.add_node("write_poem", write_poem)
parallel_builder.add_node("aggregator", aggregator)
parallel_builder.add_edge(START, "write_joke")
parallel_builder.add_edge(START, "write_story")
parallel_builder.add_edge(START, "write_poem")
parallel_builder.add_edge("write_joke", "aggregator")
parallel_builder.add_edge("write_story", "aggregator")
parallel_builder.add_edge("write_poem", "aggregator")
parallel_builder.add_edge("aggregator", END)

parallel_workflow = parallel_builder.compile()
''',
    language='python',
)

st.subheader('Routing workflow')
st.write(
    'Routing uses a decision node to choose which specialized path should run.'
)
st.code(
    '''
from typing import Literal
from pydantic import BaseModel, Field


class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        description="The next step in the routing process."
    )


router = model.with_structured_output(Route)


class RouteState(TypedDict):
    input: str
    decision: str
    output: str


def route_input(state: RouteState):
    decision = router.invoke(
        f"Route this request to poem, story, or joke: {state['input']}"
    )
    return {"decision": decision.step}


def route_decision(state: RouteState):
    if state["decision"] == "story":
        return "write_story"
    if state["decision"] == "poem":
        return "write_poem"
    return "write_joke"
''',
    language='python',
)

st.subheader('Creating workers with Send')
st.write(
    'For orchestrator-worker systems, LangGraph can dynamically create worker '
    'tasks with Send. Each worker receives its own input, then writes results '
    'back into shared state.'
)
st.code(
    '''
from langgraph.types import Send


def assign_workers(state):
    """Create one worker task for each planned section."""
    return [
        Send("write_section", {"section": section})
        for section in state["sections"]
    ]
''',
    language='python',
)

st.header('Design best practices')
st.markdown('''
- Start with one agent, then split into multiple agents only when specialization helps.
- Keep each agent's tools and context focused.
- Prefer deterministic routing when the categories are obvious.
- Use model-based routing when requests are fuzzy or natural-language-heavy.
- Use parallel workers for independent subtasks.
- Use LangGraph when you need explicit state, loops, retries, or human checkpoints.
- Trace complex systems so you can see which agent ran, which tool was called, and why.
''')

st.info(
    'Key idea: multi-agent design is context engineering. LangGraph gives you '
    'the control surface for deciding what runs, what state is visible, and '
    'how work moves through the system.'
)
