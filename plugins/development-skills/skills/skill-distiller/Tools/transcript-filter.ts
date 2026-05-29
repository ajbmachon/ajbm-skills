#!/usr/bin/env bun
/**
 * transcript-filter.ts
 *
 * Filters noise from Claude Code JSONL conversation transcripts.
 * Keeps user and assistant text content. Strips tool_use, tool_result,
 * system messages, thinking blocks, and progress events.
 *
 * Usage:
 *   bun run transcript-filter.ts <input.jsonl> [--output <path>]
 */

const USAGE = `
transcript-filter -- Strip noise from Claude Code JSONL transcripts

Usage:
  bun run transcript-filter.ts <input.jsonl> [--output <path>]

Options:
  --output <path>   Write filtered JSONL to a file instead of stdout
  --help            Show this help message

What it keeps:
  - User messages (text content only)
  - Assistant messages (text content only, tool_use blocks removed)

What it strips:
  - System role messages
  - Messages with type "system"
  - Tool use content blocks
  - Tool result messages (type "result")
  - Thinking blocks (type "thinking")
  - Progress events
`.trim();

// ---------------------------------------------------------------------------
// Argument parsing
// ---------------------------------------------------------------------------

const args = Bun.argv.slice(2);

if (args.includes("--help") || args.length === 0) {
  console.log(USAGE);
  process.exit(0);
}

let inputPath: string | null = null;
let outputPath: string | null = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--output") {
    outputPath = args[++i];
    if (!outputPath) {
      console.error("Error: --output requires a path argument");
      process.exit(1);
    }
  } else if (!args[i].startsWith("--")) {
    inputPath = args[i];
  }
}

if (!inputPath) {
  console.error("Error: No input file specified");
  console.log(USAGE);
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Types (minimal, just what we need for filtering)
// ---------------------------------------------------------------------------

interface ContentBlock {
  type: string;
  text?: string;
  [key: string]: unknown;
}

interface Message {
  role?: string;
  content?: string | ContentBlock[];
  [key: string]: unknown;
}

interface TranscriptLine {
  type?: string;
  message?: Message;
  result?: unknown;
  [key: string]: unknown;
}

// ---------------------------------------------------------------------------
// Filtering logic
// ---------------------------------------------------------------------------

/** Types of top-level JSONL entries to discard entirely. */
const DISCARD_TYPES = new Set(["system", "result", "progress"]);

/** Content block types to strip from assistant message content arrays. */
const STRIP_BLOCK_TYPES = new Set(["tool_use", "tool_result", "thinking"]);

function filterLine(raw: string): string | null {
  const trimmed = raw.trim();
  if (trimmed.length === 0) return null;

  let entry: TranscriptLine;
  try {
    entry = JSON.parse(trimmed);
  } catch {
    // Skip malformed lines silently
    return null;
  }

  // Discard top-level types we don't want
  if (entry.type && DISCARD_TYPES.has(entry.type)) {
    return null;
  }

  const msg = entry.message;
  if (!msg) return null;

  // Discard system role messages
  if (msg.role === "system") {
    return null;
  }

  // If content is a string, keep as-is (user or assistant plain text)
  if (typeof msg.content === "string") {
    return JSON.stringify(entry);
  }

  // If content is an array, filter to text-only blocks
  if (Array.isArray(msg.content)) {
    const filtered = msg.content.filter(
      (block: ContentBlock) =>
        block.type === "text" && !STRIP_BLOCK_TYPES.has(block.type)
    );

    // If nothing left after filtering, discard the entire line
    if (filtered.length === 0) return null;

    // Rebuild the entry with filtered content
    const cleaned: TranscriptLine = {
      ...entry,
      message: {
        ...msg,
        content: filtered,
      },
    };

    return JSON.stringify(cleaned);
  }

  return null;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const file = Bun.file(inputPath!);

  if (!(await file.exists())) {
    console.error(`Error: File not found: ${inputPath}`);
    process.exit(1);
  }

  const text = await file.text();
  const lines = text.split("\n");
  const outputLines: string[] = [];

  for (const line of lines) {
    const result = filterLine(line);
    if (result !== null) {
      outputLines.push(result);
    }
  }

  const output = outputLines.join("\n") + (outputLines.length > 0 ? "\n" : "");

  if (outputPath) {
    await Bun.write(outputPath, output);
    console.error(`Wrote ${outputLines.length} lines to ${outputPath}`);
  } else {
    process.stdout.write(output);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
