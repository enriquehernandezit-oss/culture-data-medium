import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_web_period(query: str, year: str) -> str:
    """Search the web for content about a topic in a specific year."""
    enhanced_query = f"{query} {year}"
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": enhanced_query,
                "max_results": 4,
                "search_depth": "basic"
            }
        )
        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No results found."
        output = []
        for r in results:
            output.append(
                f"Title: {r.get('title')}\n"
                f"URL: {r.get('url')}\n"
                f"Summary: {r.get('content', '')}\n"
                f"Published: {r.get('published_date', 'unknown')}\n"
            )
        return "\n".join(output)
    except Exception as e:
        return f"Search error: {str(e)}"


def search_reddit_period(query: str, year: str) -> str:
    """Search Reddit for discussions about a topic in a specific year."""
    try:
        headers = {"User-Agent": "CultureDelta/1.0"}
        url = "https://www.reddit.com/search.json"
        enhanced_query = f"{query} {year}"
        params = {
            "q": enhanced_query,
            "sort": "relevance",
            "limit": 8,
            "t": "all"
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        if not posts:
            return "No Reddit posts found."
        output = []
        for post in posts[:4]:
            p = post["data"]
            output.append(
                f"Title: {p.get('title')}\n"
                f"Subreddit: r/{p.get('subreddit')}\n"
                f"Score: {p.get('score')}\n"
                f"Text: {p.get('selftext', '')[:300]}\n"
            )
        return "\n".join(output)
    except Exception as e:
        return f"Reddit search error: {str(e)}"


def get_trend_context(query: str, year_from: str, year_to: str) -> str:
    """Search for trend analysis articles comparing two time periods."""
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": f"{query} trend change evolution {year_from} {year_to} shift growth decline",
                "max_results": 4,
                "search_depth": "basic"
            }
        )
        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No trend data found."
        output = []
        for r in results:
            output.append(
                f"Title: {r.get('title')}\n"
                f"Content: {r.get('content', '')[:400]}\n"
            )
        return "\n".join(output)
    except Exception as e:
        return f"Trends error: {str(e)}"