"""Financial research multi-agent team reusable from API, CLI, and tests."""
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from agno.agent import Agent
from agno.models.groq import Groq
from agno.team.mode import TeamMode
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()
NEWS_MAX_RESULTS, NEWS_DAYS = 5, 7

def search_recent_news(query: str, max_results: int = NEWS_MAX_RESULTS, days: int = NEWS_DAYS) -> list[dict[str, Any]]:
    """Return normalized, recent, deduplicated news results from DDGS."""
    try: raw_results = DDGS().news(query, max_results=max_results)
    except Exception: return []
    cutoff, results, urls = datetime.now(timezone.utc) - timedelta(days=days), [], set()
    for item in raw_results or []:
        if not isinstance(item, dict): continue
        title, url = str(item.get("title") or "").strip(), str(item.get("url") or "").strip()
        if not title or not url or url in urls: continue
        urls.add(url); date_value = str(item.get("date") or "").strip()
        try:
            published = datetime.fromisoformat(date_value.replace("Z", "+00:00")); published = published.replace(tzinfo=timezone.utc) if published.tzinfo is None else published
        except ValueError: published = None
        if published and published < cutoff: continue
        results.append({"title":title,"date":published.isoformat() if published else date_value,"source":str(item.get("source") or "").strip(),"summary":str(item.get("body") or "").strip(),"url":url})
        if len(results) == max_results: break
    return results

def create_financial_research_team() -> Team:
    """Build a coordinator and its market-data and news specialists."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: raise RuntimeError("GROQ_API_KEY is not set. Add it to the environment or .env file.")
    model = Groq(id=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), api_key=api_key)
    web_agent = Agent(id="web-search-agent", name="Web Search Agent", model=model, markdown=True, tool_call_limit=1, role="A financial news researcher who returns concise, sourced, factual recent news.", tools=[search_recent_news], instructions=["Use search_recent_news for current news and perform only one search.","Return at most five relevant items with headline, date, source, summary, and URL.","Never invent news, dates, sources, or URLs. Clearly separate facts from interpretation."])
    finance_agent = Agent(id="finance-agent", name="Finance AI Agent", model=model, markdown=True, tool_call_limit=4, role="A financial data analyst for stocks, fundamentals, analyst recommendations, and price history.", tools=[YFinanceTools(enable_stock_price=True,enable_company_info=True,enable_stock_fundamentals=True,enable_analyst_recommendations=True,enable_company_news=True,enable_historical_prices=True)], instructions=["Use financial tools whenever current data is required.","Use correct tickers (NVIDIA is NVDA). Never invent figures or analyst ratings.","Return concise, structured findings and distinguish retrieved data from interpretation."])
    return Team(id="financial-research-team",name="Financial Research Team",mode=TeamMode.coordinate,model=model,members=[web_agent,finance_agent],markdown=True,tool_call_limit=2,instructions=["You coordinate financial research. Delegate market data to Finance AI Agent and recent news to Web Search Agent.","Use both agents when appropriate; do not repeat delegation or failed operations.","Synthesize one answer, preserving sources and URLs. Use tables for structured data.","Clearly distinguish facts from analysis and never fabricate financial information."])

if __name__ == "__main__":
    create_financial_research_team().print_response(input("Ask a financial research question: ").strip(), stream=True)
