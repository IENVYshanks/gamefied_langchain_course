import streamlit as st

st.set_page_config(layout="wide")

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