* https://www.youtube.com/watch?v=SVACugFX_hM&t=44s
* https://lightning.ai/akshay-ddods

```
1. compile
python -m py_compile server.py client.py

2. install dependency
python -m pip install -r requirements.txt

3. Download mode
ollama run llama3.2

python server.py --server_type=sse &

python client.py # Ollama(model="llama3.2"

python client_openai.py # azure open ai model
```

* Debug F5 each file (server.py and client.py) - .vscode/launch.json for debugging purpose

<img width="738" height="722" alt="image" src="https://github.com/user-attachments/assets/a376d6ad-99d0-4f6a-8718-1a1f56577a84" />
