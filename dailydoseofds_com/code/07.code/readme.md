* create bucket get bucket id, pass it code
    <img width="1827" height="892" alt="image" src="https://github.com/user-attachments/assets/ab826c53-eb9c-4ebd-9f1f-33a1ef2b1ece" />

    <img width="537" height="272" alt="image" src="https://github.com/user-attachments/assets/48775e43-3848-43b2-9346-88e02ef30861" />

* Install
  ```
  usecase_07> uv sync
  usecase_07> python -m pip install -e .
  
  # usecase_07/.venv folder in local project fodler
  python -m venv .venv
  venv\Scripts\activate
  pip install "mcp[cli]"
  ```
* .env - GROUNDX_AI_API_KEY=aasdasdasdasdase

* mcp.json
  ```
  		"usecase_07_mcp_app": {
			"type": "stdio",
			"command": "C:/usecase_07/.venv/Scripts/python.exe",
			"args": ["C:/usecase_07/server.py"]
		},
  ```

     <img width="507" height="112" alt="image" src="https://github.com/user-attachments/assets/bcf62a26-54f0-4883-968d-687e1a8c1a73" />

    <img width="456" height="327" alt="image" src="https://github.com/user-attachments/assets/16ecf19d-f68c-4b35-bd2a-222e4fd8cc72" />

    <img width="541" height="398" alt="image" src="https://github.com/user-attachments/assets/cabac332-1071-4237-a441-ac2b76a07d20" />

    <img width="462" height="933" alt="image" src="https://github.com/user-attachments/assets/51c6f1ce-657c-4542-a4d9-8b303907d59f" />
    

* mcp tool run ``` npx @modelcontextprotocol/inspector@latest  mcp run server.py  ```

* New MCP Server
  - Server
    <img width="1882" height="920" alt="image" src="https://github.com/user-attachments/assets/657eae1e-c5c0-4e81-b6d2-547a46983f33" />

  - Tools

    <img width="1163" height="477" alt="image" src="https://github.com/user-attachments/assets/be2d4353-0bb4-480b-8216-9a6af7d3d9be" />
    <img width="1285" height="468" alt="image" src="https://github.com/user-attachments/assets/effa1c81-3eb8-4dd0-aba3-2dbb31e0cf19" />

  - Prompts
    
    <img width="1211" height="350" alt="image" src="https://github.com/user-attachments/assets/e055e311-1f1b-4a5d-9016-a5d6ac815ec6" />

  - Resources
    
      <img width="1157" height="450" alt="image" src="https://github.com/user-attachments/assets/b8e6087c-a017-4cc0-aec1-c16283023870" />

* Ingest file
  
    <img width="948" height="391" alt="image" src="https://github.com/user-attachments/assets/219b8acb-3439-4323-840a-71554d21a874" />

    <img width="1292" height="361" alt="image" src="https://github.com/user-attachments/assets/dbf66c7e-7198-41ee-9551-89e720b36f92" />

* search
  
    <img width="443" height="343" alt="image" src="https://github.com/user-attachments/assets/8942208f-c219-4f64-8d24-e0e38108a251" />

    <img width="1332" height="522" alt="image" src="https://github.com/user-attachments/assets/c9a1f3e8-1fd3-4258-8386-4c88bbf4b0eb" />

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant C as Copilot
    participant M as usecase_07_mcp_app
    participant G as GroundX
    participant B as Bucket 31823

    U->>C: Send deepstack.pdf and ask for summary
    C->>M: ingest_documents(local_file_path=".../deepstack.pdf")
    M->>G: ingest(Document(bucket_id=31823, file_type="pdf"))
    G->>B: Store and index PDF
    G-->>M: Ingestion accepted
    M-->>C: "Document ingested (available shortly)"

    C->>M: search_doc_for_rag_context(query="Unsuccessful attempts summary")
    M->>G: search.content(id=31823, n=10, query)
    G-->>M: Top matching excerpts
    M-->>C: Retrieved context text

    C->>C: Extract failed approaches and reasons
    C-->>U: Short summary result
```

