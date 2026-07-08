from langchain_core.messages import SystemMessage
from src.langgraphagenticai.state.state import State


class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with Tavily tool integration.
    """

    def __init__(self, model):
        self.llm = model

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function with tools bound to the LLM.
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Processes the input state and returns an LLM response.
            """

            messages = state.get("messages", [])

            if not messages:
                raise ValueError(f"No messages found in state. Received state: {state}")

            system_message = SystemMessage(
                content=(
                    "You are a helpful AI assistant with access to web search. "
                    "When current or recent information is needed, use only the available tool named tavily_search. "
                    "Do not call brave_search. Do not invent tool names. "
                    "After using the search tool, summarize the results clearly with sources when available."
                )
            )

            response = llm_with_tools.invoke([system_message] + messages)

            return {"messages": [response]}

        return chatbot_node