import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

load_dotenv()


@tool
def tavily_search(query: str) -> str:
    """
    Search the web for recent and factual information.
    Input must be a plain search query string.
    """

    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is missing. Add it to your .env file.")

    client = TavilyClient(api_key=tavily_api_key)

    response = client.search(
        query=query,
        topic="news",
        search_depth="advanced",
        include_answer=True,
        include_images=False,
        include_raw_content=False,
        max_results=5,
    )

    results = response.get("results", [])

    if not results:
        return "No relevant search results found."

    formatted_results = []

    for item in results:
        title = item.get("title", "No title")
        url = item.get("url", "No URL")
        content = item.get("content", "No content")

        formatted_results.append(
            f"Title: {title}\nURL: {url}\nContent: {content}"
        )

    return "\n\n".join(formatted_results)


def get_tools():
    return [tavily_search]


def create_tool_node(tools):
    return ToolNode(tools=tools)