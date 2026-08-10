* https://github.com/patchy631 - AI, ML...
* https://www.dailydoseofds.com/archive/

| | OpenAI |	Ollama |
|-|-|-|
| Hosting	| Cloud (OpenAI/Azure servers)	| Local (runs on your machine) |
| Privacy	| Data sent to external API	Fully | private, no data leaves your machine |
| Cost	| Pay per token	| Free (you pay only for hardware) |
| Setup	| Just an API key	| Must download & run models locally |
| Speed	| Fast (depends on network)	| Depends on your CPU/GPU |
| Models	| GPT-4o, GPT-4.1, etc.	| LLaMA, Mistral, Phi, Gemma, etc. |
| Internet	| Required	| Not required after download |
| Quality	| State-of-the-art (GPT-4.1)	| Good, but generally behind frontier models |
| Context window	| Large (128K+)	| Varies by model/hardware  |

* In your code:
  - client.py uses Ollama → Ollama(model="llama3.2") — runs locally, free, private
  - client_openai.py uses OpenAI/Azure → AsyncOpenAI(base_url=..., api_key=...) — calls Azure, costs tokens, needs internet

* When to use which:
  - Ollama → prototyping, sensitive data, offline, zero cost
  - OpenAI → production, best accuracy, complex reasoning tasks
