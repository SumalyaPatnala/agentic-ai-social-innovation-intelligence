from typing import Annotated, TypedDict, Optional, List, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class State(TypedDict, total=False):
    """
    Represents the shared state passed through the LangGraph workflow.

    The reducer add_messages appends new messages to the existing messages list.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    frequency: str
    news_data: List[Any]
    summary: str
    filename: str