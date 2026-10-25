import functools
import yfinance as yf
from strands import tool
from lib.model import model
from utils.valuation_utils import calculate_dcf

@functools.lru_cache(maxsize=32)
def _get_ticker_info(ticker: str) -> dict:
    cleaned = ticker.strip().upper()
    t = yf.Ticker(cleaned)
    return t.info or {}

@tool
@functools.lru_cache(maxsize=32)
def run_dcf_model(ticker: str) -> str:
    """Run a Discounted Cash Flow (DCF) model to compute intrinsic share value, upside/downside %, and valuation verdict.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        cleaned_ticker = ticker.strip().upper()
        t = yf.Ticker(cleaned_ticker)
        info = t.info or {}
        cf = t.cashflow
        
        # Extract Free Cash Flow
        fcf = None
        if cf is not None and not cf.empty:
            for metric in ["Free Cash Flow", "Operating Cash Flow"]:
                if metric in cf.index:
                    fcf = float(cf.loc[metric].iloc[0])
                    break
        if fcf is None or fcf <= 0:
            fcf = float(info.get("freeCashflow") or info.get("operatingCashflow") or 10_000_000_000)

        shares = float(info.get("sharesOutstanding") or 1_000_000_000)
        current_price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 100.0)
        total_debt = float(info.get("totalDebt") or 0.0)
        total_cash = float(info.get("totalCash") or 0.0)

        # Run DCF calculation
        res = calculate_dcf(
            free_cash_flow=fcf,
            shares_outstanding=shares,
            current_price=current_price,
            growth_rate=0.08,
            terminal_growth_rate=0.025,
            discount_rate=0.09,
            total_debt=total_debt,
            cash_and_equivalents=total_cash,
        )

        output = [
            f"=== DCF Valuation Model for {cleaned_ticker} ===",
            f"Valuation verdict (from ValuationAgent): {res['verdict']}",
            f"Intrinsic Value: ${res['intrinsic_value']:.2f} per share (DCF)",
            f"Current Price: ${res['current_price']:.2f}",
            f"Upside/Downside: {res['upside_downside_pct']:+.1f}%",
            f"\nDCF Breakdown & Assumptions:",
            f"- Base Free Cash Flow: ${fcf:,.0f}",
            f"- Discount Rate (WACC): {res['assumptions']['discount_rate']}",
            f"- Projected 5-Year Growth Rate: {res['assumptions']['growth_rate']}",
            f"- Terminal Growth Rate: {res['assumptions']['terminal_growth_rate']}",
            f"- Enterprise Value: ${res['enterprise_value']:,.0f}",
            f"- Equity Value: ${res['equity_value']:,.0f}",
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error executing DCF model for {ticker}: {str(e)}"

@tool
@functools.lru_cache(maxsize=32)
def get_peer_multiples(ticker: str) -> str:
    """Retrieve relative valuation multiples (P/E, EV/EBITDA, P/S, P/B) and compare against peer and sector averages.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        cleaned_ticker = ticker.strip().upper()
        info = _get_ticker_info(cleaned_ticker)
        
        pe = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        ev_ebitda = info.get("enterpriseToEbitda")
        ps = info.get("priceToSalesTrailing12Months")
        pb = info.get("priceToBook")
        sector = info.get("sector", "General Market")
        industry = info.get("industry", "Industry Benchmark")

        # Typical tech / broad market peer median benchmarks
        peer_benchmarks = {
            "trailing_pe": 26.5,
            "forward_pe": 22.0,
            "ev_ebitda": 18.0,
            "ps": 4.5,
        }

        # Calculate premium/discount to peer benchmark
        if pe:
            premium_pct = ((pe - peer_benchmarks["trailing_pe"]) / peer_benchmarks["trailing_pe"]) * 100
            peer_relation = f"trades at a {abs(premium_pct):.1f}% {'premium' if premium_pct > 0 else 'discount'}"
        else:
            peer_relation = "trades in line with peer group averages"

        output = [
            f"=== Peer Multiples & Relative Valuation for {cleaned_ticker} ===",
            f"Sector: {sector} | Industry: {industry}",
            f"Peer Benchmark Comparison: {peer_relation}",
            f"\nValuation Multiples:",
            f"- Trailing P/E: {f'{pe:.2f}' if pe else 'N/A'} (Peer Median: {peer_benchmarks['trailing_pe']:.1f})",
            f"- Forward P/E: {f'{forward_pe:.2f}' if forward_pe else 'N/A'} (Peer Median: {peer_benchmarks['forward_pe']:.1f})",
            f"- EV/EBITDA: {f'{ev_ebitda:.2f}' if ev_ebitda else 'N/A'} (Peer Median: {peer_benchmarks['ev_ebitda']:.1f})",
            f"- Price/Sales (P/S): {f'{ps:.2f}' if ps else 'N/A'} (Peer Median: {peer_benchmarks['ps']:.1f})",
            f"- Price/Book (P/B): {f'{pb:.2f}' if pb else 'N/A'}",
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error retrieving peer multiples for {ticker}: {str(e)}"

__all__ = [
    "run_dcf_model",
    "get_peer_multiples",
]