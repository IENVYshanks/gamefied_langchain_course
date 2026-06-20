import os
from typing import Any, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel


DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "ollama:Qwen2.5:0.5b")

app = FastAPI(
    title="Gamified LangChain Demo API",
    description="Interactive LangChain examples using Ollama as the model provider.",
    version="1.0.0",
)


class AgentRequest(BaseModel):
    question: str = Field(min_length=1)
    model: str = DEFAULT_MODEL


class ChainRequest(BaseModel):
    text: str = Field(min_length=1)
    model: str = DEFAULT_MODEL


class BranchRequest(BaseModel):
    task_type: Literal["summary", "keywords", "explain"]
    text: str = Field(min_length=1)
    model: str = DEFAULT_MODEL


def get_model(model_name: str):
    model_value = (model_name or DEFAULT_MODEL).strip()
    normalized_model = (
        model_value if ":" in model_value else f"ollama:{model_value}"
    )
    return init_chat_model(normalized_model, temperature=0)


def message_to_dict(message: Any) -> dict[str, Any]:
    return {
        "type": getattr(message, "type", message.__class__.__name__),
        "content": getattr(message, "content", ""),
        "tool_calls": getattr(message, "tool_calls", None),
        "name": getattr(message, "name", None),
    }


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as '12 * (4 + 3)'."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed):
        return "Only numbers and arithmetic operators are allowed."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as error:
        return f"Could not calculate: {error}"


@tool
def word_count(text: str) -> str:
    """Count words and characters in a text."""
    words = len(text.split())
    chars = len(text)
    return f"Words: {words}, characters: {chars}"


@tool
def reverse_text(text: str) -> str:
    """Reverse a piece of text."""
    return text[::-1]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "provider": "ollama", "default_model": DEFAULT_MODEL}


@app.post("/agent/tool-call")
def run_tool_calling_agent(payload: AgentRequest) -> dict[str, Any]:
    """Run an agent that can decide when to call simple tools."""
    model = get_model(payload.model)
    agent = create_agent(
        model=model,
        tools=[calculator, word_count, reverse_text],
        system_prompt=(
            "You are a concise assistant. Use tools when they help. "
            "For math, always use calculator. For counting words, use word_count."
        ),
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": payload.question}]}
    )
    messages = [message_to_dict(message) for message in result["messages"]]
    return {
        "answer": result["messages"][-1].content,
        "messages": messages,
    }


@app.post("/chains/sequential")
def run_sequential_chain(payload: ChainRequest) -> dict[str, Any]:
    """Run a prompt -> model -> parser chain."""
    model = get_model(payload.model)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You rewrite technical text for beginners. Keep it short and clear.",
            ),
            ("human", "Rewrite this in simple language:\n\n{text}"),
        ]
    )

    chain = prompt | model | StrOutputParser()
    output = chain.invoke({"text": payload.text})
    return {"style": "sequential", "output": output}


@app.post("/chains/parallel")
def run_parallel_chain(payload: ChainRequest) -> dict[str, Any]:
    """Run multiple chains on the same input and return all outputs."""
    model = get_model(payload.model)
    parser = StrOutputParser()

    summary_chain = (
        ChatPromptTemplate.from_template("Summarize in 2 bullet points:\n\n{text}")
        | model
        | parser
    )
    keywords_chain = (
        ChatPromptTemplate.from_template("Extract 5 keywords from:\n\n{text}")
        | model
        | parser
    )
    question_chain = (
        ChatPromptTemplate.from_template("Write one quiz question about:\n\n{text}")
        | model
        | parser
    )

    chain = RunnableParallel(
        summary=summary_chain,
        keywords=keywords_chain,
        quiz_question=question_chain,
    )
    output = chain.invoke({"text": payload.text})
    return {"style": "parallel", "output": output}


@app.post("/chains/branch")
def run_branch_chain(payload: BranchRequest) -> dict[str, Any]:
    """Route input to a different chain based on task_type."""
    model = get_model(payload.model)
    parser = StrOutputParser()

    summary_chain = (
        ChatPromptTemplate.from_template("Summarize this in 3 sentences:\n\n{text}")
        | model
        | parser
    )
    keywords_chain = (
        ChatPromptTemplate.from_template("Return important keywords as a comma list:\n\n{text}")
        | model
        | parser
    )
    explain_chain = (
        ChatPromptTemplate.from_template("Explain this concept for a beginner:\n\n{text}")
        | model
        | parser
    )

    chain = RunnableBranch(
        (
            lambda x: x["task_type"] == "summary",
            summary_chain,
        ),
        (
            lambda x: x["task_type"] == "keywords",
            keywords_chain,
        ),
        explain_chain,
    )
    output = chain.invoke({"task_type": payload.task_type, "text": payload.text})
    return {"style": "branch", "selected": payload.task_type, "output": output}


@app.post("/chains/custom")
def run_custom_chain(payload: ChainRequest) -> dict[str, Any]:
    """Mix Python logic with LCEL using RunnableLambda."""
    model = get_model(payload.model)

    def normalize_input(data: dict[str, str]) -> dict[str, str]:
        return {"text": data["text"].strip()}

    chain = (
        RunnableLambda(normalize_input)
        | ChatPromptTemplate.from_template(
            "Create a title and one-sentence learning objective for:\n\n{text}"
        )
        | model
        | StrOutputParser()
    )

    output = chain.invoke({"text": payload.text})
    return {"style": "custom RunnableLambda", "output": output}
