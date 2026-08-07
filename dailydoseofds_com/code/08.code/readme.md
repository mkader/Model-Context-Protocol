usecase_08> uv sync
usecase_08> python -m pip install -e .

# usecase_08/.venv folder in local project fodler
python -m venv .venv
.venv\Scripts\activate
pip install "mcp[cli]"


mcp.json
		"usecase_08_sdv_mcp": {
			"type": "stdio",
			"command": "C:/usecase_08/.venv/Scripts/python.exe",
			"args": ["C:/usecase_08/server.py"]
    	}
      
npx @modelcontextprotocol/inspector@latest  mcp run server.py 

<img width="450" height="623" alt="image" src="https://github.com/user-attachments/assets/e32391f0-04da-43e4-b515-647c95cf5b5d" />
