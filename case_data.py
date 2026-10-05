"""Fixed case for the MVP. Swap this dict later without changing app.py."""

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
