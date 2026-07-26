### Run sample

* Install dependencies ``` npm install ```
* Build it ``` npm run build ```
* Run it ``` npm start ```
    * You should see the text:
        ```text
        Registering tools...
        Starting server...
        ```

### Test the server

* Test web inspector tool ``` npx @modelcontextprotocol/inspector node build/app.js ```

* Test in CLI mode ``` npx @modelcontextprotocol/inspector --cli node ./build/app.js --method tools/list ```
    * You should see the following output:
        ```json
        {
        "tools": [
            {
            "name": "add",
            "inputSchema": {
                "type": "object",
                "properties": {
                "a": {
                    "type": "number"
                },
                "b": {
                    "type": "number"
                }
                },
                "required": [
                "a",
                "b"
                ],
                "additionalProperties": false
            }
            },
            {
            "name": "subtract",
            "inputSchema": {
                "type": "object",
                "properties": {
                "a": {
                    "type": "number"
                },
                "b": {
                    "type": "number"
                }
                },
                "required": [
                "a",
                "b"
                ],
                "additionalProperties": false
            }
            }
        ]
        ```

* Run a tool: ``` npx @modelcontextprotocol/inspector --cli node ./build/app.js --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2 ```

    * You should see a response similar to:
    ```text
    {
    "content": [
        {
        "type": "text",
        "text": "Tool add called with arguments: {\"a\":1,\"b\":2}, result: {\"content\":[{\"type\":\"text\",\"text\":\"3\"}]}"
        }
    ]
    ```

* tool "add2" doesn't exist with this command: ``` npx @modelcontextprotocol/inspector --cli node ./build/app.js --method tools/call --tool-name add2 --tool-arg a=1 --tool-arg b= ```

    * You should now see this message showing that your validatiob works:

        ```text
        {
        "content": [],
        "error": {
            "code": "tool_not_found",
            "message": "Tool add2 not found."
        }
        ```

* sending parameter `c`, rejected by the schema: ``` npx @modelcontextprotocol/inspector --cli node ./build/app.js --method tools/call --tool-name add --tool-arg a=1 --tool-arg c=2 ```

    * You should now see "invalid arguments" error:
        ```text
        {
        "content": [],
        "error": {
            "code": "invalid_arguments",
            "message": "Invalid arguments for tool add: [\n  {\n    \"code\": \"invalid_type\",\n    \"expected\": \"number\",\n    \"received\": \"undefined\",\n    \"path\": [\n      \"b\"\n    ],\n    \"message\": \"Required\"\n  }\n]"
        }
        }
        ```
