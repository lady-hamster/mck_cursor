"""Case Interview Coach — Streamlit MVP."""

import json
import os

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

from case_data import CASE, get_case, _strip_markdown_fences
from prompts import (
    evaluator_system_prompt,
    evaluator_user_message,
    interviewer_system_prompt,
)

load_dotenv()

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")
MAX_TOKENS_INTERVIEWER = 400
MAX_TOKENS_EVALUATOR = 2000


def get_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY")
        except Exception:
            api_key = None
    if not api_key:
        st.error(
            "Missing ANTHROPIC_API_KEY. Add it to a local .env file or Streamlit secrets."
        )
        st.stop()
    return Anthropic(api_key=api_key)


def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "evaluation" not in st.session_state:
        st.session_state.evaluation = None
    if "case" not in st.session_state:
        st.session_state.case = CASE
    if "case_error" not in st.session_state:
        st.session_state.case_error = None


def complete(system: str, messages: list[dict], max_tokens: int) -> str:
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise ValueError("No text block found in response")


def ask_interviewer() -> str:
    return complete(
        interviewer_system_prompt(st.session_state.case),
        st.session_state.messages,
        MAX_TOKENS_INTERVIEWER,
    )


def run_evaluation(writeup: str) -> dict:
    raw = complete(
        evaluator_system_prompt(st.session_state.case),
        [{"role": "user", "content": evaluator_user_message(writeup, st.session_state.messages)}],
        MAX_TOKENS_EVALUATOR,
    )
    cleaned = _strip_markdown_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {"_raw_fallback": raw, "_error": str(e)}


def render_evaluation(data: dict) -> None:
    if "_raw_fallback" in data:
        st.warning(f"Could not parse structured feedback: {data.get('_error', 'unknown error')}")
        st.markdown(data["_raw_fallback"])
        return

    def render_area(title: str, area: dict) -> None:
        st.markdown(f"#### {title}")
        cols = st.columns(len(area))
        for col, (key, val) in zip(cols, area.items()):
            with col:
                st.metric(key.replace("_", " ").title(), f"{val['score']}/5")
        for key, val in area.items():
            st.caption(f"**{key.replace('_', ' ').title()}:** {val['comment']}")

    st.subheader("Well done! Here is your feedback")
    render_area("1. Value Addition", data["value_addition"])
    st.divider()
    render_area("2. Client / Team", data["client_team"])
    st.divider()

    st.markdown("#### 3. Reality Check")
    rc = data["reality_check"]
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Airport Test", rc["airport_test"]["answer"].upper())
        st.caption(rc["airport_test"]["comment"])
    with col2:
        st.metric("Offer Decision", rc["offer_decision"]["answer"].upper())
        st.caption(rc["offer_decision"]["comment"])


def render_chat() -> None:
    st.subheader("Clarifying questions")
    st.caption("Ask only what you would ask a live interviewer. Information is not volunteered.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_text = st.chat_input("Ask a clarifying question")
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)
        with st.chat_message("assistant"):
            with st.spinner("Interviewer is responding..."):
                reply = ask_interviewer()
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})


def render_writeup() -> None:
    st.subheader("Frame the case")
    st.caption("Write the case type, the client objective, and your initial hypothesis.")
    writeup = st.text_area(
        "Your framing",
        height=180,
        placeholder=(
            "Case type:\n"
            "Client objective:\n"
            "Initial hypothesis:"
        ),
        label_visibility="collapsed",
    )
    if st.button("Evaluate", type="primary"):
        if not writeup.strip():
            st.warning("Write your case type, objective, and hypothesis before evaluating.")
            return
        with st.spinner("Evaluating against the rubric..."):
            st.session_state.evaluation = run_evaluation(writeup)

    if st.session_state.evaluation:
        render_evaluation(st.session_state.evaluation)


def render_sidebar() -> None:
    if st.sidebar.button("🔄 New case"):
        with st.spinner("Generating a new case..."):
            new_case, error = get_case(get_client(), MODEL)
        st.session_state.case = new_case
        st.session_state.case_error = error
        st.session_state.messages = []
        st.session_state.evaluation = None
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Case Interview Coach", layout="centered")
    init_session()
    render_sidebar()

    if st.session_state.case_error:
        st.error(f"Dynamic case generation failed: {st.session_state.case_error}")

    st.title("Case Interview Coach")
    st.markdown(f"**{st.session_state.case['title']}**")
    st.info(st.session_state.case["public_brief"])

    render_chat()
    st.divider()
    render_writeup()


if __name__ == "__main__":
    main()
