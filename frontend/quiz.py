import streamlit as st

from database import get_gamification, get_progress, record_quiz_attempt, save_progress


QUIZZES = {
    "module_1": [
        ("What does a prompt template provide?", ["Reusable prompt structure", "Database storage", "A web server", "Vector compression"], 0),
        ("Which component generates a model response?", ["Parser", "LLM", "Retriever", "Loader"], 1),
        ("What does an output parser do?", ["Trains a model", "Stores files", "Structures model output", "Creates embeddings"], 2),
        ("In LCEL, what does the pipe operator do?", ["Deletes a chain", "Connects runnable steps", "Starts MySQL", "Creates a user"], 1),
        ("Temperature mainly controls what?", ["Response randomness", "Context size", "Network speed", "Database rows"], 0),
        ("A system message normally defines what?", ["File type", "Model behavior", "SQL schema", "User password"], 1),
        ("What is a chain?", ["One static string", "Connected processing steps", "A login cookie", "A vector only"], 1),
        ("Which prompt type represents a conversation?", ["ChatPromptTemplate", "SQLPrompt", "ImagePrompt", "HashPrompt"], 0),
        ("Why use structured output?", ["To get predictable fields", "To increase latency", "To remove prompts", "To store passwords"], 0),
        ("What should hold secrets such as API keys?", ["Source code", "Public prompts", "Environment variables", "Model output"], 2),
    ],
    "module_2": [
        ("What is a tool in an agent?", ["A callable capability", "A model weight", "A CSS rule", "A password"], 0),
        ("Who decides when a tool is called?", ["Database", "Agent/model", "Browser cache", "Output file"], 1),
        ("Why are precise tool descriptions important?", ["They guide tool selection", "They hash data", "They install Python", "They style pages"], 0),
        ("What does ToolRuntime expose?", ["Runtime state and context", "Only HTML", "Model weights", "MySQL passwords"], 0),
        ("A tool schema describes what?", ["Arguments and types", "Screen colors", "Token price", "Git history"], 0),
        ("What should happen after a tool returns?", ["Agent uses the result", "Database is deleted", "App always exits", "Prompt is ignored"], 0),
        ("Why limit available tools?", ["Improve safety and selection", "Increase ambiguity", "Expose secrets", "Disable validation"], 0),
        ("What is runtime context useful for?", ["User ID and permissions", "Changing model weights", "Compiling CSS", "Creating hardware"], 0),
        ("A tool error should ideally be what?", ["Handled clearly", "Silently destructive", "A password leak", "Always retried forever"], 0),
        ("Structured tool arguments help with what?", ["Validation", "Random styling", "File deletion", "Model training"], 0),
    ],
    "module_3": [
        ("Short-term memory is usually scoped to what?", ["A thread", "All companies", "The internet", "Model weights"], 0),
        ("Long-term memory persists across what?", ["Sessions", "One token", "One function line", "CSS rules"], 0),
        ("What stores thread state in LangGraph?", ["Checkpointer", "Retriever", "Embedding", "Prompt parser"], 0),
        ("What stores durable facts?", ["Store", "Temperature", "Loader", "Router only"], 0),
        ("Why include user IDs in namespaces?", ["Data isolation", "Higher temperature", "Faster CSS", "More tokens"], 0),
        ("What is a thread ID used for?", ["Identify a conversation", "Hash passwords", "Name a model", "Create vectors"], 0),
        ("Sensitive memory should be protected by what?", ["Permissions", "Prompt length", "Randomness", "Markdown"], 0),
        ("Production memory commonly uses what?", ["Database-backed storage", "Only Python variables", "Screenshots", "Hard-coded text"], 0),
        ("Memory state should contain what?", ["Useful relevant data", "Every secret", "Unbounded logs", "Model binaries"], 0),
        ("Most real agents use which combination?", ["Checkpointer and store", "CSS and HTML", "Only temperature", "Only a loader"], 0),
    ],
    "module_4": [
        ("What does RAG stand for?", ["Retrieval-Augmented Generation", "Random Agent Graph", "Runtime API Gateway", "Recursive Answer Generator"], 0),
        ("What do embeddings represent?", ["Semantic meaning as vectors", "Passwords", "CSS themes", "SQL tables"], 0),
        ("What does a vector store support?", ["Similarity search", "Password hashing", "Page styling", "Model training only"], 0),
        ("Why split documents into chunks?", ["Improve retrieval granularity", "Delete context", "Create users", "Hide sources"], 0),
        ("What does a retriever return?", ["Relevant documents", "Model weights", "Login cookies", "Database schemas"], 0),
        ("Metadata filters help enforce what?", ["Scope and access", "Temperature", "Font size", "Password length"], 0),
        ("Grounded answers rely on what?", ["Retrieved context", "Random guesses", "CSS", "Session cookies"], 0),
        ("If context is insufficient, the model should do what?", ["Say it does not know", "Invent a source", "Delete the index", "Expose secrets"], 0),
        ("Retrieval quality should be evaluated how?", ["Separately from generation", "Never", "Only by latency", "By font color"], 0),
        ("Which step happens before user queries?", ["Indexing documents", "Answer generation", "Login reset", "Badge award"], 0),
    ],
    "module_5": [
        ("What is a multi-agent system?", ["Multiple specialized agents collaborating", "One SQL row", "A CSS framework", "A password manager"], 0),
        ("What does a router do?", ["Directs tasks to specialists", "Creates embeddings only", "Hashes passwords", "Styles buttons"], 0),
        ("LangGraph provides control over what?", ["Stateful workflows", "Model weights", "Hardware", "Email delivery only"], 0),
        ("What is graph state?", ["Shared workflow data", "A page color", "A database password", "A model file"], 0),
        ("What connects nodes in a graph?", ["Edges", "Cookies", "Embeddings", "Badges"], 0),
        ("A supervisor agent usually does what?", ["Coordinates workers", "Stores CSS", "Trains all models", "Creates passwords"], 0),
        ("Why specialize agents?", ["Focused tools and context", "More ambiguity", "Unlimited permissions", "No evaluation"], 0),
        ("Human-in-the-loop is useful for what?", ["Sensitive approvals", "Every token", "CSS rendering", "Vector dimensions"], 0),
        ("Tracing helps explain what?", ["Which steps and tools ran", "Only font size", "Password hashes", "Model weights"], 0),
        ("Multi-agent design is largely what?", ["Context engineering", "Image compression", "Database deletion", "Cookie styling"], 0),
    ],
}


def badge_for(points: int) -> str:
    if points >= 400:
        return "🥇 Gold"
    if points >= 250:
        return "🥈 Silver"
    if points >= 100:
        return "🥉 Bronze"
    return "🌱 Newbie"


def render_module_quiz(module_key: str) -> None:
    user_id = st.session_state["user_id"]
    stats = get_gamification(user_id)
    st.divider()
    st.header("Module challenge")
    st.write(f"**{stats['points']} points · {badge_for(stats['points'])} badge**")

    if get_progress(user_id, module_key) < 100:
        st.info("Finished reading? Mark this module complete to unlock its 10-question quiz.")
        if st.button("I completed this module", key=f"complete_{module_key}"):
            save_progress(user_id, module_key, 100)
            st.rerun()
        return

    questions = QUIZZES[module_key]
    with st.form(f"quiz_{module_key}"):
        answers = [
            st.radio(f"{number}. {question}", options, index=None, key=f"{module_key}_q{number}")
            for number, (question, options, _) in enumerate(questions, 1)
        ]
        submitted = st.form_submit_button("Submit quiz")
    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Please answer all 10 questions before submitting.")
            return
        score = sum(answer == options[correct] for answer, (_, options, correct) in zip(answers, questions))
        record_quiz_attempt(user_id, module_key, score)
        updated = get_gamification(user_id)
        st.success(f"You scored {score}/10. Your best scores are worth {updated['points']} points.")
        st.info(f"Current badge: {badge_for(updated['points'])}")
