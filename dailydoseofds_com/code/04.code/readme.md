* https://docs.livekit.io/agents/
* https://lab.anam.ai/api-keys - avatar
1. install ``` python -m pip install -r requirements.txt ```
2. Implementation: agent.py - This implementation uses AssemblyAI's services for speech-to-text, along with Firecrawl for web search and Supabase for database operations.
  - Requirements
      - Firecrawl API key
      - Supabase access token
      - OpenAI API key
      - AssemblyAI API key
      - LiveKit credentials

3. `.env` and configure the following environment variables:
  ```
  FIRECRAWL_API_KEY=your_firecrawl_api_key
  SUPABASE_ACCESS_TOKEN=your_supabase_token
  OPENAI_API_KEY=your_openai_api_key
  ASSEMBLYAI_API_KEY=your_assemblyai_api_key
  LIVEKIT_URL=your_livekit_url
  LIVEKIT_API_KEY=your_livekit_api_key
  LIVEKIT_API_SECRET=your_livekit_api_secret
  ```

  <img width="1023" height="357" alt="image" src="https://github.com/user-attachments/assets/a7ffcc8b-2f54-4df1-951d-45947a861c8a" />

4. Running
    - ``` python agent.py console``` - speak through vsc.
    - The agent will:
      1. Connect to LiveKit
      2. Initialize the MCP server for Supabase integration
      3. Set up voice interaction capabilities
      4. Start listening for user input

    <img width="1251" height="690" alt="image" src="https://github.com/user-attachments/assets/be74dd75-bf4c-41db-9dc0-c3b0c843bbec" />

    - inference quota exceeded, use openai llm

     <img width="1262" height="458" alt="image" src="https://github.com/user-attachments/assets/a31aaaa3-9ffa-474e-8e5d-a31561383978" />

6. Features
    - Real-time web search using Firecrawl
    - Supabase database integration via MCP
    - Voice interaction capabilities:
      - Silero VAD (Voice Activity Detection)
      - AssemblyAI Speech-to-Text
      - OpenAI GPT-4 for language processing
      - OpenAI TTS for text-to-speech
     
* Difference between assemblyai & inference
  - Short answer: they use different backends and billing paths.
  - assemblyai.STT(...)
      - Sends audio directly to AssemblyAI.
      - You pay/use your AssemblyAI account and API key.
      - You get AssemblyAI-specific features and params (like keyterms_prompt).
      - Behavior, accuracy tuning, and limits follow AssemblyAI.
  - inference.STT(model="deepgram/nova-3", language="multi")
      - Sends audio through LiveKit Inference, which routes to the provider model (here Deepgram Nova-3).
      - You use LiveKit Inference quota/billing (not direct provider credentials in this call style).
      - Easier unified setup across providers, but you can hit LiveKit Inference quota/rate limits.
      - Provider-specific knobs may be less direct than using provider SDK/plugin directly.

```mermaid     
sequenceDiagram
    autonumber
    participant U as User
    participant LK as LiveKit Room
    participant A as AgentSession
    participant STT as Azure OpenAI STT
    participant LLM as Azure OpenAI LLM
    participant MCP as Supabase MCP Server
    participant TTS as Azure OpenAI TTS
    participant AV as Anam Avatar

    Note over A,AV: Avatar starts before session.start when configured

    U->>LK: Join room and speak
    LK->>A: Audio input stream
    A->>STT: Transcribe audio
    STT-->>A: User text

    A->>LLM: Send user text + instructions
    alt LLM decides tool call
        LLM-->>A: Tool request
        A->>MCP: Execute tool (e.g., list_projects)
        MCP-->>A: Tool result
        A->>LLM: Tool result context
        LLM-->>A: Final response text
    else No tool needed
        LLM-->>A: Direct response text
    end

    A->>TTS: Synthesize reply audio
    TTS-->>A: Audio chunks
    A-->>LK: Publish assistant audio
    AV-->>LK: Publish lip-synced avatar video/audio

    LK-->>U: User hears reply and sees avatar speaking
```
