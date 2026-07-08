import os
import gradio as gr

os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

from dotenv import load_dotenv
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from langchain_core.messages import HumanMessage

load_dotenv()


def run_agentic_ai(usecase, model_name, user_input):
    try:
        user_controls_input = {
            "selected_llm": "Groq",
            "selected_groq_model": model_name,
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            "selected_usecase": usecase,
        }

        llm_config = GroqLLM(user_controls_input=user_controls_input)
        model = llm_config.get_llm_model()

        graph_builder = GraphBuilder(model)
        graph = graph_builder.setup_graph(usecase)

        if usecase == "Basic Chatbot":
            result = graph.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            return result["messages"][-1].content

        if usecase == "Chatbot with Web":
            result = graph.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            return result["messages"][-1].content

        if usecase == "AI News":
            frequency = user_input.lower().strip()
            result = graph.invoke({
                "messages": [HumanMessage(content=frequency)]
            })

            filename = result.get("filename", f"./AINEWS/{frequency}_summary.md")

            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    return f.read()

            return f"News summary generated, but file was not found at {filename}"

        return "Unsupported use case."

    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.Interface(
    fn=run_agentic_ai,
    inputs=[
        gr.Dropdown(
            choices=["Basic Chatbot", "Chatbot with Web", "AI News"],
            value="Basic Chatbot",
            label="Select Use Case"
        ),
        gr.Dropdown(
            choices=["llama-3.1-8b-instant"],
            value="llama-3.1-8b-instant",
            label="Select Groq Model"
        ),
        gr.Textbox(
            lines=4,
            placeholder="Enter message, web query, or AI News frequency like daily/weekly/monthly",
            label="Input"
        ),
    ],
    outputs=gr.Markdown(label="Agent Output"),
    title="Agentic AI Social Innovation Intelligence",
    description=(
        "A LangGraph-based agentic AI system for chatbot, web search, "
        "and AI news summarization. Built with LangGraph, Groq, Tavily, and Gradio."
    ),
)

if __name__ == "__main__":
    demo.launch()