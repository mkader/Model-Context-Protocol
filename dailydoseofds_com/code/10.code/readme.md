```
1. Install uv

# MacOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

2. create env
uv init project-name
cd project-name

# Create virtual environment and activate it
uv venv
source .venv/bin/activate  # MacOS/Linux

.venv\Scripts\activate     # Windows

3. Install dependencies
uv sync

4. .env
RAGIE_API_KEY=your_ragie_api_key

5. Run the project -> Cursor settings -> seleect MCP Tools -> Add new global MCP server - json
{
    "mcpServers": {
        "ragie": {
            "command": "uv",
            "args": [
                "--directory",
                "/absolute/path/to/project_root",
                "run",
                "server.py"
            ],
            "env": {
                "RAGIE_API_KEY": "YOUR_RAGIE_API_KEY"
            }
        }
    }
}
```

<img width="242" height="306" alt="image" src="https://github.com/user-attachments/assets/85202308-9c6e-4fb7-a155-133c0a7b80c6" />

<img width="702" height="417" alt="image" src="https://github.com/user-attachments/assets/d7b5e76b-9e67-4ee2-8a6a-9db899b2e640" />

<img width="687" height="402" alt="image" src="https://github.com/user-attachments/assets/e6fd591d-c965-492c-9991-52e70efd17fb" />

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant UI as Streamlit UI
    participant APP as app.py
    participant SS as st.session_state
    participant AAI as AssemblyAI API

    U->>UI: Open app
    UI->>APP: Run main()
    APP->>SS: Initialize session state (id, file_cache)
    APP-->>U: Show welcome screen + uploader

    U->>UI: Upload audio file
    UI->>APP: audio_file available

    alt No file uploaded
        APP-->>U: Show onboarding content
    else File uploaded
        APP-->>U: Show file preview/details
        APP->>AAI: transcribe(audio_file, TranscriptionConfig)
        AAI-->>APP: transcript (text, summary, speakers, sentiment, topics)
        APP->>SS: Store transcriber + transcript
        APP-->>U: Show tabs (Transcription/Summary/Speakers/Sentiment/Topics/Chat)

        U->>UI: Open a tab
        UI->>APP: Render selected tab
        APP-->>U: Display analysis data

        loop Q&A Chat
            U->>UI: Enter question
            UI->>APP: st.chat_input(prompt)
            APP->>SS: Append user message
            APP->>AAI: transcript.lemur.task(full_prompt)
            AAI-->>APP: assistant response
            APP->>SS: Append assistant message
            APP-->>U: Render chat response
        end
    end
```


