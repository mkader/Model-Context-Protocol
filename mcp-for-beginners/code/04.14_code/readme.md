* install frontend and backend dependencies: ``` npm install ```
* Verify the backend compiles by running ``` npx tsc --noEmit ```
* Run backend
* Windows MCP -  uses `concurrently` library to run that you need to find a replacement for- *package.json*
```
"start": "concurrently \"cross-env NODE_ENV=development INPUT=mcp-app.html vite build --watch\" \"tsx watch main.ts\""
```

* Start backend - it start the backend on `http://localhost:3001/mcp`. 
npm start
    - Choice -1 Test the app in Visual Studio Code - mcp.json
    ```
    {
        "servers": {
            "my-mcp-server-7178eca7": {
                "url": "http://localhost:3001/mcp",
                "type": "http"
            }
        },
        "inputs": []
    }
   Make sure a chat window is open and type `get-faq`, you should see a result like so:
   ```
    - Choice -2- Test the app with a host
        - The repo <https://github.com/modelcontextprotocol/ext-apps> contains several different hosts that you can use to test your MVP Apps. 
```
  # Local machine
    - Navigate to *ext-apps* after you've cloned the repo.
    - Install dependencies:     npm install
  
  - In a separate terminal window, navigate to *ext-apps/examples/basic-host*
  - Run the host: npm start
      This should connect the host with backend and you should see the app running like so:
```
      
  <img width="402" height="440" alt="image" src="https://github.com/user-attachments/assets/354499ee-5f05-4d9d-a3d1-80cccf6b7d21" />

