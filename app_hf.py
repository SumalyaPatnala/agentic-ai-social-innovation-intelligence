import os
import gradio as gr
import spaces

os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder

load_dotenv()


@spaces.GPU(duration=120)
def run_agentic_ai(usecase, model_name, user_input, frequency):
    try:
        user_controls_input = {
            "selected_llm": "Groq",
            "selected_groq_model": model_name,
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            "selected_usecase": usecase,
        }

        llm_config = GroqLLM(user_controls_input=user_controls_input)
        model = llm_config.get_llm_model()

        if model is None:
            return "Error: Groq model could not be initialized."

        graph_builder = GraphBuilder(model)
        graph = graph_builder.setup_graph(usecase)

        if usecase == "Basic Chatbot":
            if not user_input:
                return "Please enter a message."

            result = graph.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            return result["messages"][-1].content

        if usecase == "Chatbot with Web":
            if not user_input:
                return "Please enter a web search query."

            result = graph.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            return result["messages"][-1].content

        if usecase == "AI News":
            selected_frequency = frequency.lower().strip()

            result = graph.invoke({
                "messages": [HumanMessage(content=selected_frequency)]
            })

            filename = result.get(
                "filename",
                f"./AINEWS/{selected_frequency}_summary.md"
            )

            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    return f.read()

            return f"News summary generated, but file was not found at {filename}"

        return "Unsupported use case."

    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(title="Agentic AI Social Innovation Intelligence") as demo:
    gr.Markdown(
        """
        # Agentic AI Social Innovation Intelligence System

        A LangGraph-based agentic AI system for chatbot, web search, and AI news summarization. 
        Built with LangGraph, Groq, Tavily, and Gradio.
        """
    )

    usecase = gr.Dropdown(
        choices=["Basic Chatbot", "Chatbot with Web", "AI News"],
        value="AI News",
        label="Select Use Case"
    )

    model_name = gr.Dropdown(
        choices=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ],
        value="llama-3.3-70b-versatile",
        label="Select Groq Model"
    )

    user_input = gr.Textbox(
        lines=4,
        placeholder="For chatbot/web search, enter your message or query here.",
        label="Input"
    )

    frequency = gr.Dropdown(
        choices=["Daily", "Weekly", "Monthly"],
        value="Weekly",
        label="AI News Time Frame"
    )

    submit_btn = gr.Button("Submit")

    output = gr.Markdown(label="Agent Output")

    submit_btn.click(
        fn=run_agentic_ai,
        inputs=[usecase, model_name, user_input, frequency],
        outputs=output,
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        ssr_mode=False
    )