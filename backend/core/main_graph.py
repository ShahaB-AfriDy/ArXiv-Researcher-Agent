"""
main_graph.py
----------------

Defines the LangGraph pipeline for the ArXiv Researcher Agent.

It orchestrates two main agents:
1. Research Agent — performs arXiv searches and generates reports.
2. Memory Agent — retrieves and summarizes stored research sessions.

Each node represents a function call or reasoning step in the workflow.
"""

import asyncio
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from backend.core.researcher import Researcher

# -------------------------------------
# Define the State for the Graph
# -------------------------------------
class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    query: str
    result: str


# -------------------------------------
# Initialize Agents and Graph
# -------------------------------------
researcher = Researcher()
research_agent, memory_agent = researcher.define_agents()

# -------------------------------------
# Define Nodes (each represents a reasoning step)
# -------------------------------------
async def start_node(state: ResearchState):
    print("[Graph] Starting new research process...")
    return {**state, "messages": state.get("messages", []) + ["Research started."]}


async def memory_node(state: ResearchState):
    """Memory node — checks prior research memory."""
    print("[Graph] Searching memory for previous related work...")
    query = state["query"]
    memory_agent_instance = researcher.get_memory_agent()
    result = await researcher.run_agent_with_memory(memory_agent_instance, f"Find past research about {query}")
    return {**state, "messages": state["messages"] + [result.final_output]}


async def research_node(state: ResearchState):
    """Research node — runs arXiv and report generation."""
    print("[Graph] Running main research agent...")
    query = state["query"]
    research_agent_instance = researcher.get_research_agent()
    result = await researcher.run_agent_with_memory(research_agent_instance, f"Research {query}")
    return {**state, "result": result.final_output, "messages": state["messages"] + [result.final_output]}


async def end_node(state: ResearchState):
    print("[Graph] Research process completed.")
    return {**state, "messages": state["messages"] + ["Process completed."]}


# -------------------------------------
# Build the LangGraph Workflow
# -------------------------------------
graph = StateGraph(ResearchState)

graph.add_node("start", start_node)
graph.add_node("memory_search", memory_node)
graph.add_node("research_execution", research_node)
graph.add_node("end", end_node)

graph.add_edge(START, "start")
graph.add_edge("start", "memory_search")
graph.add_edge("memory_search", "research_execution")
graph.add_edge("research_execution", "end")
graph.add_edge("end", END)

workflow = graph.compile()


# -------------------------------------
# Utility function for running the workflow
# -------------------------------------
async def run_research_workflow(query: str):
    """Run the full research pipeline asynchronously."""
    print(f"[Workflow] Starting research workflow for: {query}")
    initial_state = {"query": query, "messages": [], "result": ""}
    result = await workflow.ainvoke(initial_state)
    print(f"[Workflow] Completed for: {query}")
    return result


if __name__ == "__main__":
    asyncio.run(run_research_workflow("Recent advances in quantum computing"))
