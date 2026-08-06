import asyncio
from typing import List
from firecrawl import Firecrawl

from livekit.agents import (
    RunContext,
)

firecrawl = Firecrawl(api_key="fc-sdfsdfsdfd")

# Scrape a website:
'''scrape_status = firecrawl.scrape(
  'https://firecrawl.dev', 
  formats=['summary']
)
print(scrape_status)


# Crawl a website:
crawl_status = firecrawl.crawl(
  'https://firecrawl.dev',  
  limit=1, 
  scrape_options={
    'formats': ['markdown']
  }
)
print(crawl_status)


crawl_status1 = firecrawl.crawl_url(
  'https://firecrawl.dev',
  limit=1,
  scrape_options={
    'formats': ['markdown']
  }
)
print(crawl_status1)
'''

async def firecrawl_search(
    context: RunContext,
    query: str,
    limit: int = 5
) -> List[str]:
#async def firecrawl_search() -> List[str]:
  loop = asyncio.get_event_loop()
  try:
    crawl_job = await loop.run_in_executor(
        None,
        lambda: firecrawl.crawl_url(
            url = 'https://www.google.com/search?q=Tesla TSLA stock quote Yahoo Finance (limit=1)',
            limit=2,
            scrape_options={
                'formats': ["html", 'markdown']
            }
        )
    )
    data = crawl_job.data if hasattr(crawl_job, "data") and crawl_job.data else []
    print(f"Firecrawl returned {len(data)} pages")

    return data
  except asyncio.TimeoutError:
    print(f"Timeout: The crawl request for took too long.")
    return []
  except Exception as e:
    print(f"Firecrawl search failed: {e}")
    return []

result = asyncio.run(firecrawl_search(
    context=None,
    query="Tesla TSLA stock quote Yahoo Finance",
    limit=1
))
#print(result)
