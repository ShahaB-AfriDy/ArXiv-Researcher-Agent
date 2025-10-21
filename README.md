---

# ArXiv Researcher Agent

An advanced **AI-powered research assistant** built using **LangGraph**, **LangChain**, **FastAPI**, and **PostgreSQL (pgvector)** for persistent memory.
This system demonstrates how to build intelligent research agents capable of exploring academic papers on **arXiv**, remembering prior findings, and building upon past research sessions.

---

## Overview

The **ArXiv Researcher Agent** provides a complete workflow for intelligent research automation and memory-augmented reasoning.
It can perform academic literature searches, analyze findings, and store contextual information persistently using **pgvector memory embeddings**.

With **LangGraph**, all research and memory interactions are modeled as a **state graph**, allowing structured agent coordination, reproducible research chains, and long-term contextual understanding.

---

## Screenshots

### Research Chat Interface

![Research Chat Interface](assets/images/research-chat-interface.png)

### Memory Chat Interface

![Memory Chat Interface](assets/images/memory-chat-interface.png)

---

## Key Features

### 1. Research Agent

* Performs advanced research queries using **arXiv** and scholarly sources
* Generates structured **research summaries, analyses, and reports**
* Integrates memory to recall prior research sessions and context
* Provides **fact-checked**, citation-based responses

### 2. Memory Assistant Agent

* Retrieves, summarizes, and organizes previous research sessions
* Allows **topic-based and chronological recall**
* Helps users identify links between previous research areas

### 3. Persistent Memory with PostgreSQL (pgvector)

* Uses **pgvector** for storing and retrieving research embeddings
* Supports **semantic search** and long-term memory recall
* Scalable database solution for academic research archives

### 4. LangGraph Integration

* Manages the workflow as a **stateful graph of agents**
* Enables advanced reasoning, message routing, and workflow control
* Supports **persistent session states** across user interactions

### 5. FastAPI Backend

* Provides API endpoints for research and memory operations
* Manages model calls, Tavily integration, and data persistence
* Serves as the main communication layer for frontends

### 6. Dual Frontend Interfaces

* **Streamlit UI:** Simplified research interface for local experimentation
* **Next.js UI:** Modern web dashboard for scalable deployments

---

## Technologies Used

* **LangGraph** – Agent workflow orchestration
* **LangChain** – LLM integration and prompt tooling
* **PostgreSQL + pgvector** – Persistent memory and vector search
* **FastAPI** – Backend API service for research and memory
* **Streamlit** – Quick frontend for research interactions
* **Next.js** – Web-based production-ready UI
* **Tavily API** – Academic and arXiv paper search integration
* **Python (asyncio, dotenv, pydantic)** – Backend core stack

---

## Project Structure

```
Arxiv Researcher Agent
├───APIs
│   └─── ... (FastAPI endpoints)
│
├───assets
│   └───images
│
├───backend
│   ├───core
│   │   ├── researcher.py
│   │   └── memory_manager.py
│   │   └── main_graph.py
│   └───utils
│   │    └── config.py
│   │    └── db.py
│   ├─────main.py
│
└───frontend
    ├───next.js-ui
    │   └─── ... (Next.js web dashboard)
    └───streamlit-ui
        └─── ... (Streamlit demo interface)
```

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShahaB-AfriDy/ArXiv-Researcher-Agent.git
cd arxiv-researcher-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following keys:

```
NEBIUS_API_KEY="your-nebius-api-key"
TAVILY_API_KEY="your-tavily-api-key"
POSTGRES_URL="postgresql+psycopg://user:password@localhost:5432/research_db"
EXAMPLE_MODEL_NAME="moonshotai/Kimi-K2-Instruct"
EXAMPLE_BASE_URL="https://api.studio.nebius.ai/v1"
```

### 5. Run the Backend (FastAPI)

```bash
uvicorn APIs.main:app --reload
```

### 6. Run the Streamlit Frontend

```bash
streamlit run frontend/streamlit-ui/app.py
```

Or run the **Next.js frontend**:

```bash
cd frontend/next.js-ui
npm install
npm run dev
```

---

## Usage

### Research Mode

* Input a topic, for example:
  `Research the latest breakthroughs in quantum computing`
* The agent will:

  1. Search prior memory for related research
  2. Fetch new academic papers from arXiv
  3. Generate a structured report
  4. Store session findings persistently in PostgreSQL

### Memory Mode

* Query past work, such as:
  `Summarize my research on reinforcement learning`
* The memory agent will:

  * Retrieve stored sessions
  * Summarize key findings
  * Highlight links and research progress over time

---

## Future Enhancements

* Cross-domain multi-agent collaboration
* Visual knowledge graphs for memory connections
* Integration with Google Scholar and Semantic Scholar APIs
* Support for citation management and auto-bibliography

---

## Author

**Shahab Afridi**
AI Research Engineer | Developer of Intelligent Agent Systems

* **Email:** [shahabafridy@gmail.com](mailto:shahabafridy@gmail.com)
* **LinkedIn:** [https://www.linkedin.com/in/shahab-afridy-9ba965286/](https://www.linkedin.com/in/shahab-afridy-9ba965286/)

---