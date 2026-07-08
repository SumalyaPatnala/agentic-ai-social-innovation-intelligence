import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

from src.langgraphagenticai.main import load_langgraph_agenticai_app


if __name__ == "__main__":
    load_langgraph_agenticai_app()