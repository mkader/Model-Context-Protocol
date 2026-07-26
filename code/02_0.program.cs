/*
    <PackageReference Include="Microsoft.Extensions.Logging.Console" Version="9.0.10" />
    <PackageReference Include="ModelContextProtocol" Version="0.4.0-preview.3" />
    <PackageReference Include="NJsonSchema" Version="11.5.1" />

    Compile
    c:\csharp\McpWeatherServer> dotnet publish -c Release -o publish --self-contained false /p:PublishSingleFile=true

    Run MCCP
    c:\csharp\McpWeatherServer> npx -y @modelcontextprotocol/inspector dotnet run c:\csharp\McpWeatherServer\publish\McpWeatherServer.dll
    
*/
using System.ComponentModel;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Protocol;
using ModelContextProtocol.Server;

// The main entry point for our server application
class Program
{
    static async Task Main(string[] args)
    {
        // Create the server options
        var serverOptions = new McpServerOptions
        {
            ServerInfo = new Implementation
            {
                Name = "WeatherServer",
                Version = "1.0.0"
            },
            Capabilities = new ServerCapabilities
            {
                Tools = new()
            },
            Handlers = new McpServerHandlers
            {
                ListToolsHandler = (request, cancellationToken) =>
                    ValueTask.FromResult(new ListToolsResult
                    {
                        Tools =
                        [
                            new Tool
                            {
                                Name = "getWeatherData",
                                Description = "Gets the current weather for a specified location.",
                                InputSchema = JsonSerializer.Deserialize<JsonElement>("""
                                    {
                                        "type": "object",
                                        "properties": {
                                          "location": {
                                            "type": "string",
                                            "description": "The location to get weather for"
                                          }
                                        },
                                        "required": ["location"]
                                    }
                                    """),
                            }
                        ]
                    }),

                // Mark lambda async to allow awaiting GetWeatherDataAsync
                CallToolHandler = async (request, cancellationToken) =>
                {
                    if (request.Params?.Name == "getWeatherData")
                    {
                        if (request.Params.Arguments?.TryGetValue("location", out var location) is not true)
                        {
                            return new CallToolResult
                            {
                                Content = [new TextContentBlock { Text = "Missing location parameter" }],
                                IsError = true
                            };
                        }

                        var weatherData = await GetWeatherDataAsync(location.ToString() ?? "");

                        return new CallToolResult
                        {
                            Content = [new TextContentBlock
                            {
                                Text = JsonSerializer.Serialize(weatherData)
                            }]
                        };
                    }

                    return new CallToolResult
                    {
                        Content = [new TextContentBlock { Text = $"Unknown tool: {request.Params?.Name}" }],
                        IsError = true
                    };
                }
            }
        };

        // Create and run server with stdio transport
        // Configure logging to stderr to avoid interfering with MCP protocol on stdout
        using var loggerFactory = LoggerFactory.Create(builder =>
            builder.AddConsole(options => options.LogToStandardErrorThreshold = LogLevel.Trace));

        await using var stdioTransport = new StdioServerTransport("WeatherServer", loggerFactory);
        await using var server = McpServer.Create(stdioTransport, serverOptions, loggerFactory);

        Console.WriteLine("MCP Weather Server is running...");
        Console.WriteLine("Exposing tool: getWeatherData(location)");

        // Run until process is stopped by the client (parent process)
        await server.RunAsync(); 
    }    // This is the implementation of the function we want to expose via the MCP server.
   
   private static async Task<WeatherData> GetWeatherDataAsync(string location)
    {
        Console.Error.WriteLine($"[HANDLER] Received request for weather in: {location}");

         // This would normally call a weather API
        // Simplified for demonstration
        await Task.Delay(100); // Simulate API call
        return new WeatherData
        {
            Temperature = 72.5,
            Conditions = "Sunny",
            Location = location
        };
    }
}

// Define a class for the data we will return.
public class WeatherData 
{
    [JsonPropertyName("temperature")]
    public double Temperature { get; set; }

    [JsonPropertyName("conditions")]
    public string Conditions { get; set; } = string.Empty;

    [JsonPropertyName("location")]
    public string Location { get; set; } = string.Empty;
}
