# AI Research Synthesis and Gap Analysis Engine

A production-grade, deterministic, modular, multi-model RAG system orchestrated using LangGraph.

## Features
- **Retrieval**: Fetches research papers from Semantic Scholar API.
- **Scoring**: Ranks papers deterministically using a multi-factor formula.
- **RAG & Analysis**: Uses `sentence-transformers` for local embeddings and OpenAI for structured reasoning.
- **PDF Generation**: Generates comprehensive PDF reports with `reportlab`.
- **Backend & Frontend**: Async FastAPI REST API and a Streamlit UI.
- **Deployment**: Fully containerized with `docker-compose`.

## Setup and Run

1. Copy `.env.example` to `.env` and configure your API keys:
   ```bash
   cp .env.example .env
   ```
   Add your `OPENAI_API_KEY` to the `.env` file.

2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - Frontend (Streamlit): [http://localhost:8501](http://localhost:8501)
   - Backend API Docs (FastAPI): [http://localhost:8000/docs](http://localhost:8000/docs)

## Architecture
The system uses LangGraph for orchestration. The workflow state machine executes sequentially through:
1. `planner_node`: Structures the query execution plan.
2. `retrieve_node`: Fetches papers asynchronously.
3. `score_node`: Computes similarity, citation, recency, and LLM novelty scores.
4. `select_top_node`: Selects the highest-scoring paper.
5. `summarize_best_node`: Generates a focused summary for the best paper.
6. `summarize_combined_node`: Synthesizes across all papers.
7. `gap_node`: Extracts global research gaps.
8. `pdf_node`: Generated report outputs as PDFs.
9. `finalize_node`: Finalizes execution and JSON reproducible report.