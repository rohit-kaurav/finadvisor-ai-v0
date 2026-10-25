"""Valuation utility functions for DCF modeling and relative peer multiples."""

def calculate_dcf(
    free_cash_flow: float,
    shares_outstanding: float,
    current_price: float,
    growth_rate: float = 0.08,
    terminal_growth_rate: float = 0.025,
    discount_rate: float = 0.09,
    total_debt: float = 0.0,
    cash_and_equivalents: float = 0.0,
    projection_years: int = 5,
) -> dict:
    """
    Computes intrinsic share value using a multi-period Discounted Cash Flow (DCF) model.
    """
    if shares_outstanding <= 0:
        return {
            "error": "Shares outstanding must be positive",
            "intrinsic_value": 0.0,
            "upside_downside_pct": 0.0,
            "verdict": "UNABLE TO CALCULATE",
        }

    # Handle negative or zero starting FCF by using a normalized baseline or positive estimate
    base_fcf = max(free_cash_flow, 1000.0) if free_cash_flow <= 0 else free_cash_flow

    pv_fcf_sum = 0.0
    projected_fcfs = []
    current_fcf = base_fcf

    for year in range(1, projection_years + 1):
        current_fcf *= (1 + growth_rate)
        discount_factor = (1 + discount_rate) ** year
        pv = current_fcf / discount_factor
        pv_fcf_sum += pv
        projected_fcfs.append({"year": year, "fcf": current_fcf, "pv": pv})

    # Terminal Value calculation using Gordon Growth Model
    terminal_value = (current_fcf * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
    pv_terminal_value = terminal_value / ((1 + discount_rate) ** projection_years)

    # Enterprise Value to Equity Value bridge
    enterprise_value = pv_fcf_sum + pv_terminal_value
    equity_value = enterprise_value - total_debt + cash_and_equivalents
    intrinsic_value = max(0.01, equity_value / shares_outstanding)

    upside_downside_pct = ((intrinsic_value - current_price) / current_price) * 100 if current_price > 0 else 0.0

    # Determine valuation verdict based on upside/downside
    if upside_downside_pct < -25.0:
        verdict = "SIGNIFICANTLY OVERVALUED"
    elif upside_downside_pct < -10.0:
        verdict = "MODERATELY OVERVALUED"
    elif upside_downside_pct <= 10.0:
        verdict = "FAIRLY VALUED"
    elif upside_downside_pct <= 25.0:
        verdict = "MODERATELY UNDERVALUED"
    else:
        verdict = "SIGNIFICANTLY UNDERVALUED"

    return {
        "intrinsic_value": round(intrinsic_value, 2),
        "current_price": round(current_price, 2),
        "upside_downside_pct": round(upside_downside_pct, 1),
        "verdict": verdict,
        "enterprise_value": round(enterprise_value, 2),
        "equity_value": round(equity_value, 2),
        "pv_fcf_sum": round(pv_fcf_sum, 2),
        "pv_terminal_value": round(pv_terminal_value, 2),
        "assumptions": {
            "growth_rate": f"{growth_rate * 100:.1f}%",
            "terminal_growth_rate": f"{terminal_growth_rate * 100:.1f}%",
            "discount_rate": f"{discount_rate * 100:.1f}%",
            "projection_years": projection_years,
        },
    }
