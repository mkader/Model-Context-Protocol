
// used to test the token in .env

import { config } from "dotenv";
import { verifyToken } from "./util.js";

config();

let decodedToken = verifyToken(process.env.token || "");
const payload = decodedToken && typeof decodedToken !== "string"
	? (decodedToken as { name?: string })
	: null;

console.log("Decoded Token:", decodedToken);
console.log("User exist", ["User usersson", "user1"].includes(payload?.name || ""));

console.log("Token from .env:", process.env.token);