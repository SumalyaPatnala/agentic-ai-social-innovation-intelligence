from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_with_tools_node import ChatbotWithToolNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode


class GraphBuilder:
    """
    Builds LangGraph workflows based on the selected use case.
    """

    def __init__(self, model):
        self.llm = model

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph.
        """

        graph_builder = StateGraph(State)

        basic_chatbot_node = BasicChatbotNode(self.llm)

        graph_builder.add_node("chatbot", basic_chatbot_node.process)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        return graph_builder.compile()

    def chatbot_with_tools_build_graph(self):
        """
        Builds a chatbot graph with Tavily web-search tool integration.
        """

        graph_builder = StateGraph(State)

        tools = get_tools()
        tool_node = create_tool_node(tools)

        chatbot_with_tools_node = ChatbotWithToolNode(self.llm)
        chatbot_node = chatbot_with_tools_node.create_chatbot(tools)

        graph_builder.add_node("chatbot", chatbot_node)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        return graph_builder.compile()
    
    def ai_news_builder_graph(self):

        ai_news_node = AINewsNode(self.llm)

        graph_builder = StateGraph(State)

        ## Added the nodes
        graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        graph_builder.add_node("save_result",ai_news_node.save_result)

        ## Added the edges
        graph_builder.set_entry_point("fetch_news")
        graph_builder.add_edge("fetch_news", "summarize_news")
        graph_builder.add_edge("summarize_news", "save_result")
        graph_builder.add_edge("save_result", END)

        return graph_builder.compile()

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """

        if usecase == "Basic Chatbot":
            return self.basic_chatbot_build_graph()

        if usecase == "Chatbot with Web":
            return self.chatbot_with_tools_build_graph()
        
        if usecase == 'AI News':
            return self.ai_news_builder_graph()

        raise ValueError(
            f"Unsupported use case: {usecase}. "
            "Currently supported use cases are: Basic Chatbot, Chatbot with Web."
        )