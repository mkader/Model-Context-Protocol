import { Tool } from "./tools.js";
import { MathInputSchema } from "./schema.js";

export default {
    name: "add",
    rawSchema: MathInputSchema,
    inputSchema: {
        type: "object",
        properties: {
            a: { type: "number" },
            b: { type: "number" }
        },
        required: ["a", "b"],
        additionalProperties: false
    },
    callback: async ({ a, b }) => {
        return {
            content: [{ type: "text", text: String(a + b) }]
        };
    }
} as Tool;