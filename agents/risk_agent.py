from strands import Agent
from lib.model import model
from tools import get_balance_sheet, compute_key_ratios, search_recent_news

risk_agent = Agent(
    name="risk_agent",
    description="Risk manager and sceptic. Evaluates balance sheet vulnerabilities, financial ratios, and recent news for red flags and risk factors.",
    system_prompt=(
        "You are the Risk Manager ('the sceptic'). Your role is to critically analyze downside risks, "
        "balance sheet leverage, debt serviceability, liquidity threats, and negative news catalysts.\n\n"
        "Using your tools (get_balance_sheet, compute_key_ratios, search_recent_news), you must evaluate the company and explicitly provide:\n"
        "1. Risk verdict: Choose one of [LOW RISK | MODERATE RISK | ELEVATED RISK | HIGH RISK]\n"
        "2. Key Risk Factors: Specific balance sheet vulnerabilities, leverage concerns, and negative headlines/risks."
    ),
    model=model,
    tools=[get_balance_sheet, compute_key_ratios, search_recent_news],
)

RiskAgent = risk_agent

__all__ = ["risk_agent", "RiskAgent"]
