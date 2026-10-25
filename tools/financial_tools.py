import functools
import yfinance as yf
import pandas as pd
from strands import tool
from lib.model import model

@functools.lru_cache(maxsize=64)
def _get_ticker_data(ticker: str):
    """Cached yfinance Ticker instance to share across tools."""
    cleaned_ticker = ticker.strip().upper()
    return yf.Ticker(cleaned_ticker)

@tool
@functools.lru_cache(maxsize=32)
def get_income_statement(ticker: str) -> str:
    """Retrieve annual income statement metrics (Revenue, Gross Profit, Net Income, etc.) for a company.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        t = _get_ticker_data(ticker)
        financials = t.financials
        if financials is None or financials.empty:
            return f"No income statement data found for {ticker}."
        
        # Select common key rows
        key_metrics = [
            "Total Revenue", "Operating Revenue", "Cost Of Revenue",
            "Gross Profit", "Operating Expense", "Operating Income",
            "Pretax Income", "Net Income", "Diluted EPS"
        ]
        available_metrics = [m for m in key_metrics if m in financials.index]
        if not available_metrics:
            # Fallback to top 10 rows if exact names differ
            subset = financials.iloc[:10]
        else:
            subset = financials.loc[available_metrics]
            
        # Format columns as year strings
        subset.columns = [col.strftime("%Y") if hasattr(col, "strftime") else str(col) for col in subset.columns]
        
        output = [f"=== Income Statement for {ticker.upper()} ==="]
        for metric, row in subset.iterrows():
            row_str = " | ".join([f"{col}: ${val:,.0f}" if isinstance(val, (int, float)) and abs(val) > 1e4 else f"{col}: {val}" for col, val in row.items()])
            output.append(f"- {metric}: {row_str}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching income statement for {ticker}: {str(e)}"

@tool
@functools.lru_cache(maxsize=32)
def get_balance_sheet(ticker: str) -> str:
    """Retrieve annual balance sheet metrics (Total Assets, Liabilities, Debt, Cash, Equity) for a company.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        t = _get_ticker_data(ticker)
        bs = t.balance_sheet
        if bs is None or bs.empty:
            return f"No balance sheet data found for {ticker}."
            
        key_metrics = [
            "Total Assets", "Current Assets", "Cash And Cash Equivalents",
            "Total Liabilities Net Minority Interest", "Current Liabilities",
            "Total Debt", "Long Term Debt", "Stockholders Equity", "Common Stock Equity"
        ]
        available_metrics = [m for m in key_metrics if m in bs.index]
        if not available_metrics:
            subset = bs.iloc[:10]
        else:
            subset = bs.loc[available_metrics]
            
        subset.columns = [col.strftime("%Y") if hasattr(col, "strftime") else str(col) for col in subset.columns]
        
        output = [f"=== Balance Sheet for {ticker.upper()} ==="]
        for metric, row in subset.iterrows():
            row_str = " | ".join([f"{col}: ${val:,.0f}" if isinstance(val, (int, float)) and abs(val) > 1e4 else f"{col}: {val}" for col, val in row.items()])
            output.append(f"- {metric}: {row_str}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching balance sheet for {ticker}: {str(e)}"

@tool
@functools.lru_cache(maxsize=32)
def get_cash_flow_statement(ticker: str) -> str:
    """Retrieve annual cash flow metrics (Operating Cash Flow, CapEx, Free Cash Flow) for a company.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        t = _get_ticker_data(ticker)
        cf = t.cashflow
        if cf is None or cf.empty:
            return f"No cash flow data found for {ticker}."
            
        key_metrics = [
            "Operating Cash Flow", "Capital Expenditure", "Free Cash Flow",
            "Investing Cash Flow", "Financing Cash Flow", "Repayment Of Debt",
            "Cash Dividends Paid"
        ]
        available_metrics = [m for m in key_metrics if m in cf.index]
        if not available_metrics:
            subset = cf.iloc[:10]
        else:
            subset = cf.loc[available_metrics]
            
        subset.columns = [col.strftime("%Y") if hasattr(col, "strftime") else str(col) for col in subset.columns]
        
        output = [f"=== Cash Flow Statement for {ticker.upper()} ==="]
        for metric, row in subset.iterrows():
            row_str = " | ".join([f"{col}: ${val:,.0f}" if isinstance(val, (int, float)) and abs(val) > 1e4 else f"{col}: {val}" for col, val in row.items()])
            output.append(f"- {metric}: {row_str}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error fetching cash flow statement for {ticker}: {str(e)}"

@tool
@functools.lru_cache(maxsize=32)
def compute_key_ratios(ticker: str) -> str:
    """Compute and retrieve key financial profitability, liquidity, leverage, and valuation ratios.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        t = _get_ticker_data(ticker)
        info = t.info or {}
        
        # Calculate/retrieve margins and ratios
        gross_margins = info.get("grossMargins")
        operating_margins = info.get("operatingMargins")
        profit_margins = info.get("profitMargins")
        roe = info.get("returnOnEquity")
        roa = info.get("returnOnAssets")
        current_ratio = info.get("currentRatio")
        debt_to_equity = info.get("debtToEquity")
        trailing_pe = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        peg_ratio = info.get("pegRatio")
        price_to_book = info.get("priceToBook")
        enterprise_to_ebitda = info.get("enterpriseToEbitda")
        
        output = [
            f"=== Key Financial Ratios for {ticker.upper()} ===",
            f"PROFITABILITY & RETURNS:",
            f"- Gross Margin: {f'{gross_margins*100:.1f}%' if gross_margins is not None else 'N/A'}",
            f"- Operating Margin: {f'{operating_margins*100:.1f}%' if operating_margins is not None else 'N/A'}",
            f"- Net Profit Margin: {f'{profit_margins*100:.1f}%' if profit_margins is not None else 'N/A'}",
            f"- Return on Equity (ROE): {f'{roe*100:.1f}%' if roe is not None else 'N/A'}",
            f"- Return on Assets (ROA): {f'{roa*100:.1f}%' if roa is not None else 'N/A'}",
            f"\nLIQUIDITY & SOLVENCY:",
            f"- Current Ratio: {f'{current_ratio:.2f}' if current_ratio is not None else 'N/A'}",
            f"- Debt to Equity: {f'{debt_to_equity:.2f}' if debt_to_equity is not None else 'N/A'}",
            f"\nVALUATION METRICS:",
            f"- Trailing P/E: {f'{trailing_pe:.2f}' if trailing_pe is not None else 'N/A'}",
            f"- Forward P/E: {f'{forward_pe:.2f}' if forward_pe is not None else 'N/A'}",
            f"- PEG Ratio: {f'{peg_ratio:.2f}' if peg_ratio is not None else 'N/A'}",
            f"- Price to Book: {f'{price_to_book:.2f}' if price_to_book is not None else 'N/A'}",
            f"- EV/EBITDA: {f'{enterprise_to_ebitda:.2f}' if enterprise_to_ebitda is not None else 'N/A'}",
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error computing key ratios for {ticker}: {str(e)}"

__all__ = [
    "get_income_statement",
    "get_balance_sheet",
    "get_cash_flow_statement",
    "compute_key_ratios",
]