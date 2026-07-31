import re
import json
import os
import asyncio
import yfinance as yf
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool

from dotenv import load_dotenv

load_dotenv()


class QueryAnalysisOutput(BaseModel):
    """Structured output for the query analysis task."""
    symbols: list[str] = Field(..., description="List of stock ticker symbols (e.g., ['TSLA', 'AAPL']).")
    timeframe: str = Field(..., description="Time period (e.g., '1d', '1mo', '1y').")
    action: str = Field(..., description="Action to be performed (e.g., 'fetch', 'plot').")


openai_api_key = os.getenv("OPENAI_API_KEY", "asdaadsd").strip()
openai_model = os.getenv("OPENAI_MODEL", "EGPT-4.1").strip()
openai_base_url = os.getenv("OPENAI_BASE_URL", "https://eus2.openai.azure.com/openai/v1").strip()
if not openai_api_key:
    raise ValueError("Missing OPENAI_API_KEY. Set it in your environment or .env file.")

llm = LLM(
    base_url=openai_base_url,
    model=f"{openai_model}",
    api_key=openai_api_key,
    # temperature=0.7
)


# 1) Query parser agent
query_parser_agent = Agent(
    role="Stock Data Analyst",
    goal="Extract stock details and fetch required data from this user query: {query}.",
    backstory="You are a financial analyst specializing in stock market data retrieval.",
    llm=llm,
    verbose=False,
    memory=True,
)

query_parsing_task = Task(
    description="Analyze the user query and extract stock details.",
    expected_output="A dictionary with keys: 'symbol', 'timeframe', 'action'.",
    output_pydantic=QueryAnalysisOutput,
    agent=query_parser_agent,
)


# 2) Code writer agent
code_writer_agent = Agent(
    role="Senior Python Developer",
    goal="Write Python code to visualize stock data.",
    backstory="""You are a Senior Python developer specializing in stock market data visualization.
                 You are also a Pandas, Matplotlib and yfinance library expert.
                 You are skilled at writing production-ready Python code""",
    llm=llm,
    verbose=False,
)

code_writer_task = Task(
    description="""Write Python code to visualize stock data based on the inputs from the stock analyst
                   where you would find stock symbol, timeframe and action.""",
    expected_output="A clean and executable Python script file (.py) for stock visualization.",
    agent=code_writer_agent,
)


# 3) Code execution agent
code_execution_agent = Agent(
    role="Senior Code Execution Expert",
    goal="Review and execute the generated Python code by code writer agent to visualize stock data and fix any errors encountered. It can delegate tasks to code writer agent if needed.",
    backstory="You are a code execution expert. You are skilled at executing Python code.",
    allow_code_execution=True,
    allow_delegation=True,
    llm=llm,
    verbose=False,
)

code_execution_task = Task(
    description="""Review and execute the generated Python code by code writer agent to visualize stock data and fix any errors encountered.""",
    expected_output="A clean, working and executable Python script file (.py) for stock visualization.",
    agent=code_execution_agent,
)

# Create the crew
crew = Crew(
    agents=[query_parser_agent, code_writer_agent, code_execution_agent],
    tasks=[query_parsing_task, code_writer_task, code_execution_task],
    process=Process.sequential,
)


# Function to be wrapped inside MCP tool
async def run_financial_analysis_async(query):
    result = await crew.kickoff_async(inputs={"query": query})
    return result.raw


def run_financial_analysis(query):
    result = asyncio.run(run_financial_analysis_async(query))
    return result


if __name__ == "__main__":
    # Run the crew with a query
    print(asyncio.run(run_financial_analysis_async("Plot YTD stock gain of Tesla")))
