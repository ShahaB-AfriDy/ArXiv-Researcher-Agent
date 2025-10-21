from core.researcher import research_graph

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
