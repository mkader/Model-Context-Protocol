# server.py
from mcp.server.fastmcp import FastMCP
from rag_code import *
import os
import sys

# Create an MCP server
mcp = FastMCP("MCP-RAG-app",
              host="127.0.0.1",
              port=8080)

@mcp.tool()
def machine_learning_faq_retrieval_tool(query: str) -> str:
    """Retrieve the most relevant documents from the machine learning
       FAQ collection. Use this tool when the user asks about ML.

    Input:
        query: str -> The user query to retrieve the most relevant documents

    Output:
        context: str -> most relevant documents retrieved from a vector DB
    """

    # check type of text
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    print(f"[mcp-rag-app] machine_learning_faq_retrieval_tool called: {query}", file=sys.stderr, flush=True)
    
    retriever = Retriever(QdrantVDB("ml_faq_collection"), EmbedData())
    response = retriever.search(query)

    return response


@mcp.tool()
def bright_data_web_search_tool(query: str) -> list[str]:
    """
    Search for information on a given topic using Bright Data.
    Use this tool when the user asks about a specific topic or question 
    that is not related to general machine learning.

    Input:
        query: str -> The user query to search for information

    Output:
        context: list[str] -> list of most relevant web search results
    """
    # check type of text
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    
    import requests
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Bright Data Request API configuration
    api_key = "1234c66d-1234-1234-1234-9741602d1234"
    zone = "mak_serp_api"

    print(f"[mcp-rag-app] bright_data_web_search_tool called: {query}", file=sys.stderr, flush=True)


    formatted_query = "+".join(query.split())
    search_url = f"https://www.google.com/search?q={formatted_query}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "zone": zone,
        "url": search_url,
        "format": "raw",
        "data_format": "html",
    }

    response = requests.post(
        "https://api.brightdata.com/request",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    # Return HTML payload as a single entry to satisfy list[str] return type.
    return [response.text]

if __name__ == "__main__":
    print("[mcp-rag-app] Starting MCP server in stdio mode", file=sys.stderr, flush=True)
    mcp.run()