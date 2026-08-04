* https://docs.livekit.io/agents/
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


6. Features
    - Real-time web search using Firecrawl
    - Supabase database integration via MCP
    - Voice interaction capabilities:
      - Silero VAD (Voice Activity Detection)
      - AssemblyAI Speech-to-Text
      - OpenAI GPT-4 for language processing
      - OpenAI TTS for text-to-speech
