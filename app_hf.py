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
            return "Error: Groq model could not be initialized. Please check GROQ_API_KEY and model name."

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


def toggle_inputs(usecase):
    if usecase == "AI News":
        return (
            gr.update(visible=False),
            gr.update(visible=True),
        )

    return (
        gr.update(visible=True),
        gr.update(visible=False),
    )


with gr.Blocks(title="Agentic AI Social Innovation Intelligence") as demo:
    gr.Markdown(
        """
        # Agentic AI Social Innovation Intelligence System

        LangGraph-powered AI news, web intelligence, and SDG-focused social innovation analysis.
        """
    )

    usecase = gr.Dropdown(
        choices=["Basic Chatbot", "Chatbot with Web", "AI News"],
        value="Basic Chatbot",
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
        placeholder="Enter your message or web query",
        label="Input",
        visible=True
    )

    frequency = gr.Dropdown(
        choices=["Daily", "Weekly", "Monthly"],
        value="Weekly",
        label="Select Time Frame",
        visible=False
    )

    submit_btn = gr.Button("Run Agent")

    output = gr.Markdown(label="Agent Output")

    usecase.change(
        fn=toggle_inputs,
        inputs=usecase,
        outputs=[user_input, frequency],
    )

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