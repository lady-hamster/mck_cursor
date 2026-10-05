# Workflow & Rules — Case Interview Coach

## Project context

This app is a **demo MVP** for a McKinsey Forward breakout session on Cursor.
Dual pedagogical goal:
1. Simulate, with a single fixed case, the early stages of an MBB-style case
   interview (clarification → framing → objectives → hypothesis → evaluation),
   inspired by the *Case in Point* method (Marc Cosentino).
2. Serve as a live example of how software gets built with an AI agent (Cursor),
   showing iteration, debugging, and feature extension.

**Demo audience:** McKinsey Forward alumni, interested in tech and consulting.
AI knowledge varies — keep the code readable, avoid unnecessary abstraction.

## MVP scope — what TO build

- One **fixed, hardcoded** business case (not dynamically generated).
- A chat where the user asks clarifying questions about the case.
- A text field where the user writes: identified case type, client objective,
  and initial hypothesis.
- An "Evaluate" button that sends that text to the AI and returns structured
  feedback.
- Simple session-state persistence (use `st.session_state`, no database).

## MVP scope — what NOT to build (yet)

These are the "live extension options" shown during the demo, NOT part of the
initial MVP. **Do not implement these unless explicitly asked**:

- Dynamic case generation with AI.
- Industry/case-type selector for the user.
- Multiple cases or cross-session history.
- User authentication.
- Saving results to a database.

If a requested task can be solved more simply without adding these features,
prefer the simpler solution.

## Interviewer behavior rules (case domain)

- The system **never volunteers case information**. It answers exactly what
  the user explicitly asks, just like a real interviewer would.
- If the user asks a vague question, the system can ask for clarification
  instead of assuming and over-answering.
- The interviewer's tone is professional, neutral, slightly terse — it should
  not sound like a generic friendly chatbot.
- Evaluation feedback must follow a consistent rubric (see `architecture.md`
  → Evaluation rubric) and should not invent new criteria each time.

## Agent workflow rules (Cursor)

- Before editing existing code, **briefly explain what you're about to change
  and why**, in 1-3 lines.
- Don't touch files outside the scope of the requested task without flagging
  it first.
- Prefer small, clearly named functions over condensed logic that's hard to
  read live in front of an audience.
- Never hardcode the API key in the code — always via environment variable
  (`.env`, loaded with `python-dotenv` or `st.secrets`).
- If a change breaks something, say so explicitly and show the error before
  attempting to fix it (this is an intentional part of the demo).
- When adding a new feature, show the plan as 2-4 bullets before writing code,
  unless told otherwise.

## Style conventions

- All in English: variable/function names, user-facing strings (UI), and the
  system prompts sent to the model. The event is in English, so no Spanish
  text should appear anywhere visible in the demo.
- Python following PEP8, type hints where they add clarity.
- Comments only where the "why" isn't obvious — avoid commenting the obvious.
- A single `app.py` file for the MVP; split into modules only if the file
  exceeds ~200 lines or it's explicitly requested.
