import sys
from agents import run_orchestrator, orchestrator

def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(f"=== Starting Financial Advisory Analysis for {ticker} ===")
    
    # Executes the 3-phase research workflow as outlined in the architecture diagram:
    # Phase 1: FinancialDataAgent, NewsAndSentimentAgent, RiskAgent in parallel
    # Phase 2: ValuationAgent using financial context
    # Phase 3: ReportWriterAgent producing the Investment Brief
    brief = run_orchestrator(ticker)
    
    print("\n" + "="*50)
    print("FINAL INVESTMENT BRIEF (Rating · Value · Risk · Sentiment)")
    print("="*50 + "\n")
    print(brief)

if __name__ == "__main__":
    main()
