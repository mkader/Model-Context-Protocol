1. Get BrightData API Key -  brightdata.com -> create a new "SERP API" -> Store it in the .env file.

2. compile ``` python -m py_compile server.py rag_code.py ```

3. install dependency ``` python -m pip install -r requirements.txt ```

4. start a Qdrant docker container
   ```bash
   docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

   docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v "${PWD}/qdrant_storage:/qdrant/storage" qdrant/qdrant
   ```

5. Run Project  - go to the notebook.ipynb file, run the code to create a collection in your vector database.

6. Finally, set up your local MCP server as follows : Go to Cursor IDE settings -> Select MCP -> Add new global MCP server -> add this:
    ```json
    {
    "mcpServers": {
        "mcp-rag-app": {
            "command": "python",
            "args": ["/absolute/path/to/server.py"],
            "host": "127.0.0.1",
            "port": 8080,
            "timeout": 30000
        }
    }
    }
    ```

7. OR you can do it through VSC, start server

    ``` 
    {
        "servers": {
            "mcp-rag-app": {
                "type": "stdio",
                "command": "C:/mcp/.venv/Scripts/python.exe",
                "args": ["C:/mcp/usecase_02/server.py"]
            }
        },
        "inputs": []
    }
    ```
    - Please call mcp-rag-app with query "How do I prevent overfitting?"
    - Please call mcp-rag-app with query "Latest weather in Chennai"

    ![](chat_prompt.png)

7. now interact with your vector database and fallback to web search if needed.
    
    ![alt text](server_log.png)

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant C as Chat Client (VS Code Copilot)
    participant M as MCP Runtime
    participant S as mcp-rag-app (server.py)
    participant R as Router Logic
    participant T1 as machine_learning_faq_retrieval_tool
    participant E as EmbedData
    participant V as Retriever + QdrantVDB
    participant Q as Qdrant (localhost:6333)
    participant T2 as bright_data_web_search_tool
    participant B as Bright Data API
    participant G as Google Search

    U->>C: Ask question
    C->>M: Evaluate available MCP tools
    M->>S: Initialize/handshake (stdio)

    S->>R: Classify query intent

    alt ML-related query
        R->>T1: Call retrieval tool(query)
        T1->>E: Create query embedding
        E-->>T1: query_vector
        T1->>V: search(query_vector)
        V->>Q: query_points(collection=ml_faq_collection, limit=3)
        Q-->>V: top matching points
        V-->>T1: combined context
        T1-->>S: ML context response
        S-->>M: Tool result
        M-->>C: Return grounded answer
    else Non-ML query
        R->>T2: Call web search tool(query)
        T2->>B: POST /request (zone, url, format=raw, data_format=html)
        B->>G: Fetch search results
        G-->>B: Search page/content
        B-->>T2: HTML/raw payload
        T2-->>S: list[str] web context
        S-->>M: Tool result
        M-->>C: Return fallback web answer
    end

    C-->>U: Final response
```