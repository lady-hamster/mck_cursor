"""Fixed case for the MVP. Swap this dict later without changing app.py."""

import json
import random

CASE = {
    "title": "Declining Profitability — TechRetail Co.",
    "public_brief": (
        "Your client is TechRetail Co., a consumer electronics retail chain. "
        "Their profitability has dropped 30% over the last two years. The CEO "
        "wants to know why, and what to do about it."
    ),
    "hidden_context": {
        "revenue_trend": "Revenue has been stable, even slightly growing (~3% over two years).",
        "cost_structure": (
            "Rent and staffing costs rose 40% due to physical store expansion "
            "over the last 2 years."
        ),
        "competitor_landscape": (
            "Two online-only competitors entered the market with lower fixed costs "
            "and 10–15% lower prices on comparable SKUs."
        ),
        "customer_data": (
            "In-store foot traffic dropped 15%; online sales grew but still "
            "represent only 20% of total revenue."
        ),
        "store_footprint": (
            "The chain opened 18 new stores in the last two years, mostly in "
            "suburban malls with high rent."
        ),
        "margins": (
            "Gross margin is roughly unchanged. The profitability drop is driven "
            "by operating costs, not by a collapse in unit economics per item sold."
        ),
    },
    "case_type": "profitability",
    "reference_hypothesis": (
        "The drop in profitability is explained by rising fixed costs "
        "(physical expansion) without proportional revenue growth, compounded "
        "by competitive pressure from online players."
    ),
}

INDUSTRIES = ["retail", "healthcare", "logistics", "fintech", "public sector", "hospitality"]
CASE_TYPES = ["profitability", "market entry", "growth strategy", "pricing strategy"]


def _strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()
    return cleaned


def generate_case(client, model: str) -> dict:
    industry = random.choice(INDUSTRIES)
    case_type = random.choice(CASE_TYPES)

    system_prompt = f"""You are generating a business case for a case-interview
    training tool. Create a {case_type} case in the {industry} industry.

    Respond with ONLY valid JSON, no markdown fences, no extra text, matching
    exactly this structure:

    {{
      "title": "string",
      "public_brief": "string, 2-3 sentences, what the candidate sees first",
      "hidden_context": {{
        "key_fact_1": "string",
        "key_fact_2": "string",
        "key_fact_3": "string",
        "key_fact_4": "string"
      }},
      "case_type": "{case_type}",
      "reference_hypothesis": "string, the model-answer hypothesis"
    }}"""

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": "Generate the case now."}],
    )

    for block in response.content:
        if block.type == "text":
            raw = _strip_markdown_fences(block.text)
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError(f"Model returned invalid JSON (raw text: {raw!r})") from e
    raise ValueError("No text block found in response")


def get_case(client, model: str):
    try:
        return generate_case(client, model), None
    except Exception as e:
        return CASE, str(e)
