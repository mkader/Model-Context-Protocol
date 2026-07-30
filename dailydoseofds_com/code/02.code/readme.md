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
   participant NB as Jupyter Notebook
   participant E as EmbedData
   participant V as QdrantVDB
   participant Q as Qdrant (localhost:6333)
   participant S as MCP Server (mcp-rag-app)
   participant C as Chat Client (VS Code Copilot)
   participant M as MCP Runtime
   participant T1 as ML Retrieval Tool
   participant T2 as Web Search Tool
   participant B as Bright Data API
   participant G as Google Search
   Note over U,NB: Phase 1: Notebook setup and data loading
   U->>NB: Run notebook cells
   NB->>NB: Prepare FAQ text chunks
   NB->>E: Generate embeddings for chunks
   E-->>NB: Embedding vectors
   NB->>V: Create collection ml_faq_collection
   V->>Q: create_collection if missing
   Q-->>V: Collection ready
   NB->>V: Ingest vectors + payloads
   V->>Q: upload_collection in batches
   Q-->>V: Data stored
   
   Note over U,S: Phase 2: Start MCP server
   U->>S: Start server process
   S->>M: Register tools and connect
   
   Note over U,C: Phase 3: Ask questions in chat
   U->>C: Ask a question
   C->>M: Decide tool usage
   
   alt ML question
       M->>T1: machine_learning_faq_retrieval_tool(query)
       T1->>E: Embed user query
       E-->>T1: Query vector
       T1->>Q: query_points top-k
       Q-->>T1: Matching FAQ contexts
       T1-->>M: Combined retrieved context
       M-->>C: Grounded answer
   else Non-ML question
       M->>T2: bright_data_web_search_tool(query)
       T2->>B: POST request
       B->>G: Fetch search result page
       G-->>B: HTML results
       B-->>T2: Raw response
       T2-->>M: Web fallback context
       M-->>C: Fallback answer
   end
   
   C-->>U: Final response
```
