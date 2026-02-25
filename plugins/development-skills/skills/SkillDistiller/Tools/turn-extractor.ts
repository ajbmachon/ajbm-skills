#!/usr/bin/env bun
/**
 * turn-extractor.ts
 *
 * Extracts clean user/assistant turn pairs from Claude Code JSONL transcripts.
 * Filters noise internally (tool_use, tool_result, system, thinking blocks)
 * then pairs each user message with the preceding assistant response.
 *
 * Usage:
 *   bun run turn-extractor.ts <input.jsonl>
 *   bun run turn-extractor.ts <input.jsonl> --output <path>
 */

import { readFileSync, writeFileSync } from "fs";

interface ContentBlock {
  type: string;
  text?: string;
}

interface Message {
  role: string;
  content: string | ContentBlock[];
}

interface JournalEntry {
  type: string;
  message?: Message;
}

interface TurnPair {
  turn_number: number;
  assistant_context: string;
  user_action: string;
}

// --- CLI arg parsing ---

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
  console.log(`turn-extractor — Extract user/assistant turn pairs from JSONL transcripts

Usage:
  bun run turn-extractor.ts <input.jsonl>
  bun run turn-extractor.ts <input.jsonl> --output <path>

Options:
  --output, -o <path>   Write JSON output to file instead of stdout
  --help, -h            Show this help message

Output format:
  JSON array of turn objects:
  [
    {
      "turn_number": 1,
      "assistant_context": "What Claude said before the user responded",
      "user_action": "What the user said"
    }
  ]
`);
  process.exit(0);
}

let inputPath: string | undefined;
let outputPath: string | undefined;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--output" || args[i] === "-o") {
    outputPath = args[++i];
  } else if (!args[i].startsWith("-")) {
    inputPath = args[i];
  }
}

if (!inputPath) {
  console.error("Error: No input file provided. Use --help for usage.");
  process.exit(1);
}

// --- Read and parse JSONL ---

let raw: string;
try {
  raw = readFileSync(inputPath, "utf-8");
} catch (err: any) {
  console.error(`Error reading file: ${err.message}`);
  process.exit(1);
}

const lines = raw.split("\n").filter((line) => line.trim().length > 0);

// --- Extract text from content blocks, filtering noise ---

function extractText(content: string | ContentBlock[]): string {
  if (typeof content === "string") return content.trim();
  if (!Array.isArray(content)) return "";

  return content
    .filter(
      (block) =>
        block.type === "text" && typeof block.text === "string"
    )
    .map((block) => block.text!.trim())
    .filter((t) => t.length > 0)
    .join("\n\n");
}

// --- Filter and collect clean messages ---

type CleanMessage = { role: "assistant" | "user"; text: string };

const messages: CleanMessage[] = [];

for (const line of lines) {
  let entry: JournalEntry;
  try {
    entry = JSON.parse(line);
  } catch {
    continue; // skip malformed lines
  }

  // Only process human and assistant message types
  if (entry.type !== "user" && entry.type !== "assistant") continue;
  if (!entry.message?.content) continue;

  const role = entry.type === "user" ? "user" : "assistant";
  const text = extractText(entry.message.content);

  // Skip if no meaningful text content after filtering
  if (!text) continue;

  messages.push({ role: role as "assistant" | "user", text });
}

// --- Pair into turns ---
// A "turn" is: assistant says something, then user responds.
// If conversation starts with user (no prior assistant), assistant_context is empty.

const turns: TurnPair[] = [];
let turnNumber = 0;
let lastAssistantText = "";

for (const msg of messages) {
  if (msg.role === "assistant") {
    // Accumulate assistant text. If multiple assistant messages appear
    // before a user message, concatenate them.
    if (lastAssistantText) {
      lastAssistantText += "\n\n" + msg.text;
    } else {
      lastAssistantText = msg.text;
    }
  } else if (msg.role === "user") {
    turnNumber++;
    turns.push({
      turn_number: turnNumber,
      assistant_context: lastAssistantText,
      user_action: msg.text,
    });
    lastAssistantText = "";
  }
}

// --- Output ---

const output = JSON.stringify(turns, null, 2);

if (outputPath) {
  try {
    writeFileSync(outputPath, output + "\n", "utf-8");
    console.error(`Wrote ${turns.length} turns to ${outputPath}`);
  } catch (err: any) {
    console.error(`Error writing output: ${err.message}`);
    process.exit(1);
  }
} else {
  console.log(output);
}
