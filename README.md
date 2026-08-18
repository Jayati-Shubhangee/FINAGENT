
# FinAgent — AI-Powered Financial Research Agent

<p align="center">

  <strong>FinAgent</strong>

  AI-powered multi-agent financial research and market intelligence platform built with Agno, Groq, YFinance, DuckDuckGo/DDGS, FastAPI, and a modern web interface.

</p>

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Agno-Multi--Agent-orange" alt="Agno">
  <img src="https://img.shields.io/badge/LLM-Groq-black" alt="Groq">
  <img src="https://img.shields.io/badge/Model-GPT--OSS--120B-purple" alt="GPT OSS">
  <img src="https://img.shields.io/badge/Finance-YFinance-green" alt="YFinance">
  <img src="https://img.shields.io/badge/Web%20Search-DuckDuckGo%20%2F%20DDGS-yellow" alt="DuckDuckGo">
  <img src="https://img.shields.io/badge/API-FastAPI-teal" alt="FastAPI">
  <img src="https://img.shields.io/badge/Container-Docker-blue" alt="Docker">

</p>

---

## Overview

**FinAgent** is a multi-agent AI financial research system designed to combine:

- Real-time financial data
- Analyst recommendations
- Company fundamentals
- Historical market information
- Recent financial news
- LLM-based reasoning and synthesis

Instead of relying on a single general-purpose AI agent, FinAgent uses a **specialized multi-agent architecture** in which different agents are responsible for different categories of financial research.

The system is coordinated by a central **Financial Research Team** powered by **Agno**.

A typical request such as:

> "Summarize analyst recommendations and the latest stock news for NVIDIA (NVDA)."

is decomposed into specialized tasks:

1. The **Finance AI Agent** retrieves financial and analyst data.
2. The **Web Search Agent** retrieves recent financial news.
3. The **Financial Research Team** coordinates the agents.
4. The LLM synthesizes the retrieved information.
5. The final result is returned as a structured financial research report.

---

# Key Features

### Multi-Agent Financial Research

- Specialized agents for financial data and web/news research.
- Centralized coordination using Agno `Team`.
- Task delegation based on the type of user request.
- Final response synthesis by the coordinating agent.

### Financial Data Analysis

Powered by `YFinanceTools` for retrieving:

- Stock prices
- Company information
- Stock fundamentals
- Analyst recommendations
- Company news
- Historical prices

### Web & Financial News Research

Powered by Agno's DuckDuckGo integration backed by DDGS.

The Web Search Agent is responsible for:

- Recent financial news
- Relevant market developments
- News source metadata
- Publication dates
- Source URLs when available

### LLM Reasoning

The system uses:

- **Groq API**
- **`openai/gpt-oss-120b`**

for fast inference and agent coordination.

### API Backend

A FastAPI backend provides a service layer between the frontend and the agentic system.

### Web Interface

The project includes a frontend that communicates with the FastAPI backend instead of directly interacting with the terminal-based agent.

### Containerization

Docker configuration is included to make the application easier to:

- Package
- Run consistently
- Deploy
- Reproduce across environments

---

# Architecture

```text
                         ┌─────────────────────────┐
                         │       USER / UI         │
                         │                         │
                         │   Web Frontend          │
                         └────────────┬────────────┘
                                      │
                                      │ HTTP Request
                                      ▼
                         ┌─────────────────────────┐
                         │       FASTAPI           │
                         │      Backend API        │
                         │                         │
                         │ Request / Response      │
                         │ Handling                │
                         └────────────┬────────────┘
                                      │
                                      ▼
                  ┌─────────────────────────────────────┐
                  │        AGNO FINANCIAL TEAM          │
                  │                                     │
                  │   Financial Research Coordinator    │
                  └──────────────┬───────────┬──────────┘
                                 │           │
                    Delegate     │           │     Delegate
                                 │           │
                                 ▼           ▼
                  ┌──────────────────┐   ┌──────────────────┐
                  │  FINANCE AGENT   │   │  WEB SEARCH      │
                  │                  │   │     AGENT        │
                  │ Financial Data   │   │                  │
                  │ Analyst Data     │   │ Financial News   │
                  │ Fundamentals     │   │ Web Research     │
                  │ Historical Data  │   │ Recent Events    │
                  └────────┬─────────┘   └────────┬─────────┘
                           │                      │
                           ▼                      ▼
                  ┌──────────────────┐   ┌──────────────────┐
                  │    YFINANCE      │   │ DUCKDUCKGO /     │
                  │                  │   │      DDGS        │
                  │ Market Data      │   │                  │
                  │ Company Data     │   │ Web / News Data  │
                  └──────────────────┘   └──────────────────┘
                           │                      │
                           └──────────┬───────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       GROQ LLM          │
                         │                         │
                         │ openai/gpt-oss-120b     │
                         │                         │
                         │ Reasoning + Synthesis   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   STRUCTURED RESPONSE   │
                         │                         │
                         │ Financial Data          │
                         │ News                    │
                         │ Analysis                 │
                         │ Sources                 │
                         └─────────────────────────┘

