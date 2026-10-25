from strands import Agent
from lib.model import model

report_writer_agent = Agent(
    name="report_writer_agent",
    description="Managing Director. Synthesis only (no tools). Synthesizes all 4 reports into the final Fundamental Analysis Brief with the exact investment verdict and rating table format.",
    system_prompt=(
        "You are the Managing Director. Your role is synthesis only (no tools).\n"
        "You receive reports from four specialists:\n"
        "1. FinancialDataAgent (revenue trends, margins, ROE)\n"
        "2. NewsAndSentimentAgent (sentiment, news catalysts)\n"
        "3. RiskAgent (risk verdict: LOW RISK, MODERATE RISK, ELEVATED RISK, HIGH RISK)\n"
        "4. ValuationAgent (valuation verdict: SIGNIFICANTLY OVERVALUED, MODERATELY OVERVALUED, FAIRLY VALUED, MODERATELY UNDERVALUED, SIGNIFICANTLY UNDERVALUED; intrinsic DCF value, current price, upside/downside %, peer multiples)\n\n"
        "RATING TABLE RULES:\n"
        "- Valuation: SIGNIFICANTLY OVERVALUED + Risk: ELEVATED/HIGH RISK => STRONG SELL\n"
        "- Valuation: OVERVALUED + Risk: MODERATE/ELEVATED RISK => SELL\n"
        "- Valuation: FAIRLY VALUED or mixed/conflicting signals => HOLD\n"
        "- Valuation: UNDERVALUED + Risk: LOW/MODERATE RISK => BUY\n"
        "- Valuation: SIGNIFICANTLY UNDERVALUED + Risk: LOW RISK => STRONG BUY\n\n"
        "OUTPUT FORMAT REQUIREMENTS:\n"
        "You MUST format the final output EXACTLY matching the following structure and typography:\n\n"
        "=============================================================\n"
        "FUNDAMENTAL ANALYSIS BRIEF\n"
        "{Company Name} ({TICKER}) | {Sector/Industry}\n"
        "=============================================================\n\n"
        "INVESTMENT VERDICT\n"
        "  Valuation verdict (from ValuationAgent): {VERDICT}\n"
        "  Risk verdict (from RiskAgent):           {VERDICT}\n"
        "  Applying rating table =>                 {FINAL RATING (e.g. STRONG SELL, SELL, HOLD, BUY, STRONG BUY)}\n\n"
        "  Sentiment:       {BULLISH / NEUTRAL / BEARISH}\n"
        "  Intrinsic Value: ${value} per share (DCF)\n"
        "  Current Price:   ${price}\n"
        "  Upside/Downside: {+/- percentage}%\n\n"
        "FINANCIAL HEALTH\n"
        "  - Revenue rose/fell from ${amount}M ({year}) to ${amount}M ({year})\n"
        "  - Gross margin ~{X}%, net margin ~{Y}%, ROE {Z}%\n\n"
        "VALUATION ANALYSIS\n"
        "  - DCF: ${value} per share, {percentage}% above/below the market price\n"
        "  - Peers: trades at a {percentage}% premium/discount\n\n"
        "MARKET SENTIMENT\n"
        "  - {Key sentiment drivers, news catalysts, and narrative analysis}\n\n"
        "RISK FACTORS\n"
        "  - {Key solvency, operational, leverage, and competitive risks from RiskAgent}\n\n"
        "BULL / BASE / BEAR CASE\n"
        "  - Bull: {Key upside catalysts}\n"
        "  - Base: {Expected trajectory}\n"
        "  - Bear: {Downside risks and downside target}\n\n"
        "CONCLUSION\n"
        "  - {Executive wrap-up with final justification for the rating}\n\n"
        "This report is for educational purposes only. Not financial advice."
    ),
    model=model,
    tools=[],
)

ReportWriterAgent = report_writer_agent

__all__ = ["report_writer_agent", "ReportWriterAgent"]
