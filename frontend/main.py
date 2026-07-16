import streamlit as st
from ui_style import apply_style, hero, module_card
from auth_utils import restore_session, save_config


def render_login_gate(authenticator, config):
    st.title("Gamified LangChain Learning")
    st.caption("Log in to unlock the course modules.")

    tab_login, tab_register, tab_forgot_pw, tab_forgot_user = st.tabs(
        ["Login", "Register", "Forgot password", "Forgot username"]
    )

    with tab_login:
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)
        auth_status = st.session_state.get("authentication_status")
        if auth_status is False:
            st.error("Username/password is incorrect")
        elif auth_status is None:
            st.info("Enter your username and password to access the course.")
        elif auth_status is True:
            st.rerun()

    with tab_register:
        try:
            email, username, name = authenticator.register_user(
                pre_authorized=config["pre-authorized"]["emails"]
            )
            if email:
                save_config(config)
                st.success("Registered successfully — switch to the Login tab.")
        except Exception as e:
            st.error(e)

    with tab_forgot_pw:
        try:
            username, email, new_password = authenticator.forgot_password()
            if username:
                save_config(config)
                st.success("New password generated.")
                st.info(f"New password (demo only): {new_password}")
            elif username is False:
                st.error("Username not found")
        except Exception as e:
            st.error(e)

    with tab_forgot_user:
        try:
            username, email = authenticator.forgot_username()
            if username:
                st.success(f"Username recovered (demo only): {username}")
            elif username is False:
                st.error("Email not found")
        except Exception as e:
            st.error(e)


def render_course_home():
    hero(
        "Gamified LangChain Learning",
        "A focused learning app for understanding LangChain, agents, memory, "
        "RAG, and LangGraph through short explanations and practical code examples.",
        "Course home",
    )

    st.header("What this course covers")
    st.markdown("""
- :blue[Models] - initialize chat models and understand model parameters.
- :blue[Prompts] - build reusable prompts, chat prompts, system prompts, and prompt chains.
- :blue[Chains] - connect prompts, models, parsers, and custom logic into workflows.
- :blue[Agents] - create tool-using agents with models, tools, system prompts, and structured output.
- :blue[Tools] - define callable tools, use runtime context, and manage tool return values.
- :blue[Memory] - add short-term memory for threads and long-term memory across sessions.
- :blue[RAG] - use embeddings, vector stores, and retrieval chains for grounded answers.
- :blue[Agentic AI] - design multi-agent systems and build controlled workflows with LangGraph.
- :blue[Interactive demos] - run a FastAPI backend with Ollama-powered agents and chains.
""")

    st.header("Module guide")
    row_1 = st.columns(3)
    with row_1[0]:
        module_card(
            "Module 1",
            "Models, Prompts, Chains",
            "Core LangChain building blocks for model calls, prompt design, and workflows.",
        )
    with row_1[1]:
        module_card(
            "Module 2",
            "Agents and Tools",
            "Tool calling, agent setup, system prompts, and structured output.",
        )
    with row_1[2]:
        module_card(
            "Module 3",
            "Memory",
            "Short-term memory, long-term memory, state, checkpointers, and stores.",
        )

    row_2 = st.columns(3)
    with row_2[0]:
        module_card(
            "Module 4",
            "RAG",
            "Embeddings, vector stores, semantic search, and retrieval chains.",
        )
    with row_2[1]:
        module_card(
            "Module 5",
            "Agentic AI",
            "Multi-agent systems, LangGraph basics, routing, and stateful workflows.",
        )
    with row_2[2]:
        module_card(
            "Module 6",
            "Interactive Demo",
            "FastAPI backend with Ollama, tool calling agents, and LCEL chain styles.",
        )

    st.header("Learning path")
    st.markdown("""
1. Start with :blue[Module 1] to understand models, prompts, and chains.
2. Move to :blue[Module 2] to learn how agents use tools.
3. Use :blue[Module 3] to add memory to conversations and applications.
4. Study :blue[Module 4] to build retrieval-based question answering systems.
5. Finish with :blue[Module 5] to design multi-step and multi-agent workflows.
6. Try :blue[Module 6] to run an interactive agent and chain demo.
""")

    st.header("Key ideas to remember")
    st.markdown("""
- A :blue[model] generates or reasons over text.
- A :blue[prompt] shapes what the model should do.
- A :blue[chain] connects multiple steps into a predictable workflow.
- An :blue[agent] decides when to call tools and when to answer.
- :blue[memory] lets applications remember useful information.
- :blue[RAG] gives models external knowledge at runtime.
- :blue[LangGraph] gives precise control over stateful agent workflows.
- :blue[FastAPI] can expose LangChain agents and chains as backend endpoints.
""")

    st.info(
        "Use the sidebar to open each module. Each page contains summarized "
        "concepts and code examples you can adapt for your own LangChain apps."
    )


def main():
    apply_style("Gamified LangChain Learning")
    authenticator, config = restore_session()

    if st.session_state.get("authentication_status"):
        with st.sidebar:
            st.write(f'Logged in as **{st.session_state.get("name")}**')
            authenticator.logout("Logout", "sidebar")
        render_course_home()
    else:
        render_login_gate(authenticator, config)


if __name__ == "__main__":
    main()

