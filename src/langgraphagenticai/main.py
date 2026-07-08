import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph Agentic AI application with Streamlit UI.
    """

    # Load Streamlit UI/sidebar controls
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    

    if st.session_state.get("IsFetchButtonClicked"):
        user_message = st.session_state.get("timeframe", "")
        # user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")
    
    if user_message:
        try:
            # Configure selected LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            # Get selected use case
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected.")
                return

            # Build graph
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(usecase)

            # Display result
            DisplayResultStreamlit(
                usecase=usecase,
                graph=graph,
                user_message=user_message,
            ).display_result_on_ui()

        except Exception as e:
            st.error(f"Error: setup failed - {e}")


if __name__ == "__main__":
    load_langgraph_agenticai_app()