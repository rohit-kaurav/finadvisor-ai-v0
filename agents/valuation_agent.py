from strands import Agent
from lib.model import model
from tools import run_dcf_model, get_peer_multiples

valuation_agent = Agent(
    name="valuation_agent",
    description="Valuation specialist. Calculates company intrinsic valuation using DCF modeling and relative peer multiples.",
    system_prompt=(
        "You are the Valuation Specialist. Your role is to determine the intrinsic and relative value "
        "of a company using Discounted Cash Flow (DCF) models and peer valuation multiples.\n\n"
        "Using the financial context and your tools (run_dcf_model, get_peer_multiples), you must calculate and explicitly provide:\n"
        "1. Valuation verdict: Choose one of [SIGNIFICANTLY OVERVALUED | MODERATELY OVERVALUED | FAIRLY VALUED | MODERATELY UNDERVALUED | SIGNIFICANTLY UNDERVALUED]\n"
        "2. Intrinsic Value (DCF): target price per share\n"
        "3. Current Market Price: current price per share\n"
        "4. Upside/Downside: percentage relative to market price (e.g. -48.3%)\n"
        "5. Peers Comparison: whether the stock trades at a premium or discount relative to peer multiples."
    ),
    model=model,
    tools=[run_dcf_model, get_peer_multiples],
)

ValuationAgent = valuation_agent

__all__ = ["valuation_agent", "ValuationAgent"]
