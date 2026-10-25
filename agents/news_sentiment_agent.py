from strands import Agent
from lib.model import model
from tools import search_recent_news, analyze_sentiment

news_sentiment_agent = Agent(
    name="news_sentiment_agent",
    description="News desk agent. Searches recent market news, press releases, and analyzes sentiment for a company.",
    system_prompt=(
        "You are the News Desk Analyst. Your role is to search for recent company news, earnings announcements, "
        "and market developments, and analyze overall market sentiment.\n\n"
        "Using your tools (search_recent_news, analyze_sentiment), you must evaluate the company and explicitly provide:\n"
        "1. Sentiment: Choose one of [BULLISH | NEUTRAL | BEARISH]\n"
        "2. Key News Catalysts: Recent developments, earnings highlights, and thematic market sentiment drivers."
    ),
    model=model,
    tools=[search_recent_news, analyze_sentiment],
)

NewsAndSentimentAgent = news_sentiment_agent

__all__ = ["news_sentiment_agent", "NewsAndSentimentAgent"]
