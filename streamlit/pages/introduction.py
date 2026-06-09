import streamlit as st
import requests
from helper.auth import require_role
import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None
require_role("admin", "user")

st.title("Dashboard")
st.set_page_config(
    page_title="Models",
    page_icon="🤖",
    layout="wide"
)
st.info("""
👋 Welcome to the Models section.

This page explains the AI models, their capabilities, and how they are initialized within the application.
""")

st.header("Models")
st.markdown("This page will provide information about the different models used in the Agentic AI application.")


st.subheader("LLM : Large Language Model")

st.markdown("LLMs are powerful AI tools that can interpret and generate text like humans. They’re versatile enough to write content, translate languages, summarize, and answer questions without needing specialized training for each task. LLMs are trained on vast amounts of text data, learning patterns and structures in language to understand context and generate coherent responses."
" They can be used in various applications, including chatbots, content creation, and data analysis, making them a valuable asset in many industries.")

st.markdown("""
In addition to text generation, many models support:
            
 * :blue[Tool calling] - calling external tools (like databases queries or API calls) and use results in their responses.\n
 * :blue[Structured output] - where the model’s response is constrained to follow a defined format.\n
 * :blue[Multimodality] - process and return data other than text, such as images, audio, and video.
 * :blue[Reasoning] - models perform multi-step reasoning to arrive at a conclusion.""")

st.subheader("Initialization of models")

st.write("The easiest way to get started with a standalone model in LangChain is to use init_chat_model to initialize one from a chat model provider of your choice (examples below):")

st.code("""
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.4")

response = model.invoke("Why do parrots talk?")
        
print(response.content)
 """, language="python")

st.write("response content:")

st.code("""     
Parrots can talk because they have a specialized vocal organ called the syrinx that allows them to mimic sounds accurately.
In the wild, they use vocal mimicry to communicate and bond with their flock.
When kept as pets, they often imitate human speech as a form of social interaction.
""", language="text")

st.subheader("Parameters")

st.markdown("""
A chat model takes parameters that can be used to configure its behavior. The full set of supported parameters varies by model and provider, but standard ones include:
​
* :blue[model] : string\t:red[required]\n
The name or identifier of the specific model you want to use with a provider. You can also specify both the model and its provider in a single argument using the ’:’ format, for example, ‘openai:o1’.
​
* :blue[api_key] : string\n
The key required for authenticating with the model’s provider. This is usually issued when you sign up for access to the model. Often accessed by setting an environment variable.
​
* :blue[temperature] : number\n 
Controls the randomness of the model’s output. A higher number makes responses more creative; lower ones make them more deterministic.
​
* :blue[max_tokens] : number\n
Limits the total number of tokens in the response, effectively controlling how long the output can be.
​
* :blue[timeout] : number\n
The maximum time (in seconds) to wait for a response from the model before canceling the request.
​
* :blue[max_retries] : number default:"6"\n
The maximum number of attempts the system will make to resend a request if it fails due to issues like network timeouts or rate limits. Retries use exponential backoff with jitter. Network errors, rate limits (429), and server errors (5xx) are retried automatically. Client errors such as 401 (unauthorized) or 404 are not retried. For long-running agent tasks on unreliable networks, consider increasing this to 10–15.
""")

st.write("Example of initializing a model with parameters:")
st.code("""
model = init_chat_model(
    "claude-sonnet-4-6",
    # Kwargs passed to the model:
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
    max_retries=6,  # Default; increase for unreliable networks
""", language = "python")

st.markdown("""
A list of messages can be provided to a chat model to represent conversation history.
Each message has a role that models use to indicate who sent the message in the conversation.
            """)

st.code("""
conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")""", language="python")

st.code("""
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")""", language="python")


st.subheader("Model Providers")
st.markdown("""
LangChain supports a wide range of model providers, including:
* :blue[OpenAI] - Access to OpenAI’s GPT models, including the latest versions with advanced capabilities.
* :blue[Anthropic] - Access to Anthropic’s Claude models, known for their safety and reliability.
* :blue[Google] - Access to Google’s PaLM models, which excel in language understanding and generation.
* :blue[Azure] - Access to Microsoft Azure’s OpenAI Service, which provides scalable and secure access to OpenAI models.
* :blue[Hugging Face] - Access to a wide variety of models hosted on Hugging Face, including both open-source and commercial options.
* :blue[Custom Providers] - LangChain also allows you to integrate custom model providers by implementing the necessary interfaces, giving you the flexibility to use any model that suits your needs.
""")
st.subheader("Invocation configuration")
st.markdown("""
When invoking a model, you can pass additional configuration through the config parameter using a RunnableConfig dictionary. This provides run-time control over execution behavior, callbacks, and metadata tracking.
Common configuration options include:""")
st.code("""
response = model.invoke(
    "Tell me a joke",
    config={
        "run_name": "joke_generation",      # Custom name for this run
        "tags": ["humor", "demo"],          # Tags for categorization
        "metadata": {"user_id": "123"},     # Custom metadata
        "callbacks": [my_callback_handler], # Callback handlers
    }
)""", language="python")

st.subheader("LLM in action")

query = st.text_area("Enter your query here:", height=100)

if st.button("Generate Response"):
    response = requests.post("http://localhost:8000/query/", json={"query": query}).json()
    generated_code = response.strip()
    st.write( generated_code)

