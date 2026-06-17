# Autonomous Research Analyst

An end-to-end multi-agent research system that turns one research query into a structured, source-backed report.

The project is ready for API keys, but does not require them to start. Without keys it runs in offline demo mode so the pipeline, API, CLI, and tests still work.

## What It Does

- Plans a research query into goals
- Builds executable tasks
- Searches external sources when keys are available
- Extracts evidence into structured facts
- Verifies source quality and flags contradictions
- Finds missing information
- Generates follow-up queries through a reflection loop
- Writes Markdown, JSON, or PDF-ready text reports

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Add API keys to `.env` when you have them. Tavily search is supported out of the box through `TAVILY_API_KEY`.

## Run The API

```bash
uvicorn autonomous_research_analyst.api:app --reload
```

Then open:

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Run From CLI

```bash
research-analyst "Research quantum computing startups in India"
```

Or:

```bash
python -m autonomous_research_analyst.cli "Research quantum computing startups in India" --format markdown
```

## Environment Variables

All keys are optional until you want live providers:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`
- `TAVILY_API_KEY`
- `SERPER_API_KEY`
- `FIRECRAWL_API_KEY`
- `LANGSMITH_API_KEY`

## Project Structure

```text
autonomous_research_analyst/
  agents/       Planner, search, verifier, gap analysis, writer
  providers/    Search provider adapters
  export/       Report exporters
  api.py        FastAPI app
  cli.py        Command-line interface
  config.py     .env driven settings
  graph.py      Reflection-loop orchestration
  state.py      Shared research state models
tests/
```

## Current Provider Status

Implemented:

- Offline demo search provider
- Tavily search provider

Reserved for later:

- Serper
- Firecrawl
- LLM-backed extraction and writing
- ChromaDB long-term memory
- LangGraph orchestration

