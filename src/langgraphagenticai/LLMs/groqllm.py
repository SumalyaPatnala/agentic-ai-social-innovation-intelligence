import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv(override=True)


class GroqLLM:
    """
    Creates and returns a Groq-backed LangChain chat model.
    """

    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            # Prefer .env key first
            groq_api_key = os.getenv("GROQ_API_KEY") or self.user_controls_input.get("GROQ_API_KEY")

            selected_groq_model = self.user_controls_input.get("selected_groq_model")

            if not groq_api_key:
                st.error("Please enter the Groq API key.")
                return None

            if not selected_groq_model:
                st.error("Please select a Groq model.")
                return None

            # Debug only first 8 chars
            print("GROQ KEY USED:", groq_api_key[:8])
            print("GROQ MODEL USED:", selected_groq_model)

            llm = ChatGroq(
                api_key=groq_api_key,
                model=selected_groq_model,
                temperature=0.7,
            )

            return llm

        except Exception as e:
            raise ValueError(f"Error occurred while initializing Groq LLM: {e}")