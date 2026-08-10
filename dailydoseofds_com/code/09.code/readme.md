```
ollama pull deepseek-r1:7b 
cd C:\usecase_09 ``

python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install crewai streamlit python-dotenv linkup pydantic

python -m streamlit run app.py

python agents_test.py 

```
```mermaid
sequenceDiagram
    actor User

    box Streamlit UI (app.py)
        participant App as app.py
    end

    box MCP Server (server.py)
        participant MCP as FastMCP Server
    end

    box CrewAI Pipeline (agents.py)
        participant RC as create_research_crew()
        participant WS as Web Searcher Agent
        participant RA as Research Analyst Agent
        participant TW as Technical Writer Agent
    end

    participant LU as LinkUp API
    participant OL as Ollama (deepseek-r1:7b)

    alt Via Streamlit UI
        User->>App: Enter Linkup API Key (sidebar)
        User->>App: Submit research query (chat input)
        App->>App: run_research(query)
    else Via MCP Client
        User->>MCP: crew_research(query)
        MCP->>MCP: run_research(query)
    end

    App->>RC: create_research_crew(query)
    MCP->>RC: create_research_crew(query)

    RC->>RC: Initialize LinkUpSearchTool
    RC->>RC: Init LLM (Ollama/deepseek-r1:7b)
    RC->>RC: Define Agents & Tasks (sequential)
    RC-->>App: crew
    RC-->>MCP: crew

    Note over App,TW: crew.kickoff() — sequential process

    App->>WS: search_task
    MCP->>WS: search_task
    WS->>OL: Generate search query
    OL-->>WS: query string
    WS->>LU: linkup_client.search(query)
    LU-->>WS: raw search results + URLs
    WS-->>RA: raw results (context)

    RA->>OL: Analyze & synthesize results
    OL-->>RA: structured analysis
    opt Fact-check needed
        RA->>WS: delegate verification query
        WS->>LU: linkup_client.search(verification query)
        LU-->>WS: additional results
        WS-->>RA: verified facts
    end
    RA-->>TW: structured analysis + citations (context)

    TW->>OL: Write final markdown response
    OL-->>TW: formatted response with citations

    TW-->>App: result.raw (markdown)
    TW-->>MCP: result.raw (markdown)

    App-->>User: Display response in chat
    MCP-->>User: Return response string
```
