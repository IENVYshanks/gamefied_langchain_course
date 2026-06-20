import streamlit as st


def apply_style(page_title: str = "Gamified LangChain Learning") -> None:
    st.set_page_config(page_title=page_title, layout="wide")
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    with st.sidebar:
        st.toggle("Dark mode", key="dark_mode")

    if st.session_state.dark_mode:
        palette = {
            "bg": "#07130f",
            "bg_soft": "#0d1f19",
            "panel": "#10251e",
            "panel_soft": "#143128",
            "text": "#e8f3ee",
            "muted": "#a7b8b0",
            "green": "#43d58d",
            "green_dark": "#8af0bd",
            "blue": "#7aa7ff",
            "line": "#24443a",
            "shadow": "rgba(0, 0, 0, 0.32)",
            "app_start": "#081611",
            "sidebar": "#081611",
            "table_header": "#17392e",
            "table_cell": "rgba(16, 37, 30, 0.72)",
            "code_border": "#2d5146",
            "code_bg": "#07100d",
            "inline_code": "#b6ffd6",
            "inline_code_bg": "rgba(67, 213, 141, 0.10)",
            "alert_bg": "rgba(20, 49, 40, 0.72)",
            "hero_bg": "#10251e",
            "green_glow": "rgba(67, 213, 141, 0.16)",
            "blue_glow": "rgba(122, 167, 255, 0.10)",
        }
    else:
        palette = {
            "bg": "#f6f8fb",
            "bg_soft": "#eef5f1",
            "panel": "#ffffff",
            "panel_soft": "#eef5f1",
            "text": "#17202a",
            "muted": "#53606f",
            "green": "#1f7a4d",
            "green_dark": "#145c39",
            "blue": "#2563eb",
            "line": "#d9e2ec",
            "shadow": "rgba(23, 32, 42, 0.08)",
            "app_start": "#f8fbfd",
            "sidebar": "#ffffff",
            "table_header": "#eaf3ee",
            "table_cell": "rgba(255, 255, 255, 0.92)",
            "code_border": "#d4dde7",
            "code_bg": "#f7fafc",
            "inline_code": "#145c39",
            "inline_code_bg": "rgba(31, 122, 77, 0.10)",
            "alert_bg": "rgba(238, 245, 241, 0.92)",
            "hero_bg": "#ffffff",
            "green_glow": "rgba(31, 122, 77, 0.10)",
            "blue_glow": "rgba(37, 99, 235, 0.08)",
        }

    css_vars = f"""
<style>
    :root {{
        --bg: {palette["bg"]};
        --bg-soft: {palette["bg_soft"]};
        --panel: {palette["panel"]};
        --panel-soft: {palette["panel_soft"]};
        --text: {palette["text"]};
        --muted: {palette["muted"]};
        --green: {palette["green"]};
        --green-dark: {palette["green_dark"]};
        --blue: {palette["blue"]};
        --line: {palette["line"]};
        --shadow: {palette["shadow"]};
        --app-start: {palette["app_start"]};
        --sidebar: {palette["sidebar"]};
        --table-header: {palette["table_header"]};
        --table-cell: {palette["table_cell"]};
        --code-border: {palette["code_border"]};
        --code-bg: {palette["code_bg"]};
        --inline-code: {palette["inline_code"]};
        --inline-code-bg: {palette["inline_code_bg"]};
        --alert-bg: {palette["alert_bg"]};
        --hero-bg: {palette["hero_bg"]};
        --green-glow: {palette["green_glow"]};
        --blue-glow: {palette["blue_glow"]};
    }}
"""
    st.markdown(
        css_vars
        + """
    .stApp {
        background:
            radial-gradient(circle at top left, var(--green-glow), transparent 30rem),
            radial-gradient(circle at bottom right, var(--blue-glow), transparent 26rem),
            linear-gradient(180deg, var(--app-start) 0%, var(--bg) 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    h1 {
        color: var(--green-dark);
        font-weight: 800;
        letter-spacing: 0;
        margin-bottom: 0.4rem;
    }

    h2 {
        border-top: 1px solid var(--line);
        padding-top: 1.5rem;
        margin-top: 2.25rem;
        color: var(--text);
        letter-spacing: 0;
    }

    h3 {
        color: var(--green-dark);
        margin-top: 1.4rem;
        letter-spacing: 0;
    }

    p, li {
        color: var(--text);
        font-size: 1rem;
        line-height: 1.65;
    }

    [data-testid="stMarkdownContainer"] {
        color: var(--text);
    }

    .stMarkdown strong {
        color: var(--green-dark);
    }

    div[data-testid="stMarkdownContainer"] a {
        color: var(--blue);
        text-decoration: none;
    }

    div[data-testid="stMarkdownContainer"] table {
        overflow: hidden;
        border-radius: 8px;
        border: 1px solid var(--line);
        background: var(--panel);
        color: var(--text);
    }

    div[data-testid="stMarkdownContainer"] th {
        background: var(--table-header);
        color: var(--green-dark);
        font-weight: 700;
    }

    div[data-testid="stMarkdownContainer"] td {
        color: var(--text);
        background: var(--table-cell);
    }

    div[data-testid="stMarkdownContainer"] td,
    div[data-testid="stMarkdownContainer"] th {
        border-color: var(--line);
        padding: 0.65rem 0.8rem;
    }

    [data-testid="stCodeBlock"] {
        border: 1px solid var(--code-border);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 10px 24px var(--shadow);
    }

    [data-testid="stCodeBlock"] pre {
        background: var(--code-bg);
    }

    code {
        color: var(--inline-code);
        background: var(--inline-code-bg);
        border-radius: 5px;
        padding: 0.08rem 0.24rem;
    }

    [data-testid="stAlert"] {
        border-radius: 8px;
        border: 1px solid var(--line);
        background: var(--alert-bg);
        color: var(--text);
    }

    .hero {
        background:
            linear-gradient(135deg, var(--green-glow), var(--blue-glow)),
            var(--hero-bg);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1.35rem 1.5rem;
        margin: 0.35rem 0 1.5rem 0;
        box-shadow: 0 16px 38px var(--shadow);
    }

    .hero-kicker {
        color: var(--green);
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .hero-title {
        color: var(--green-dark);
        font-size: 2.2rem;
        font-weight: 850;
        line-height: 1.15;
        margin: 0;
    }

    .hero-copy {
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.6;
        margin-top: 0.65rem;
        max-width: 760px;
    }

    .module-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        min-height: 145px;
        box-shadow: 0 12px 28px var(--shadow);
    }

    .module-number {
        color: var(--green);
        font-weight: 800;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .module-title {
        color: var(--text);
        font-weight: 800;
        font-size: 1.05rem;
        margin-top: 0.25rem;
    }

    .module-copy {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.5;
        margin-top: 0.4rem;
    }

    .metric-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.75rem;
        margin: 1rem 0 1.5rem;
    }

    .metric {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 0.85rem 0.9rem;
    }

    .metric-value {
        color: var(--green-dark);
        font-size: 1.45rem;
        font-weight: 850;
        line-height: 1;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.84rem;
        margin-top: 0.35rem;
    }

    @media (max-width: 760px) {
        .hero-title {
            font-size: 1.65rem;
        }

        .metric-strip {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, copy: str, kicker: str = "LangChain course") -> None:
    st.markdown(
        f"""
<div class="hero">
    <div class="hero-kicker">{kicker}</div>
    <div class="hero-title">{title}</div>
    <div class="hero-copy">{copy}</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def module_card(number: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
<div class="module-card">
    <div class="module-number">{number}</div>
    <div class="module-title">{title}</div>
    <div class="module-copy">{copy}</div>
</div>
        """,
        unsafe_allow_html=True,
    )
