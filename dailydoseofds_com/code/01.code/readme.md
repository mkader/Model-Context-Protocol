<img height="50%" width="50%" src="https://private-user-images.githubusercontent.com/3132680/628243257-6342f5a8-ba62-483c-bcb0-482fc98075c0.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODUzODAwOTIsIm5iZiI6MTc4NTM3OTc5MiwicGF0aCI6Ii8zMTMyNjgwLzYyODI0MzI1Ny02MzQyZjVhOC1iYTYyLTQ4M2MtYmNiMC00ODJmYzk4MDc1YzAucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDczMCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA3MzBUMDI0OTUyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9OWNhMmRiNzM3YmU5YmVkNDU1YjU1N2JlNjQ5ODVlYjBmYjZiN2ZlZTk4ZjMxNjY5YTA1ZmE5Zjg5ZTcyNzliMSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.T-V5ynviFbXGELmAqfZEmEpslE2GSxXiYGjLN6tMKKw">

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
