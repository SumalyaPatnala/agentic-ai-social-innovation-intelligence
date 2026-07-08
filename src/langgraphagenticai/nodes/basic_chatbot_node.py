from src.langgraphagenticai.state.state import State


class BasicChatbotNode:
    """
    Basic chatbot logic implementation.
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a chatbot response.
        """

        messages = state.get("messages", [])

        if not messages:
            raise ValueError(f"No messages found in state. Received state: {state}")

        response = self.llm.invoke(messages)

        return {"messages": [response]}