import os
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START, add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import TavilySearchAPIWrapper
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_postgres import PostgresChatMessageHistory

# Load environment variables
load_dotenv()

# --- Environment Variables ---
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

# --- Model Setup ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GOOGLE_API_KEY)

# --- Create tmp dir for reports ---
cwd = Path(__file__).parent.resolve()
tmp = cwd.joinpath("tmp")
tmp.mkdir(exist_ok=True, parents=True)

today = datetime.now().strftime("%Y-%m-%d")

# --- PostgreSQL Memory Setup ---
# This stores chat history persistently in PostgreSQL
message_history = PostgresChatMessageHistory(
    connection_string=DATABASE_URL,
    session_id="arxiv_research_agent"
)

# --- Tavily Search Setup ---
tavily = TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY)

# --- Define Tools ---

@tool("search_arxiv", return_direct=True)
def search_arxiv_tool(query: str) -> str:
    """
    Search for research papers on arXiv related to a given topic.
    Returns a formatted summary with titles, URLs, and snippets.
    """
    search_query = f"arXiv research papers {query} latest developments academic research"
    results = tavily.run(search_query)

    if not results:
        return f"No results found for '{query}'. Try a broader term."

    text = f"## arXiv Research Papers for: {query}\n\n"
    for i, r in enumerate(results[:5], 1):
        title = r.get("title", "Untitled")
        url = r.get("url", "")
        snippet = r.get("content", "")[:300]
        text += f"**{i}. {title}**\n\n{snippet}\n\n🔗 {url}\n\n"
    text += "---\n*Search performed using Tavily academic engine.*"
    return text


@tool("recall_memory", return_direct=True)
def recall_memory_tool(query: str) -> str:
    """
    Search and summarize relevant past research sessions from Postgres memory.
    """
    messages = message_history.messages
    relevant_msgs = [m.content for m in messages if query.lower() in m.content.lower()]

    if not relevant_msgs:
        return f"No prior research found related to '{query}'."
    
    summary = f"### Found {len(relevant_msgs)} previous discussions about '{query}':\n\n"
    for i, msg in enumerate(relevant_msgs[-5:], 1):
        summary += f"{i}. {msg[:250]}...\n\n"
    return summary


# --- Define LangGraph State ---
class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    query: str


# --- Define Nodes ---
async def researcher_node(state: ResearchState):
    """
    The main research agent — queries memory and performs new arXiv research.
    """
    user_query = state["query"]
    memory_results = recall_memory_tool(user_query)
    arxiv_results = search_arxiv_tool(user_query)

    prompt = dedent(f"""
    You are Professor X-1000, an AI research assistant with persistent memory.

    The user asked: {user_query}

    You previously found:
    {memory_results}

    New research papers from arXiv:
    {arxiv_results}

    Based on both, generate a structured academic report:
    - Summary of findings
    - Key papers
    - Implications and future work
    """).strip()

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    message_history.add_message(AIMessage(content=response.content))
    return {"messages": [AIMessage(content=response.content)], "query": user_query}


# --- Define Graph ---
graph = StateGraph(ResearchState)
graph.add_node("researcher", researcher_node)
graph.add_edge(START, "researcher")
graph.add_edge("researcher", END)

# Compile graph into a runnable
research_graph = graph.compile()


# --- Run Example ---
if __name__ == "__main__":
    import asyncio

    async def main():
        print("LangGraph Researcher Agent Started\n")
        user_topic = input("Enter your research topic: ")
        result = await research_graph.ainvoke({"messages": [], "query": user_topic})
        print("\n=== AI Research Report ===\n")
        print(result["messages"][-1].content)
        print("\nSaved to PostgreSQL memory.")

    asyncio.run(main())
