import { Client, ClientOptions } from "discord.js";
import interactionCreate from "./listeners/interactionCreate";
import ready from "./listeners/ready";

require('dotenv').config()
const token = process.env.BOT_TOKEN;
const channel = process.env.GH_CHANNEL;

console.log("Bot is starting...");

const client = new Client({
    intents: []
});

ready(client);
interactionCreate(client);

client.login(token); 