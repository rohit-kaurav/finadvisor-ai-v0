import functools
from datetime import datetime
import yfinance as yf
from strands import tool
from lib.model import model

@functools.lru_cache(maxsize=32)
def _fetch_news_items(ticker: str, count: int = 8) -> list:
    """Helper to fetch news items via yfinance Search and Ticker with caching."""
    cleaned_ticker = ticker.strip().upper()
    news_items = []
    try:
        # yf.Search provides reliable recent news in latest yfinance
        search_res = yf.Search(cleaned_ticker, news_count=count)
        if search_res and search_res.news:
            news_items.extend(search_res.news)
    except Exception:
        pass
        
    if not news_items:
        try:
            t = yf.Ticker(cleaned_ticker)
            if t.news:
                news_items.extend(t.news)
        except Exception:
            pass

    return news_items[:count]

@tool
@functools.lru_cache(maxsize=32)
def search_recent_news(ticker: str) -> str:
    """Search and retrieve recent market news, announcements, and headlines for a company ticker.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        items = _fetch_news_items(ticker, count=6)
        if not items:
            return f"No recent news articles found for {ticker}."
            
        output = [f"=== Recent News for {ticker.upper()} ==="]
        for idx, item in enumerate(items, 1):
            title = item.get("title") or item.get("headline") or "No title"
            publisher = item.get("publisher", "Unknown Publisher")
            pub_time = item.get("providerPublishTime")
            time_str = datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d %H:%M") if pub_time else "Recent"
            link = item.get("link", "")
            output.append(f"{idx}. [{time_str}] {title} (Source: {publisher})")
            if link:
                output.append(f"   Link: {link}")
                
        return "\n".join(output)
    except Exception as e:
        return f"Error retrieving recent news for {ticker}: {str(e)}"

@tool
@functools.lru_cache(maxsize=32)
def analyze_sentiment(ticker: str) -> str:
    """Analyze recent market and news sentiment for a company ticker, categorizing as BULLISH, NEUTRAL, or BEARISH.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        items = _fetch_news_items(ticker, count=8)
        if not items:
            return f"Sentiment for {ticker.upper()}: NEUTRAL (insufficient recent news data)."
            
        headlines = [item.get("title", "") for item in items if item.get("title")]
        
        # Financial sentiment keywords lexicon
        positive_keywords = {
            "surge", "jump", "growth", "beat", "rally", "outperform", "bull", "record",
            "profit", "strong", "higher", "gain", "buy", "upgrade", "lead", "boost",
            "expand", "breakthrough", "partnership", "success", "innovative", "dividend"
        }
        negative_keywords = {
            "drop", "fall", "miss", "decline", "slump", "loss", "bear", "plunge",
            "downgrade", "probe", "investigation", "lawsuit", "layoffs", "cut", "risk",
            "warning", "headwind", "struggle", "debt", "tariff", "antitrust", "penalty"
        }
        
        pos_count = 0
        neg_count = 0
        scored_headlines = []
        
        for h in headlines:
            words = set(h.lower().replace("-", " ").replace(".", " ").split())
            p_hits = words.intersection(positive_keywords)
            n_hits = words.intersection(negative_keywords)
            pos_count += len(p_hits)
            neg_count += len(n_hits)
            tone = "Positive" if len(p_hits) > len(n_hits) else ("Negative" if len(n_hits) > len(p_hits) else "Neutral")
            scored_headlines.append(f"- \"{h}\" [{tone}]")

        if pos_count > neg_count + 1:
            sentiment = "BULLISH"
        elif neg_count > pos_count + 1:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"
            
        output = [
            f"=== Sentiment Analysis for {ticker.upper()} ===",
            f"Sentiment: {sentiment}",
            f"Sentiment Score: {pos_count} positive signals vs {neg_count} negative signals across {len(headlines)} headlines.",
            f"\nHeadline Breakdown:",
            "\n".join(scored_headlines[:5]),
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error analyzing sentiment for {ticker}: {str(e)}"

__all__ = [
    "search_recent_news",
    "analyze_sentiment",
]