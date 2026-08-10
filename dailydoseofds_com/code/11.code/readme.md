```
cd usecase_11

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# MacOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

.env
ASSEMBLYAI_API_KEY=your_assemblyai_api_key

1. Run as a Streamlit App (Interactive UI)
streamlit run app.py

2. Run as an MCP Server (for Cursor/Agent Integration)
{
    "mcpServers": {
        "assemblyai": {
            "command": "python",
            "args": [
                "server.py"
            ],
            "env": {
                "ASSEMBLYAI_API_KEY": "YOUR_ASSEMBLYAI_API_KEY"
            }
        }
    }
}
```
```mermaid
sequenceDiagram
    autonumber
    actor C as MCP Client
    participant S as server.py (FastMCP)
    participant ENV as .env / OS Env
    participant AAI as AssemblyAI API
    participant T as Global transcript

    Note over S,ENV: Startup
    S->>ENV: load_dotenv()
    S->>ENV: read ASSEMBLYAI_API_KEY
    S->>AAI: set aai.settings.api_key
    S-->>C: MCP tools available (transcribe_audio, get_audio_data)

    C->>S: transcribe_audio(audio_location)
    S->>AAI: Transcriber().transcribe(audio_location, config)
    AAI-->>S: transcript object
    S->>T: store transcript (global)
    S-->>C: return transcript.summary

    C->>S: get_audio_data(flags)
    alt transcript is None
        S-->>C: {"error":"No transcript available..."}
    else transcript exists
        S->>T: read transcript
        opt text=True
            S->>T: get_sentences()
            S-->>C: out.text
        end
        opt timestamps=True
            S->>T: get_sentences() + _format_timestamp()
            S-->>C: out.sentences[]
        end
        opt summary=True
            S->>T: summary
            S-->>C: out.summary
        end
        opt speakers=True
            S->>T: utterances + _format_timestamp()
            S-->>C: out.speakers[]
        end
        opt sentiment=True
            S->>T: sentiment_analysis + counts/details
            S-->>C: out.sentiment
        end
        opt topics=True
            S->>T: iab_categories.summary
            S-->>C: out.topics
        end
        S-->>C: merged output dict
    end
```
