import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class AINewsNode:
    def __init__(self, llm):
        tavily_api_key = os.getenv("TAVILY_API_KEY")

        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY is missing.")

        self.tavily = TavilyClient(api_key=tavily_api_key)
        self.llm = llm

    def fetch_news(self, state: dict) -> dict:
        print("FETCH_NEWS STARTED")
        print("STATE IN FETCH_NEWS:", state)

        frequency = state["messages"][0].content.lower().strip()
        print("FREQUENCY:", frequency)

        time_range_map = {
            "daily": "d",
            "weekly": "w",
            "monthly": "m",
            "year": "y",
        }

        days_map = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
            "year": 366,
        }

        if frequency not in time_range_map:
            raise ValueError(
                f"Invalid frequency: {frequency}. Choose daily, weekly, monthly, or year."
            )

        response = self.tavily.search(
            query="Top Artificial Intelligence AI technology news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer=True,
            max_results=20,
            days=days_map[frequency],
        )

        news_data = response.get("results", [])

        print("NEWS COUNT:", len(news_data))

        return {
            "frequency": frequency,
            "news_data": news_data,
        }

    def summarize_news(self, state: dict) -> dict:
        print("SUMMARIZE_NEWS STARTED")
        print("STATE IN SUMMARIZE_NEWS:", state)

        news_items = state.get("news_data", [])

        if not news_items:
            raise ValueError("No news data found from Tavily search.")

        prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                """Summarize AI news articles into markdown format. For each item include:
- Date in **YYYY-MM-DD** format in PST timezone
- Concise summary from latest news
- Sort news by date wise, latest first
- Source URL as markdown link

Use format:
### [Date]
- [Summary](URL)
"""
            ),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Date: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(
            prompt_template.format(articles=articles_str)
        )

        summary = response.content

        print("SUMMARY GENERATED LENGTH:", len(summary))

        return {
            "summary": summary,
        }

    def save_result(self, state: dict) -> dict:
        print("SAVE_RESULT STARTED")
        print("STATE IN SAVE_RESULT:", state)

        frequency = state.get("frequency")
        summary = state.get("summary")

        if not frequency:
            raise ValueError("Frequency missing in state.")

        if not summary:
            raise ValueError("Summary missing in state.")

        os.makedirs("./AINEWS", exist_ok=True)

        filename = f"./AINEWS/{frequency}_summary.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        print("NEWS SUMMARY SAVED TO:", filename)
        print("FILE EXISTS:", os.path.exists(filename))

        return {
            "filename": filename,
        }