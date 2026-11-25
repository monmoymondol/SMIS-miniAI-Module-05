
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="SMIS miniAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROMPT_MODES = {
    "General Assistant": (
        "You are a helpful AI assistant. Give accurate, clear, "
        "well-organized answers. Explain difficult concepts simply."
    ),
    "Coding Assistant": (
        "You are an experienced programming assistant. Explain code, "
        "debug errors, suggest improvements, and provide runnable examples. "
        "Mention assumptions and potential security issues."
    ),
    "Research Assistant": (
        "You are an academic research assistant. Help with research "
        "questions, outlines, literature review planning, methodology, "
        "and academic writing. Never invent citations or research results."
    ),
    "Productivity Assistant": (
        "You are a productivity coach. Break goals into practical tasks, "
        "create realistic schedules, and help prioritize work."
    ),
    "Content Writer": (
        "You are a professional writing assistant. Produce clear, "
        "audience-appropriate writing and follow the requested tone and format."
    ),
}

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
]


def get_saved_api_key():
    """Read a key from environment variables or Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY", "").strip()

    if key:
        return key

    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        return ""


def create_theme(theme):
    """Apply a simple visual theme to the Streamlit interface."""
    if theme == "Dark":
        background = "#0E1117"
        sidebar = "#161B22"
        text = "#F0F3F6"
        card = "#1C2430"
    else:
        background = "#F7F9FC"
        sidebar = "#FFFFFF"
        text = "#182230"
        card = "#FFFFFF"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background};
            color: {text};
        }}
        [data-testid="stSidebar"] {{
            background-color: {sidebar};
        }}
        [data-testid="stChatMessage"] {{
            border: 1px solid rgba(128,128,128,0.18);
            border-radius: 12px;
            padding: 12px;
        }}
        .smis-card {{
            background: {card};
            border: 1px solid rgba(128,128,128,0.20);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def generate_answer(messages, mode, model, api_key, temperature, max_tokens):
    """Send conversation context to the Gemini API."""
    client = genai.Client(api_key=api_key)

    recent_messages = messages[-12:]

    conversation = "\n\n".join(
        f"{'User' if item['role'] == 'user' else 'Assistant'}: "
        f"{item['content']}"
        for item in recent_messages
    )

    response = client.models.generate_content(
        model=model,
        contents=conversation,
        config=types.GenerateContentConfig(
            system_instruction=PROMPT_MODES[mode],
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )

    answer = (response.text or "").strip()

    if not answer:
        raise RuntimeError(
            "The model returned an empty response. Try a different prompt."
        )

    return answer


def export_chat(messages):
    """Create a Markdown transcript for download."""
    lines = [
        "# SMIS miniAI Conversation",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    for item in messages:
        label = "You" if item["role"] == "user" else "SMIS miniAI"
        lines.extend([f"## {label}", item["content"], ""])

    return "\n".join(lines)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "manual_api_key" not in st.session_state:
    st.session_state.manual_api_key = ""


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("🤖 SMIS miniAI")
    st.caption("AI-powered productivity workspace")

    st.divider()

    mode = st.selectbox(
        "Assistant Mode",
        list(PROMPT_MODES.keys()),
    )

    model = st.selectbox(
        "Gemini Model",
        MODELS,
        index=0,
    )

    theme = st.selectbox(
        "Appearance",
        ["System", "Light", "Dark"],
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
    )

    max_tokens = st.slider(
        "Maximum output tokens",
        min_value=256,
        max_value=4096,
        value=2048,
        step=256,
    )

    st.divider()

    saved_key = get_saved_api_key()

    if saved_key:
        api_key = saved_key
        st.success("Gemini API key loaded")
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Used for this session only. Do not share your key.",
        )

    st.caption("Keep your API key private.")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.messages:
        st.download_button(
            "⬇️ Export conversation",
            data=export_chat(st.session_state.messages),
            file_name="smis_miniai_conversation.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.caption("Module 05 | AI Tools & Mini Project")


# ---------------- MAIN INTERFACE ----------------

if theme != "System":
    create_theme(theme)

st.title("SMIS miniAI")
st.write("### Your intelligent workspace for learning and productivity.")

st.caption(
    "Explore AI-assisted coding, research, writing, and everyday tasks."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Assistant Modes", "5")

with col2:
    st.metric("Conversation Messages", len(st.session_state.messages))

with col3:
    st.metric("Selected Model", model.replace("gemini-", "").upper())

st.divider()

# Assistant mode description
st.info(f"Current workspace: **{mode}**")

# Starter prompts
with st.expander("Explore example prompts"):
    examples = {
        "General Assistant": "Explain artificial intelligence in simple language.",
        "Coding Assistant": "Write a Python function to check whether a number is prime.",
        "Research Assistant": "Create a research outline about multi-agent AI systems.",
        "Productivity Assistant": "Create a realistic 7-day learning plan for machine learning.",
        "Content Writer": "Write a professional introduction for a computer science student.",
    }

    st.write(examples[mode])

# Render existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask SMIS miniAI anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            st.warning(
                "Add your Gemini API key in the sidebar or configure "
                "GEMINI_API_KEY in your environment."
            )
        else:
            try:
                with st.spinner("SMIS miniAI is thinking..."):
                    answer = generate_answer(
                        messages=st.session_state.messages,
                        mode=mode,
                        model=model,
                        api_key=api_key,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.error(
                    "The Gemini request failed. Check your API key, "
                    "model access, internet connection, and usage limits."
                )
                st.caption(f"Technical details: {error}")

st.divider()

st.caption(
    "SMIS miniAI is an educational project. "
    "AI-generated output may be inaccurate and should be verified."
)
