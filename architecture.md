# Architecture — Case Interview Coach

## Tech stack

- **Python 3.11+**
- **Streamlit** — UI and server in a single piece; keeps the API key off the
  browser.
- **Anthropic SDK** (`anthropic`) for calls to the Claude API.
- **python-dotenv** to load the API key from `.env` in local development
  (alternative: `st.secrets` if deployed on Streamlit Community Cloud).

Why Streamlit instead of plain HTML/JS: the logic (and the API key) stays
server-side, the code is readable for a non-technical audience, and it avoids
splitting frontend/backend for a demo MVP.

## File structure (MVP)

```
mck_cursor/
├── app.py              # Streamlit app, UI + orchestration
├── case_data.py          # The fixed case: context, hidden data, rubric
├── prompts.py             # System prompts for interviewer and evaluator
├── .env                   # ANTHROPIC_API_KEY (not committed to git)
├── .gitignore              # includes .env
└── requirements.txt        # streamlit, anthropic, python-dotenv
```

## Data flow

1. On load, `case_data.py` provides the **public brief** of the case (the only
   thing the user sees upfront).
2. The user asks clarifying questions in a chat (`st.chat_input`).
3. Each question is sent to the Claude API along with:
   - The "interviewer" system prompt (`prompts.py`)
   - The **full hidden context** of the case (`case_data.py`) — info the
     interviewer knows but doesn't volunteer
   - The conversation history (`st.session_state.messages`)
4. In a separate field, the user writes: case type, client objective, initial
   hypothesis.
5. On clicking "Evaluate", that text + the question history is sent to the API
   with the "evaluator" system prompt and the rubric.
6. The response is displayed structured (not as plain text): broken down by
   rubric criterion.

## Case data schema (`case_data.py`)

```python
CASE = {
    "title": "Declining Profitability — TechRetail Co.",
    "public_brief": (
        "Your client is TechRetail Co., a consumer electronics retail chain. "
        "Their profitability has dropped 30% over the last two years. The CEO "
        "wants to know why, and what to do about it."
    ),
    "hidden_context": {
        "revenue_trend": "Revenue has been stable, even slightly growing.",
        "cost_structure": "Rent and staffing costs rose 40% due to physical"
                            " store expansion over the last 2 years.",
        "competitor_landscape": "Two online-only competitors entered the market"
                                  " with lower fixed costs.",
        "customer_data": "In-store foot traffic dropped 15%; online sales grew"
                           " but still represent only 20% of total revenue.",
        # Add more facts as needed to enrich the case
    },
    "case_type": "profitability",  # used internally by the evaluator
    "reference_hypothesis": (
        "The drop in profitability is explained by rising fixed costs "
        "(physical expansion) without proportional revenue growth, compounded "
        "by competitive pressure from online players."
    ),
}
```

## Evaluation rubric

The evaluator reviews the user's text (case type + objectives + hypothesis)
against these criteria, always in this order:

1. **Case type** — did they correctly identify this as a profitability case
   (not market entry, growth, etc.)?
2. **Client objective** — did they distinguish between "what happened"
   (diagnosis) and "what to do" (prescription)?
3. **MECE structure** — does the hypothesis separate mutually exclusive causes
   (revenue vs. costs) without overlap?
4. **Hypothesis quality** — is it a specific, testable hypothesis, or a vague
   one ("we need to improve efficiency")?
5. **Key questions not asked** — the evaluator can flag 1-2 questions a strong
   candidate would have asked that the user didn't.

Feedback is returned in this format (instruct the model to respond this way):

```
✅ / ⚠️ / ❌  [Criterion]: [brief comment, 1-2 lines]
```

## Extension points (for the demo's "live options")

Design `case_data.py` and `prompts.py` so these extensions are easy to add
live, without touching `app.py`:

- **Dynamic case generation**: replace the fixed `CASE` dict with an API call
  that generates a new one with the same structure (`title`, `public_brief`,
  `hidden_context`, `case_type`, `reference_hypothesis`).
- **Industry selector**: an `st.selectbox` choosing between 2-3 pre-loaded
  cases in a list `CASES = [CASE_RETAIL, CASE_HEALTHCARE, ...]`.
- **Cross-session history**: save `st.session_state.messages` to a local JSON
  file at the end of the session (no database needed yet).
