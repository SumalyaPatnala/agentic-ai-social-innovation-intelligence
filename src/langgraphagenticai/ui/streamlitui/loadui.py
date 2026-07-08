import os
import streamlit as st
from dotenv import load_dotenv

from src.langgraphagenticai.ui.uiconfigfile import Config

load_dotenv()


class LoadStreamlitUI:
    """
    Loads Streamlit sidebar controls and returns user selections.
    """

    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        """
        Loads all Streamlit UI controls.
        Returns:
            dict: User-selected LLM, model, use case, and API keys.
        """

        # Page setup
        st.set_page_config(
            page_title=self.config.get_page_title(),
            layout="wide",
        )

        st.title(self.config.get_page_title())
        st.caption(self.config.get_page_caption())

        # Initialize session state safely
        if "timeframe" not in st.session_state:
            st.session_state.timeframe = ""

        if "IsFetchButtonClicked" not in st.session_state:
            st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox(
                "Select LLM",
                llm_options,
            )

            # Groq model and API key
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()

                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select Model",
                    model_options,
                )

                groq_key_from_env = os.getenv("GROQ_API_KEY", "")

                if groq_key_from_env:
                    self.user_controls["GROQ_API_KEY"] = groq_key_from_env
                    st.success("Groq API key loaded from .env")
                else:
                    self.user_controls["GROQ_API_KEY"] = st.text_input(
                        "Groq API Key",
                        type="password",
                    )

                    if self.user_controls["GROQ_API_KEY"]:
                        os.environ["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"]
                    else:
                        st.warning(
                            "Please enter your GROQ API key. "
                            "Don't have one? Refer: https://console.groq.com/keys"
                        )

            # Use case selection
            self.user_controls["selected_usecase"] = st.selectbox(
                "Select UseCases",
                usecase_options,
            )

            selected_usecase = self.user_controls["selected_usecase"]

            # Tavily API key for web/news use cases
            if selected_usecase in ["Chatbot with Web", "AI News"]:
                tavily_key_from_env = os.getenv("TAVILY_API_KEY", "")

                if tavily_key_from_env:
                    self.user_controls["TAVILY_API_KEY"] = tavily_key_from_env
                    st.success("Tavily API key loaded from .env")
                else:
                    self.user_controls["TAVILY_API_KEY"] = st.text_input(
                        "Tavily API Key",
                        type="password",
                    )

                    if self.user_controls["TAVILY_API_KEY"]:
                        os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]
                    else:
                        st.warning(
                            "Please enter your TAVILY_API_KEY. "
                            "Don't have one? Refer: https://app.tavily.com/home"
                        )

            # AI News controls
            if selected_usecase == "AI News":
                st.subheader("AI News Intelligence")

                time_frame = st.selectbox(
                    "Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=1,
                )

                if st.button("Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame.lower()

        return self.user_controls