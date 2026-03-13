from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    """Perform a web search using DuckDuckGo and return a summarized string of results."""
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No results found."
        
        output = [f"- {res['title']}: {res['body']}" for res in results]
        return "\n".join(output)
    except Exception as e:
        return f"Web search failed: {str(e)}"
