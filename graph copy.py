from langgraph.graph import StateGraph, START, END
from state import State
from llm import invoke_llm_stream, classify_query
from webscraper import scrape_website
from pineconeagent import query_pinecone

def chatbot(state: State):
    """Handles general chatbot responses."""
    return {"messages": invoke_llm_stream(state["messages"])}

def web_scraper(state: State):
    """Handles website scraping responses."""
    return  {"messages":scrape_website(state["messages"][-1])}  # No argument needed
    # {"messages": [{"role": "system", "content": scraped_content}]}

def determine_query_type(state: State):
    """Uses LLM to determine if the query is 'chat' or 'vector'."""
    query_type = classify_query(state["messages"][-1].content)
    return query_type

def build_chat_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    # graph_builder.add_node("web_scraper", web_scraper)
    graph_builder.add_node("vector", query_pinecone)

    graph_builder.add_conditional_edges(
        START,
        lambda state: "chatbot" if determine_query_type(state) == "chat" else "vector"
    )

    graph_builder.add_edge("chatbot", END)
    graph_builder.add_edge("vector", END)
    # graph_builder.add_edge("web_scraper", END)

    return graph_builder.compile()

chat_graph = build_chat_graph()

# __all__ = ["graph"]