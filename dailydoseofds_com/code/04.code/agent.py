"""
MCP voice agent that routes queries either to Firecrawl web search or to Supabase via MCP.
"""

from __future__ import annotations

import asyncio
import copy
import json
import logging
import os
from typing import Any, Callable, List, Optional

import inspect
from dotenv import load_dotenv
from firecrawl import FirecrawlApp, V1ScrapeOptions
#from pydantic_ai.mcp import MCPServerStdio

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    mcp,
    cli,
    inference,
    function_tool,
)

from livekit.plugins import assemblyai, openai, silero

# ------------------------------------------------------------------------------
# Configuration & Logging
# ------------------------------------------------------------------------------
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
SUPABASE_TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN")

if not FIRECRAWL_API_KEY:
    logger.error("FIRECRAWL_API_KEY is not set in environment.")
    raise EnvironmentError("Please set FIRECRAWL_API_KEY env var.")

if not SUPABASE_TOKEN:
    logger.error("SUPABASE_ACCESS_TOKEN is not set in environment.")
    raise EnvironmentError("Please set SUPABASE_ACCESS_TOKEN env var.")

firecrawl_app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)


def _py_type(schema: dict) -> Any:
    """Convert JSON schema types into Python typing annotations."""
    t = schema.get("type")
    mapping = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "object": dict,
    }

    if isinstance(t, list):
        if "array" in t:
            return List[_py_type(schema.get("items", {}))]
        t = t[0]

    if isinstance(t, str) and t in mapping:
        return mapping[t]
    if t == "array":
        return List[_py_type(schema.get("items", {}))]

    return Any


def schema_to_google_docstring(description: str, schema: dict) -> str:
    """
    Generate a Google-style docstring section from a JSON schema.
    """
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    lines = [description or "", "Args:"]

    for name, prop in props.items():
        t = prop.get("type", "Any")
        if isinstance(t, list):
            if "array" in t:
                subtype = prop.get("items", {}).get("type", "Any")
                py_type = f"List[{subtype.capitalize()}]"
            else:
                py_type = t[0].capitalize()
        elif t == "array":
            subtype = prop.get("items", {}).get("type", "Any")
            py_type = f"List[{subtype.capitalize()}]"
        else:
            py_type = t.capitalize()

        if name not in required:
            py_type = f"Optional[{py_type}]"

        desc = prop.get("description", "")
        lines.append(f"    {name} ({py_type}): {desc}")

    return "\n".join(lines)


@function_tool
async def firecrawl_search(
    context: RunContext,
    query: str,
    limit: int = 2 #number pages to crawl
) -> List[str]:
    """
    Search the web via Firecrawl.

    Args:
        context (RunContext): LiveKit runtime context.
        query (str): Search query string.
        limit (int): Maximum pages to crawl.

    Returns:
        List[str]: Raw page contents.
    """
    url = f"https://www.google.com/search?q={query}"
    logger.debug("Starting Firecrawl for URL: %s (limit=%d)", url, limit)

    loop = asyncio.get_event_loop()
    try:
        crawl_job = await loop.run_in_executor(
            None,
            lambda: firecrawl_app.crawl_url(
                url,
                limit=limit,
                scrape_options={
                    'formats': ['html','markdown']
                }
            )
        )
        
        data = crawl_job.data if hasattr(crawl_job, "data") and crawl_job.data else []
        logger.info("Firecrawl returned %d pages", len(data))

        return data
    except asyncio.TimeoutError:
        logger.warning("Timeout: The crawl request for %s took too long.", url)
        return []
    except Exception as e:
        logger.error("Firecrawl search failed: %s", e, exc_info=True)
        return []

async def build_livekit_tools(server: mcp.MCPServerStdio) -> List[Callable]:
    """
    Build LiveKit tools from a Supabase MCP server.
    """
    tools: List[Callable] = []
    all_tools = await server.list_tools()
    logger.info("Found %d MCP tools", len(all_tools))

    for td in all_tools:
        tool_name = td.info.name
        logger.info("Building tool proxy for: %s", tool_name)
        if tool_name == "deploy_edge_function":
            logger.warning("Skipping tool %s", tool_name)
            continue

        raw_schema = td.info.raw_schema or {}
        parameters_dict = raw_schema.get("parameters", {})
        
        schema = copy.deepcopy(parameters_dict)
        if tool_name == "list_tables":
            props = schema.setdefault("properties", {})
            props["schemas"] = {
                "type": ["array", "null"],
                "items": {"type": "string"},
                "default": []
            }
            schema["required"] = [r for r in schema.get("required", []) if r != "schemas"]

        props = schema.get("properties", {})
        required = set(schema.get("required", []))

        def make_proxy(
            t_name=tool_name, 
            t_desc=raw_schema.get("description", ""), 
            _props=props, 
            _required=required, 
            _schema=schema
        ) -> Callable:
            
            async def proxy(context: RunContext, **kwargs):
                # Convert None → [] for array params
                for k, v in list(kwargs.items()):
                    p_type = _props.get(k, {}).get("type", "")
                    if (p_type == "array" or (isinstance(p_type, list) and "array" in p_type)) and v is None:
                        kwargs[k] = []

                # Execute call against the server with extracted string name
                response = await server.call_tool(t_name, arguments=kwargs or None)
                if isinstance(response, list):
                    return response
                if hasattr(response, "content") and response.content:
                    text = response.content.text
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return text
                return response

            params = [inspect.Parameter("context", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=RunContext)]
            ann = {"context": RunContext}

            for name, ps in _props.items():
                default = ps.get("default", inspect._empty if name in required else None)
                params.append(inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, annotation=_py_type(ps), default=default))
                ann[name] = _py_type(ps)

            proxy.__signature__ = inspect.Signature(params)
            proxy.__annotations__ = ann
            proxy.__name__ = t_name
            proxy.__doc__ = schema_to_google_docstring(t_desc, _schema)
            return function_tool(proxy)

        tools.append(make_proxy())

    return tools


async def entrypoint(ctx: JobContext) -> None:
    """
    Main entrypoint for the LiveKit agent.
    """
    await ctx.connect()
    server_config = mcp.MCPServerStdio(
        "npx",
        args=[
            "-y", 
            "@supabase/mcp-server-supabase@latest", 
            "--access-token", 
            SUPABASE_TOKEN
        ],
    )

    try:

        await server_config.initialize()

        supabase_tools = await build_livekit_tools(server_config)
        tools = [firecrawl_search] + supabase_tools

        agent = Agent(
            instructions=(
                "You can either perform live web searches via `firecrawl_search` or "
                "database queries via Supabase MCP tools. "
                "Choose the appropriate tool based on whether the user needs fresh web data "
                "(news, external facts) or internal Supabase data."
            ),
            tools=tools,
        )

        '''
        session = AgentSession(
            vad=silero.VAD.load(min_silence_duration=0.1),
            stt=assemblyai.STT(word_boost=["Supabase"]),
            llm=openai.LLM(model="gpt-4o"),
            tts=openai.TTS(voice="ash"),
        )
        '''

        #Literal['universal-streaming-english', 'universal-streaming-multilingual', 'u3-rt-pro', 'u3-rt-pro-beta-1', 'u3-pro', 'universal-3-5-pro'] = "universal-3-5-pro",

        # Set up a voice AI pipeline using OpenAI, Cartesia, Deepgram, and the LiveKit turn detector
        session = AgentSession(
            #Keep min_silence_duration=0.1 only if you disable TurnDetector behavior:
            #Set turn detection mode to STT/manual instead of streaming TurnDetector
            #min_silence_duration=0.1 not heard voice, but STT is still working. 0.25 is the default for TurnDetector.
            vad=silero.VAD.load(min_silence_duration=0.25),

            # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
            # See all available models at https://docs.livekit.io/agents/models/stt/
            #stt=assemblyai.STT(word_boost=["Supabase"]),
            stt=inference.STT(model="deepgram/nova-3", language="multi"),

            # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
            # See all available models at https://docs.livekit.io/agents/models/llm/
            #llm=openai.LLM(model="gpt-4o"),
            llm=inference.LLM(model="google/gemma-4-31b-it"),

            # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
            # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
            #tts=openai.TTS(voice="ash"),
            tts=inference.TTS(
                model="cartesia/sonic-3", voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
            ),
            # To use a realtime model instead of a voice pipeline, replace the LLM
            # with a RealtimeModel and remove the STT/TTS from the AgentSession
            # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/)
            # 1. Install livekit-agents[openai]
            # 2. Set OPENAI_API_KEY in .env.local
            # 3. Add `from livekit.plugins import openai` to the top of this file
            # 4. Replace the llm argument with:
            #     llm=openai.realtime.RealtimeModel(voice="marin")
        )
        

        await session.start(agent=agent, room=ctx.room)
        await session.generate_reply(instructions="Hello! How can I assist MAK today?")

        # Keep the session alive until cancelled
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Session cancelled, shutting down.")

    finally:
        logger.info("Session finally ended.")
        await server_config.aclose()
        #await server.__aexit__(None, None, None)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
