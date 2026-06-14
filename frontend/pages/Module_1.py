import streamlit as st
from ziko_st_toc import table_of_contents


st.title('Table Of contents :')

with st.sidebar:
   table_of_contents()


st.header('Models')

st.write("LLMs are powerful AI tools that can interpret and generate text like humans. They’re versatile enough to write content, translate languages, summarize, and answer questions without needing specialized training for each task.")

st.markdown('''
In addition to text generation, many models support:
 * :blue[Tool calling] - calling external tools (like databases queries or API calls) and use results in their responses.
 * :blue[Structured output] - where the model’s response is constrained to follow a defined format.
 * :blue[Multimodality] - process and return data other than text, such as images, audio, and video.
 * :blue[Reasoning] - models perform multi-step reasoning to arrive at a conclusion.''')

st.write("""Models are the reasoning engine of agents. They drive the agent’s decision-making process, determining which tools to call, how to interpret results, and when to provide a final answer.
The quality and capabilities of the model you choose directly impact your agent’s baseline reliability and performance. Different models excel at different tasks - some are better at following complex instructions, others at structured reasoning, and some support larger context windows for handling more information.
LangChain’s standard model interfaces give you access to many different provider integrations, which makes it easy to experiment with and switch between models to find the best fit for your use case.""")

st.subheader("Initialize a model")
st.write("The easiest way to get started with a standalone model in LangChain is to use init_chat_model to initialize one from a chat model provider of your choice (examples below):")

st.code('''
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.5") 
        
        ''',language = "python")

st.code('''
response = model.invoke("Why do parrots talk?")      
        ''',language = "python")
st.subheader("Parameter")
st.markdown('''
:blue[Parameters] : \n
A chat model takes parameters that can be used to configure its behavior. The full set of supported parameters varies by model and provider, but standard ones include:\n
​
:blue[model] :red[string] :red[required] : \n
The name or identifier of the specific model you want to use with a provider. You can also specify both the model and its provider in a single argument using the ’:’ format, for example, ‘openai:o1’.\n
​
:blue[api_key] :red[string] :\n
The key required for authenticating with the model’s provider. This is usually issued when you sign up for access to the model. Often accessed by setting an environment variable.\n
​
:blue[temperature] :red[number] :\n
Controls the randomness of the model’s output. A higher number makes responses more creative; lower ones make them more deterministic.\n
​
:blue[max_tokens] :red[number] :\n
Limits the total number of tokens in the response, effectively controlling how long the output can be.\n
​
:blue[timeout] :red[number] :\n
The maximum time (in seconds) to wait for a response from the model before canceling the request.\n
​
:blue[max_retries] :red[number] :red[default:"6"] :\n
The maximum number of attempts the system will make to resend a request if it fails due to issues like network timeouts or rate limits. Retries use exponential backoff with jitter. Network errors, rate limits (429), and server errors (5xx) are retried automatically. Client errors such as 401 (unauthorized) or 404 are not retried. For long-running agent tasks on unreliable networks, consider increasing this to 10–15. \n     
            
            
            
            ''')

st.header('Prompts')

st.subheader("1. What is a Prompt?")
st.write("""
A prompt is an instruction given to an LLM. LangChain provides tools to create
dynamic, reusable, and structured prompts.
""")

# -----------------------------------------------------

st.subheader("2. PromptTemplate")
st.write("Used for creating prompts with variables.")

st.code('''
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms."
)

prompt = template.format(topic="Cloud Computing")
print(prompt)
''', language="python")

st.write("Benefits:")
st.markdown("""
- Reusable prompts
- Dynamic input injection
- Cleaner code
""")

# -----------------------------------------------------

st.subheader("3. ChatPromptTemplate")
st.write("Designed for chat models such as GPT.")

st.code('''
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful tutor."),
        ("human", "Explain {topic}")
    ]
)

messages = prompt.format_messages(topic="Recursion")
''', language="python")

st.write("Roles:")
st.markdown("""
- **system** → Defines AI behavior
- **human** → User message
- **ai** → Previous AI response
""")

# -----------------------------------------------------

st.subheader("4. System Messages")
st.write("Control model behavior globally.")

st.code('''
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Python expert."),
        ("human", "{question}")
    ]
)
''', language="python")

# -----------------------------------------------------

st.subheader("5. Few-Shot Prompting")
st.write("Provide examples to improve output quality.")

st.code('''
from langchain_core.prompts import FewShotPromptTemplate

examples = [
    {"question": "2+2", "answer": "4"},
    {"question": "3+3", "answer": "6"}
]
''', language="python")

st.write("Useful for:")
st.markdown("""
- Classification
- Formatting
- Consistent responses
""")

# -----------------------------------------------------

st.subheader("6. MessagesPlaceholder")
st.write("Insert chat history dynamically.")

st.code('''
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant."),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ]
)
''', language="python")

st.write("Used with memory and conversations.")

# -----------------------------------------------------

st.subheader("7. Partial Variables")
st.write("Pre-fill constant values.")

st.code('''
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="You are a {role}. Explain {topic}.",
    input_variables=["topic"],
    partial_variables={"role": "teacher"}
)
''', language="python")

# -----------------------------------------------------

st.subheader("8. Prompt Chaining")
st.write("Connect prompts with models.")

st.code('''
chain = prompt | llm

response = chain.invoke(
    {"topic": "Docker"}
)
''', language="python")

st.code('''
Input → Prompt → LLM → Output
''')

# -----------------------------------------------------

st.subheader("9. Structured Output Prompting")
st.write("Force predictable outputs.")

st.code('''
Return JSON:
{
    "title": "",
    "summary": ""
}
''')

st.write("Useful for:")
st.markdown("""
- APIs
- Agents
- Data Extraction
""")

# -----------------------------------------------------

st.subheader("10. Prompt Engineering Best Practices")

st.write("Be Specific")

st.code('''
# Bad
Explain Python.

# Good
Explain Python decorators with examples for beginners.
''')

st.write("Define Output Format")

st.code('''
Return answer in markdown.
''')

st.write("Set Constraints")

st.code('''
Answer in less than 100 words.
''')

st.write("Use System Prompts")

st.code('''
You are a senior cloud architect.
''')

# -----------------------------------------------------

st.subheader("11. Common Prompting Patterns")

st.write("Q&A")

st.code('''
"Answer the following question: {question}"
''')

st.write("Summarization")

st.code('''
"Summarize the following text: {text}"
''')

st.write("Translation")

st.code('''
"Translate {text} to French."
''')

st.write("Code Generation")

st.code('''
"Write a Python function for {task}."
''')

st.write("Information Extraction")

st.code('''
"Extract names, emails, and phone numbers."
''')

# -----------------------------------------------------

st.subheader("12. Prompt Flow in LangChain")

st.code('''
User Input
    ↓
PromptTemplate
    ↓
ChatPromptTemplate
    ↓
LLM
    ↓
Output Parser (Optional)
    ↓
Final Response
''')

# -----------------------------------------------------

st.subheader("13. Important Prompt Classes")

st.code('''
PromptTemplate
ChatPromptTemplate
FewShotPromptTemplate
MessagesPlaceholder
PipelinePromptTemplate
''')

st.write("""
These classes form the foundation of prompt engineering in LangChain
and are heavily used in Chains, Agents, RAG systems, and AI applications.
""")


#---------------------------------------------------

st.header("Chains ")

st.subheader("1. What is a Chain?")
st.write("""
A Chain connects multiple LangChain components together.
Typically: Input → Prompt → LLM → Output.
Chains help automate AI workflows.
""")

# -----------------------------------------------------

st.subheader("2. Basic LCEL Chain")
st.write("The simplest chain using LangChain Expression Language (LCEL).")

st.code('''
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Explain {topic}"
)

llm = ChatOpenAI()

chain = prompt | llm

response = chain.invoke(
    {"topic": "Docker"}
)
''', language="python")

# -----------------------------------------------------

st.subheader("3. Chain Components")
st.write("A chain usually consists of:")

st.code('''
User Input
    ↓
Prompt
    ↓
LLM
    ↓
Output Parser
    ↓
Final Output
''')

# -----------------------------------------------------

st.subheader("4. Sequential Chaining")
st.write("Output from one step becomes input to the next step.")

st.code('''
prompt1 = ChatPromptTemplate.from_template(
    "Generate 5 interview questions about {topic}"
)

prompt2 = ChatPromptTemplate.from_template(
    "Answer these questions:\\n{questions}"
)

chain = (
    prompt1
    | llm
    | {"questions": lambda x: x.content}
    | prompt2
    | llm
)
''', language="python")

# -----------------------------------------------------

st.subheader("5. RunnableSequence")
st.write("Explicit way to build sequential chains.")

st.code('''
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    prompt,
    llm
)

response = chain.invoke(
    {"topic": "AWS"}
)
''', language="python")

# -----------------------------------------------------

st.subheader("6. RunnableLambda")
st.write("Used for custom Python logic inside chains.")

st.code('''
from langchain_core.runnables import RunnableLambda

def uppercase(text):
    return text.upper()

chain = (
    prompt
    | llm
    | RunnableLambda(uppercase)
)
''', language="python")

# -----------------------------------------------------

st.subheader("7. RunnableParallel")
st.write("Execute multiple chains simultaneously.")

st.code('''
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain
)

result = chain.invoke(
    {"text": document}
)
''', language="python")

st.write("Useful for:")
st.markdown("""
- Summarization + Sentiment Analysis
- Translation + Classification
- Multi-Agent Systems
""")

# -----------------------------------------------------

st.subheader("8. Output Parsers")
st.write("Convert model output into structured formats.")

st.code('''
from langchain_core.output_parsers import StrOutputParser

chain = (
    prompt
    | llm
    | StrOutputParser()
)
''', language="python")

# -----------------------------------------------------

st.subheader("9. JSON Output Parsing")
st.write("Extract structured JSON from LLM responses.")

st.code('''
from langchain_core.output_parsers import JsonOutputParser

chain = (
    prompt
    | llm
    | JsonOutputParser()
)
''', language="python")

# -----------------------------------------------------

st.subheader("10. Branching Chains")
st.write("Execute different paths based on conditions.")

st.code('''
from langchain_core.runnables import RunnableBranch

chain = RunnableBranch(
    (
        lambda x: "python" in x.lower(),
        python_chain
    ),
    general_chain
)
''', language="python")

# -----------------------------------------------------

st.subheader("11. Chain with Memory")
st.write("Maintain conversation history.")

st.code('''
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

chain = ConversationChain(
    llm=llm,
    memory=memory
)
''', language="python")

# -----------------------------------------------------

st.subheader("12. Retrieval Chain (RAG)")
st.write("Combine retrieval with generation.")

st.code('''
retrieval_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
)
''', language="python")

st.write("Workflow:")

st.code('''
User Query
      ↓
Retriever
      ↓
Relevant Documents
      ↓
Prompt
      ↓
LLM
      ↓
Answer
''')

# -----------------------------------------------------

st.subheader("13. Agent Chains")
st.write("Chains that can use tools dynamically.")

st.code('''
agent = create_react_agent(
    llm,
    tools,
    prompt
)
''', language="python")

st.write("Useful when the model needs:")
st.markdown("""
- Web Search
- Database Access
- API Calls
- Calculations
""")

# -----------------------------------------------------

st.subheader("14. Streaming Responses")
st.write("Receive tokens as they are generated.")

st.code('''
for chunk in chain.stream(
    {"topic": "Kubernetes"}
):
    print(chunk)
''', language="python")

# -----------------------------------------------------

st.subheader("15. Batch Processing")
st.write("Run multiple inputs efficiently.")

st.code('''
responses = chain.batch(
    [
        {"topic": "AWS"},
        {"topic": "Docker"},
        {"topic": "Kubernetes"}
    ]
)
''', language="python")

# -----------------------------------------------------

st.subheader("16. Async Chains")
st.write("Execute chains asynchronously.")

st.code('''
response = await chain.ainvoke(
    {"topic": "Cloud Security"}
)
''', language="python")

# -----------------------------------------------------

st.subheader("17. Chain Best Practices")

st.markdown("""
- Keep prompts modular.
- Use output parsers whenever possible.
- Prefer LCEL (`|`) syntax.
- Use RunnableParallel for independent tasks.
- Cache expensive operations.
- Stream long responses.
- Use retrievers instead of large prompts.
""")

# -----------------------------------------------------

st.subheader("18. Common Runnable Classes")

st.code('''
RunnableSequence
RunnableParallel
RunnableLambda
RunnableBranch
RunnablePassthrough
RunnableAssign
''', language="python")

# -----------------------------------------------------

st.subheader("19. Chain Flow")

st.code('''
User Input
      ↓
PromptTemplate
      ↓
LLM
      ↓
Output Parser
      ↓
Chain Logic
      ↓
Final Response
''')

st.write("""
Chains are the core building blocks of LangChain applications and are used in
chatbots, RAG systems, agents, workflows, automation pipelines, and multi-agent architectures.
""")
