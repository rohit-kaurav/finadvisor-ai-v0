import concurrent.futures
from strands import Agent
from lib.model import model
from .financial_data_agent import financial_data_agent
from .news_sentiment_agent import news_sentiment_agent
from .valuation_agent import valuation_agent
from .risk_agent import risk_agent
from .report_writer_agent import report_writer_agent

# Director of Research Agent (calls every specialist as a tool)
orchestrator = Agent(
    name="director_of_research",
    description="Director of research. Calls every specialist as a tool across three phases and returns the final brief word for word.",
    system_prompt=(
        "You are the Director of Research. Your job is to orchestrate the research process by calling "
        "every specialist agent as a tool, and then returning the final brief word for word.\n\n"
        "You MUST follow this exact 3-phase execution order:\n\n"
        "Phase 1 - Three calls at once (the three data agents don't depend on each other, so call them at the same time):\n"
        "  1. financial_data_agent ('junior analyst · the spreadsheet'): gets income statement, balance sheet, cash flow, key ratios.\n"
        "  2. news_sentiment_agent ('news desk'): searches recent news and analyzes sentiment.\n"
        "  3. risk_agent ('risk manager · the sceptic'): checks balance sheet, key ratios, and news for red flags.\n\n"
        "Phase 2 - Then (valuation needs the financial numbers, so it waits):\n"
        "  4. valuation_agent ('valuation specialist'): provide the financial context gathered from financial_data_agent "
        "     so it can run the DCF model and peer multiples.\n\n"
        "Phase 3 - Finally (the writer needs everything, so it goes last):\n"
        "  5. report_writer_agent ('managing director · synthesis only'): send all four reports "
        "     (financial data, news/sentiment, risk, and valuation) to produce the final 'Investment brief' "
        "     (rating table, value, risk, sentiment).\n\n"
        "Return the final Investment Brief from report_writer_agent WORD FOR WORD without truncation or extra commentary."
    ),
    model=model,
    tools=[
        financial_data_agent,
        news_sentiment_agent,
        risk_agent,
        valuation_agent,
        report_writer_agent,
    ],
)

DirectorOfResearch = orchestrator
orchestrator_agent = orchestrator


def run_orchestrator(ticker: str) -> str:
    """
    Executes the 3-phase architecture deterministically:
    Phase 1: Run FinancialDataAgent, NewsAndSentimentAgent, and RiskAgent in parallel.
    Phase 2: Run ValuationAgent with financial context from Phase 1.
    Phase 3: Run ReportWriterAgent with all four reports to generate the Investment Brief.
    """
    print(f"\n[Phase 1] Launching 3 data agents at once for {ticker}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        f_future = executor.submit(
            financial_data_agent,
            f"Retrieve financial statements and compute key financial ratios for {ticker}."
        )
        n_future = executor.submit(
            news_sentiment_agent,
            f"Search recent news and analyze sentiment for {ticker}."
        )
        r_future = executor.submit(
            risk_agent,
            f"Analyze downside risks, balance sheet leverage, and red flags for {ticker}."
        )

        financial_report = str(f_future.result())
        news_report = str(n_future.result())
        risk_report = str(r_future.result())

    print(f"[Phase 2] Running ValuationAgent with financial context for {ticker}...")
    valuation_prompt = (
        f"Perform DCF and peer multiples valuation for {ticker} using this financial context:\n\n"
        f"{financial_report}"
    )
    valuation_report = str(valuation_agent(valuation_prompt))

    print(f"[Phase 3] Running ReportWriterAgent with all 4 reports for {ticker}...")
    writer_prompt = (
        f"Generate the final Investment brief for {ticker} based on all four specialist reports:\n\n"
        f"=== 1. FINANCIAL DATA REPORT ===\n{financial_report}\n\n"
        f"=== 2. NEWS & SENTIMENT REPORT ===\n{news_report}\n\n"
        f"=== 3. RISK ASSESSMENT REPORT ===\n{risk_report}\n\n"
        f"=== 4. VALUATION REPORT ===\n{valuation_report}\n"
    )
    final_brief = str(report_writer_agent(writer_prompt))
    return final_brief


__all__ = [
    "orchestrator",
    "orchestrator_agent",
    "DirectorOfResearch",
    "run_orchestrator",
]

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    brief = run_orchestrator(target)
    print("\n" + "="*50 + "\nFINAL INVESTMENT BRIEF\n" + "="*50)
    print(brief)
