
* building-financial-analyst-azure-openai.ipynb - very fast, it can be done 14s, compare to local deepstack-r1 it take minimum 1 hr

1. compile
python -m py_compile server.py finance_crew.py

2. install dependency
python -m pip install -r requirements.txt

3. Download model
ollama run deepseek-r1

4. Run the project, set up your MCP server : Cursor settings -> MCP -> add new global MCP server -> JSON file

```
{
    "mcpServers": {
        "financial-analyst": {
         "command": "uv",
            "args": [
                "--directory",
                "absolute/path/to/project_root",
                "run",
                "server.py"
            ]
        }
    }
}
```

- Cursor MCP settings -> toggle the button to connect the server to the host.

- chat with Cursor and analyze stock market data. 
- Simply provide the stock symbol and timeframe you want to analyze, and watch the magic unfold.

- Example queries:
    - "Show me Tesla's stock performance over the last 3 months"
    - "Compare Apple and Microsoft stocks for the past year"
    - "Analyze the trading volume of Amazon stock for the last month"

7. OR you can do it through VSC, start server

    ``` 
    {
        "servers": {
           "mcp-finance-app": {
                "type": "stdio",
                "command": "C:/mcp/.venv/Scripts/python.exe",
                "args": ["C:/mcp/usecase_03/server.py"]
		    }
        },
        "inputs": []
    }
    ```
    - Please call mcp-rag-app with query "Plot YTD stock gain of Tesla""

```mermaid
sequenceDiagram
    autonumber
    actor U as User / MCP Client
    participant S as server.py (FastMCP)
    participant F as finance_crew_openai.py
    participant C as CrewAI Crew (sequential)
    participant A1 as Agent 1: Stock Data Analyst
    participant A2 as Agent 2: Senior Python Developer
    participant A3 as Agent 3: Senior Code Execution Expert
    participant L as OpenAI-compatible Endpoint

    U->>S: call tool analyze_stock(query)
    activate S
    Note over S: Create StringIO buffers<br/>redirect stdout/stderr

    S->>F: await run_financial_analysis_async(query)
    activate F
    F->>C: await crew.kickoff_async(inputs={"query": query})
    activate C

    C->>A1: Execute query_parsing_task
    A1->>L: LLM call (parse symbol/timeframe/action)
    L-->>A1: Parsed query structure
    A1-->>C: Task 1 output

    C->>A2: Execute code_writer_task
    A2->>L: LLM call (generate stock analysis script)
    L-->>A2: Python code/script
    A2-->>C: Task 2 output

    C->>A3: Execute code_execution_task
    A3->>L: LLM call (review/fix/execute guidance)
    L-->>A3: Final executable result
    A3-->>C: Task 3 output

    C-->>F: result.raw
    deactivate C
    F-->>S: result string
    deactivate F

    S-->>U: tool response (string)

    alt Exception anywhere in flow
        S-->>U: "Error: <exception message>"
    end
    deactivate S
```
