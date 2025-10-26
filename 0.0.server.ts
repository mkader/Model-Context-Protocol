import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

class MyMCPServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'my-first-mcp-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  private setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'hello',
            description: 'Say hello to the world',
            inputSchema: {
              type: 'object',
              properties: {
                name: {
                  type: 'string',
                  description: 'Name to greet',
                },
              },
            },
          },


          // Add this to your tools list
{
  name: 'get-time',
  description: 'Get the current time',
  inputSchema: {
    type: 'object',
    properties: {},
  },
},
{
  name: 'calculate',
  description: 'Perform basic mathematical calculations',
  inputSchema: {
    type: 'object',
    properties: {
      operation: {
        type: 'string',
        enum: ['add', 'subtract', 'multiply', 'divide'],
        description: 'Mathematical operation to perform',
      },
      a: {
        type: 'number',
        description: 'First number',
      },
      b: {
        type: 'number',
        description: 'Second number',
      },
    },
    required: ['operation', 'a', 'b'],
  },
}

          
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'hello':
          const nameToGreet = args?.name || 'World';
          return {
            content: [
              {
                type: 'text',
                text: `Hello, ${nameToGreet}! This is your first MCP server responding.`,
              },
            ],
          };

case 'get-time':
  return {
    content: [
      {
        type: 'text',
        text: `Current time: ${new Date().toISOString()}`,
      },
    ],
  };

case 'calculate':
  const { operation, a, b } = args as {
    operation: string;
    a: number;
    b: number;
  };
  
  let result: number;
  switch (operation) {
    case 'add':
      result = a + b;
      break;
    case 'subtract':
      result = a - b;
      break;
    case 'multiply':
      result = a * b;
      break;
    case 'divide':
      if (b === 0) throw new Error('Division by zero');
      result = a / b;
      break;
    default:
      throw new Error(`Unknown operation: ${operation}`);
  }
  
  return {
    content: [
      {
        type: 'text',
        text: `${a} ${operation} ${b} = ${result}`,
      },
    ],
  };



          
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('MCP server running on stdio');
  }
}

const server = new MyMCPServer();
server.run().catch(console.error);
