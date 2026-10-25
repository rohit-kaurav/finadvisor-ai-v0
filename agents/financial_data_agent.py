from strands import Agent
from lib.model import model
from tools import get_income_statement, get_balance_sheet, get_cash_flow_statement, compute_key_ratios

financial_data_agent = Agent(
    name="financial_data_agent",
    description="Junior analyst ('the spreadsheet'). Retrieves company financial statements and computes key financial ratios.",
    system_prompt=(
        "You are the Financial Data Junior Analyst ('the spreadsheet'). Your responsibility is to retrieve "
        "and parse complete financial statements (income statement, balance sheet, cash flow statement) "
        "and compute key ratios for the target company.\n\n"
        "Using your tools (get_income_statement, get_balance_sheet, get_cash_flow_statement, compute_key_ratios), "
        "you must explicitly calculate and provide:\n"
        "1. Revenue progression across recent annual/quarterly periods (e.g., from $X M in year1 to $Y M in year2)\n"
        "2. Key profitability & return ratios: Gross margin %, Net margin %, and Return on Equity (ROE %)\n"
        "3. Cash flow generation and balance sheet highlights."
    ),
    model=model,
    tools=[get_income_statement, get_balance_sheet, get_cash_flow_statement, compute_key_ratios],
)

FinancialDataAgent = financial_data_agent

__all__ = ["financial_data_agent", "FinancialDataAgent"]
