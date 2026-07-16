import json
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

import streamlit as st
from ziko_st_toc import table_of_contents

from ui_style import apply_style
from auth_utils import require_login


apply_style('Try it - Interactive Agent Demo')
require_login()

st.title('Module 6 - Interactive Agent Demo')
with st.sidebar:
   table_of_contents()


def post_json(base_url: str, path: str, payload: dict) -> dict:
    request = Request(
        f"{base_url.rstrip('/')}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(base_url: str, path: str) -> dict:
    request = Request(f"{base_url.rstrip('/')}{path}", method="GET")
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def show_error(error: Exception) -> None:
    if isinstance(error, HTTPError):
        detail = error.read().decode("utf-8")
        st.error(f"Backend error {error.code}: {detail}")
    elif isinstance(error, URLError):
        st.error(
            "Could not reach the FastAPI backend. Start it with: "
            "`python -m uvicorn src.app:app --reload --port 8000`"
        )
    else:
        st.error(f"Request failed: {error}")


st.write(
    'This page connects to a FastAPI backend in the `src` folder. The backend '
    'uses Ollama as the model provider and demonstrates simple tool calling '
    'plus different LangChain chaining styles.'
)

st.header('Backend connection')
col_1, col_2 = st.columns([2, 1])
with col_1:
    backend_url = st.text_input('FastAPI backend URL', value='http://localhost:8000')
with col_2:
    model_name = st.text_input('Ollama model', value='ollama:Qwen2.5:0.5b')

if st.button('Check backend'):
    try:
        health = get_json(backend_url, '/health')
        st.success(f"Backend is ready: {health}")
    except Exception as error:
        show_error(error)

st.info(
    'Before using the examples, make sure Ollama is running and the selected '
    'model is available locally.'
)

st.header('Agent with simple tool calling')
st.write(
    'The agent has three tools: calculator, word_count, and reverse_text. '
    'Ask something that requires one of those tools and inspect the message trace.'
)

agent_question = st.text_area(
    'Agent question',
    value='What is (18 + 7) * 4? Use a tool and explain briefly.',
    height=90,
)

if st.button('Run agent'):
    try:
        result = post_json(
            backend_url,
            '/agent/tool-call',
            {'question': agent_question, 'model': model_name},
        )
        st.subheader('Answer')
        st.write(result['answer'])

        with st.expander('Message trace'):
            for index, message in enumerate(result['messages'], start=1):
                st.markdown(f"**{index}. {message['type']}**")
                if message.get('content'):
                    st.write(message['content'])
                if message.get('tool_calls'):
                    st.json(message['tool_calls'])
    except Exception as error:
        show_error(error)

st.header('Different chaining styles')
st.write(
    'These examples show how the same model can be wired into different chain '
    'patterns: sequential, parallel, branch, and custom Python logic.'
)

chain_text = st.text_area(
    'Input text for chains',
    value=(
        'LangChain helps developers build applications that combine language '
        'models with prompts, tools, retrieval, memory, and structured workflows.'
    ),
    height=120,
)

tab_1, tab_2, tab_3, tab_4 = st.tabs(
    ['Sequential', 'Parallel', 'Branch', 'Custom']
)

with tab_1:
    st.write('Sequential chain: prompt -> model -> string parser.')
    st.code(
        '''
chain = prompt | model | StrOutputParser()
output = chain.invoke({"text": text})
''',
        language='python',
    )
    if st.button('Run sequential chain'):
        try:
            result = post_json(
                backend_url,
                '/chains/sequential',
                {'text': chain_text, 'model': model_name},
            )
            st.write(result['output'])
        except Exception as error:
            show_error(error)

with tab_2:
    st.write(
        'Parallel chain: run summary, keyword extraction, and quiz generation '
        'at the same time.'
    )
    st.code(
        '''
chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    quiz_question=question_chain,
)
''',
        language='python',
    )
    if st.button('Run parallel chain'):
        try:
            result = post_json(
                backend_url,
                '/chains/parallel',
                {'text': chain_text, 'model': model_name},
            )
            output = result['output']
            st.subheader('Summary')
            st.write(output['summary'])
            st.subheader('Keywords')
            st.write(output['keywords'])
            st.subheader('Quiz question')
            st.write(output['quiz_question'])
        except Exception as error:
            show_error(error)

with tab_3:
    st.write('Branch chain: route to a different prompt based on task type.')
    task_type = st.selectbox('Task type', ['summary', 'keywords', 'explain'])
    st.code(
        '''
chain = RunnableBranch(
    (lambda x: x["task_type"] == "summary", summary_chain),
    (lambda x: x["task_type"] == "keywords", keywords_chain),
    explain_chain,
)
''',
        language='python',
    )
    if st.button('Run branch chain'):
        try:
            result = post_json(
                backend_url,
                '/chains/branch',
                {'task_type': task_type, 'text': chain_text, 'model': model_name},
            )
            st.write(result['output'])
        except Exception as error:
            show_error(error)

with tab_4:
    st.write('Custom chain: use RunnableLambda to add Python logic inside LCEL.')
    st.code(
        '''
chain = (
    RunnableLambda(normalize_input)
    | prompt
    | model
    | StrOutputParser()
)
''',
        language='python',
    )
    if st.button('Run custom chain'):
        try:
            result = post_json(
                backend_url,
                '/chains/custom',
                {'text': chain_text, 'model': model_name},
            )
            st.write(result['output'])
        except Exception as error:
            show_error(error)

st.header('Run commands')
st.write('Use these commands from the project root when you want to run the demo manually.')
st.code(
    '''
# Start Ollama separately if it is not already running
ollama serve

# Pull the model once if needed
ollama pull devstral-2

# Start FastAPI backend
python -m uvicorn src.app:app --reload --port 8000

# Start Streamlit frontend
python -m streamlit run frontend/main.py
''',
    language='powershell',
)
