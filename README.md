---
title: Agentic AI Social Innovation Intelligence
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.0.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

# Agentic AI News Intelligence System

A production-style Agentic AI application for source-grounded news summarization using LangGraph, LangChain, Tavily Search, FastAPI, Streamlit, and LangSmith.

The system retrieves real-time news using Tavily, orchestrates a multi-step agent workflow with LangGraph, summarizes relevant information, and evaluates response quality using LangSmith tracing and evaluation.

## Key Features

- LangGraph-based agentic workflow orchestration
- Tavily-powered real-time news retrieval
- FastAPI backend for production-style API access
- Streamlit frontend for interactive demo
- LangSmith integration for tracing, debugging, and evaluation
- Source-grounded summarization to reduce hallucination risk
- Modular project structure for testing and future deployment

## Tech Stack

- LangGraph
- LangChain
- Tavily Search
- Groq LLM
- FastAPI
- Streamlit
- LangSmith
- FAISS
- Pytest