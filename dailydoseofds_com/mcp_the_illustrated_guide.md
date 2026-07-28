## What is MCP? 
* Only know English. To get info from a person who only knows or you must learn French, German, ... 

   <img width="250" height="150" alt="image" src="https://github.com/user-attachments/assets/a1f642c4-a491-4ee5-bd5d-3c9c187752e9" />

* Learning even 5 languages will be a nightmare for you. Add a translator that understands all languages

   <img width="300" height="150" alt="image" src="https://github.com/user-attachments/assets/af835b4e-3834-467f-9250-86307dbf7b2c" />

* The translator is like an MCP.
  - It lets you (Agents) talk to other people (tools or other capabilities) through a single interface. 
  - To formalize, while LLMs possess impressive knowledge and reasoning skills, which allow them to perform many complex tasks, their knowledge is limited to their initial training data.
  - If they need to access real-time information, they must use external tools and resources on their own.
  
* MCP is a standardized interface and framework that allows AI models to seamlessly interact with external tools, resources and environments.

  <img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/1f2dca92-8ff0-4645-81a2-3f7c49473490" />

## Why was MCP created? 
* Without MCP, adding a new tool or integrating a new model was a headache. 
* If 3 AI applications and 3 external tools, end up writing 9 different integration modules (each AI x each tool) because there was no common standard. This doesn’t scale. 
Let’s understand this in detail.
* Each AI (each “Model”) might require unique code to connect to each external service (database, filesystem, calculator, etc.), leading to spaghetti-like interconnections. 

  <img width="350" height="200" alt="image" src="https://github.com/user-attachments/assets/8bdf828e-e610-4275-9673-14899d9bdef4" />

* MCP tackles this by introducing a standard interface in the middle.
* Instead of M × N direct integrations, we get M (AI application) + N (tools) implementations an MCP server once.

  <img width="400" height="150" alt="image" src="https://github.com/user-attachments/assets/4dd01ed4-656b-4f1f-a59d-8e80b967d480" />

  <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/5918153a-7936-4917-89a7-83c7403c39e1" />

### MCP Architecture Overview 
* MCP follows a client-server architecture (much like the web or other network protocols). 
* 3 main roles to understand: the Host, the Client, and the Server. 

### Host 
* The Host is the user-facing AI application, the environment where the AI model lives and interacts with the user. 
* This could be a chat application (like OpenAI’s ChatGPT or Anthropic’s Claude desktop app), an AI-enhanced IDE (like Cursor), or any custom app that embeds an AI assistant like Chainlit. 
* Host is the one that initiates connections to the available MCP servers when the system needs them.
* It captures the user's input, keeps the conversation history, 
and displays the model’s replies.

  <img width="350" height="200" alt="image" src="https://github.com/user-attachments/assets/0158d823-68c3-4571-8a0f-723f202df1a5" />


### Client 
* The MCP Client is a component within the Host that handles the low-level communication with an MCP Server. 
* the Host decides what to do, the Client knows how to speak MCP to actually carry out those instructions with the server.
  
  <img width="300" height="150" alt="image" src="https://github.com/user-attachments/assets/624ee72a-03b7-4d0f-95ff-abbb837e6d80" />

### Server 
* The MCP Server is the external program or service that actually provides the capabilities (tools, data, etc.) to the application. 
* An MCP Server exposes a set of actions or resources in a standardized way so that any MCP Client can invoke them. 
* Servers can run locally on the same machine as the Host or remotely on some 
cloud service since MCP is designed to support both scenarios seamlessly.

## Tools, Resources and Prompts 

  <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/8749c747-323b-4623-ad29-4e3ccac8a0d7" />

* Tools, prompts and resources form the 3 core capabilities of the MCP framework.
* Capabilities are essentially the features or functions that the server makes available.  
  - Tools: Executable actions or functions that the AI (host/client) can invoke (often with side effects or external API calls). 
  - Resources: Read-only data sources that the AI (host/client) can query for information (no side effects, just retrieval). 
  - Prompts: Predefined prompt templates or workflows that the server can supply. 

### Tools 
* Tools are usually triggered by the AI model’s choice, which means the LLM (via the host) decides to call a tool when it determines it needs that functionality. 
* a simple tool for weather. In an MCP server’s python code, it might look like:

  <img width="300" height="100" alt="image" src="https://github.com/user-attachments/assets/96e6b1d2-70fe-4d87-b12c-54bda1fdfdf6" />

    - function - registered with @mcp.tool(), can be invoked by the AI via MCP. 
    - When the AI calls tools/call with name "get_weather" and {"location": "San Francisco"} as arguments, the server will execute get_weather("San Francisco") and return the dictionary result. 
    - The client will get that JSON result and make it available to the AI.
    - Notice the tool returns structured data (temperature, conditions), and the AI can then use or 
    verbalize (generate a response) that info. 
    - Since tools can do things like file I/O or network calls, an MCP implementation     often requires that the user permit a tool call. 

### Resources  
* Resources provide read-only data to the AI model. 
* These are like databases or knowledge bases that the AI can query to get information, but not modify. 
* Unlike tools, resources typically do not involve heavy computation or side effects, since they are often just information lookup. 
Another key difference is that resources are usually accessed under the host 
application’s control (not spontaneously by the model). In practice, this might 
mean the Host knows when to fetch a certain context for the model. 
14 
DailyDoseofDS.com 
For instance, if a user says, “Use the company handbook to answer my question,” 
the Host might call a resource that retrieves relevant handbook sections and 
feeds them to the model. 
Resources could include a local file’s contents, a snippet from a knowledge base 
or documentation, a database query result (read-only), or any static data like 
configuration info. 
Essentially anything the AI might need to know as context. An AI research 
assistant could have resources like “ArXiv papers database,” where it can retrieve 
an abstract or reference when asked. 
A simple resource could be a function to read a file: 
Here we use a decorator @mcp.resource("file://{path}") which might indicate a 
template for resource URIs. 
The AI (or Host) could ask the server for resources.get with a URI like 
file://home/user/notes.txt, and the server would 
callread_file("/home/user/notes.txt") and return the text. 
Notice that resources are usually identified by some identifier (like a URI or 
name) rather than being free-form functions. 
15 
DailyDoseofDS.com 
They are also often application-controlled, meaning the app decides when to 
retrieve them (to avoid the model just reading everything arbitrarily). 
From a safety standpoint, since resources are read-only, they are less dangerous, 
but still, one must consider privacy and permissions (the AI shouldn’t read files 
it’s not supposed to). 
The Host can regulate which resource URIs it allows the AI to access, or the 
server might restrict access to certain data. 
In summary, Resources give the AI knowledge without handing over the keys to 
change anything. 
They’re the MCP equivalent of giving the model reference material when needed, 
which acts like a smarter, on-demand retrieval system integrated through the 
protocol. 
Prompts 
Prompts in the MCP context are a special concept: they are predefined prompt 
templates or conversation flows that can be injected to guide the AI’s behavior. 
Essentially, a Prompt capability provides a canned set of instructions or an 
example dialogue that can help steer the model for certain tasks. 
But why have prompts as a capability? 
Think of recurring patterns: e.g., a prompt that sets up the system role as “You 
are a code reviewer,” and the user’s code is inserted for analysis. 
Rather than hardcoding that in the host application, the MCP server can supply 
it. 
Prompts can also represent multi-turn workflows. 
For instance, a prompt might define how to conduct a step-by-step diagnostic 
interview with a user. By exposing this via MCP, any client can retrieve and use 
16 
DailyDoseofDS.com 
these sophisticated prompts on demand. 
As far as control is concerned, Prompts are usually user-controlled or 
developer-controlled. 
The user might pick a prompt/template from a UI (e.g., “Summarize this 
document” template), which the host then fetches from the server. 
The model doesn’t spontaneously decide to use prompts the way it does tools. 
Rather, the prompt sets the stage before the model starts generating. In that 
sense, prompts are often fetched at the beginning of an interaction or when the 
user chooses a specific “mode”. 
Suppose we have a prompt template for code review. The MCP server might have: 
This prompt function returns a list of message objects (in OpenAI format) that 
set up a code review scenario. 
When the host invokes this prompt, it gets those messages and can insert the 
actual code to be reviewed into the user content. 
Then it provides these messages to the model before the model’s own answer. 
Essentially, the server is helping to structure the conversation. 
While we have personally not seen much applicability of this yet, common use 
cases for prompt capabilities include things like “brainstorming guide,” 
“step-by-step problem solver template,” or domain-specific system roles. 
17 
DailyDoseofDS.com 
By having them on the server, they can be updated or improved without changing 
the client app, and different servers can offer different specialized prompts. 
An important point to note here is that prompts, as a capability, blur the line 
between data and instructions. 
They represent best practices or predefined strategies for the AI to use. 
In a way, MCP prompts are similar to how ChatGPT plugins can suggest how to 
format a query, but here it’s standardized and discoverable via the protocol. 
  

  
