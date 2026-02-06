# Multi-Agent Framework Skill Definition Patterns

**Research Date:** 2026-02-02
**Researcher:** Ava Sterling (ClaudeResearcher)
**Focus:** LLM-agnostic skill definitions, composability, hierarchical patterns, discovery mechanisms

---

## Executive Summary

This research analyzes skill and tool definition patterns across major multi-agent frameworks. The industry is converging on several key patterns:

1. **Skills as Markdown with YAML frontmatter** - Pioneered by Claude Code, now adopted by Spring AI and becoming an open standard
2. **Progressive disclosure** - Load skill metadata at startup, full content on-demand
3. **Tool Search pattern** - Discover tools dynamically rather than loading all upfront (34-64% token savings)
4. **Agent-as-Tool pattern** - Wrap sub-agents as invocable tools for hierarchical composition
5. **Handoff pattern** - Explicit delegation between agents for task routing

---

## Framework Analysis

### 1. Spring AI Agent Skills

**Source:** [Spring AI Agentic Patterns - Agent Skills](https://spring.io/blog/2026/01/13/spring-ai-generic-agent-skills/)

#### Skill Definition Pattern

Skills are **modular folders** containing instructions, scripts, and resources that AI agents discover and load on demand.

**Folder Structure:**
```
skill-name/
├── SKILL.md           # Required: instructions + YAML frontmatter
├── reference.md       # Optional: detailed documentation
├── examples.md        # Optional: usage examples
├── scripts/           # Optional: executable helpers
│   └── process.py
└── assets/            # Optional: templates, resources
```

**SKILL.md Format:**
```markdown
---
name: my-skill
description: >
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when working with PDF files, converting PDFs, or manipulating PDF content.
allowed-tools: FileSystemTools, ShellTools
model: gpt-4o  # Optional: specific LLM
---

# My Skill Instructions

Instructions that tell the agent how to perform this task...
```

**Key Metadata Fields:**
| Field | Purpose |
|-------|---------|
| `name` | Identifier (lowercase, hyphens, max 64 chars) |
| `description` | Semantic trigger text (max 1024 chars) - CRITICAL for matching |
| `allowed-tools` | Comma-separated tools the AI can access |
| `model` | Optional specific LLM for this skill |

#### Skill Loading Mechanism

```java
SkillsTool.builder()
    .addSkillsDirectory(".claude/skills")
    .addSkillsDirectory(System.getenv("HOME") + "/.claude/skills")
    .build()
```

**Three-Phase Invocation:**
1. **Discovery** - Startup scans directories, extracts name + description from YAML
2. **Semantic Matching** - User requests match against skill descriptions
3. **Execution** - Full SKILL.md loads when relevance determined

#### Application to Claude Code Skills

**Direct Pattern Match:** Spring AI's implementation is explicitly inspired by Claude Code's Agent Skills. The SKILL.md format, folder structure, and progressive disclosure pattern are nearly identical.

**Key Insight:** Skills provide knowledge and instructions, not arbitrary code execution. They're declarative capability extensions.

---

### 2. Vercel AI SDK

**Source:** [AI SDK by Vercel](https://ai-sdk.dev/docs/introduction), [AI SDK 6](https://vercel.com/blog/ai-sdk-6)

#### Agent Abstraction (v6+)

AI SDK 6 introduces a formal **Agent abstraction** for building reusable agents:

```typescript
import { Agent, tool } from 'ai';
import { z } from 'zod';

// Tool definition with Zod schema
const searchTool = tool({
  description: 'Search the web for information',
  parameters: z.object({
    query: z.string().describe('The search query'),
  }),
  execute: async ({ query }) => {
    // Implementation
    return results;
  },
});

// Agent definition - reusable across application
const researchAgent = new Agent({
  name: 'researcher',
  model: 'gpt-4o', // or any supported model
  instructions: 'You are a research assistant...',
  tools: [searchTool],
});
```

#### Tool Definition Pattern

```typescript
import { tool, dynamicTool } from 'ai';
import { jsonSchema, zodSchema, valibotSchema } from 'ai';

// Static tool with Zod
const staticTool = tool({
  description: 'What the tool does',
  parameters: zodSchema(z.object({
    param1: z.string(),
    param2: z.number().optional(),
  })),
  execute: async (params) => { /* ... */ },
});

// Dynamic tool - schema generated at runtime
const dynamicTool = dynamicTool({
  description: 'Dynamically configured tool',
  parametersSchema: async () => fetchSchemaFromAPI(),
  execute: async (params) => { /* ... */ },
});
```

#### Composability Patterns

**Middleware System:**
```typescript
import { wrapLanguageModel } from 'ai';

const wrappedModel = wrapLanguageModel(baseModel, {
  beforeCall: async (options) => {
    // Pre-processing
    return options;
  },
  afterCall: async (result) => {
    // Post-processing
    return result;
  },
});
```

**Provider Registry:**
```typescript
import { createProviderRegistry } from 'ai';

const registry = createProviderRegistry({
  openai: openaiProvider,
  anthropic: anthropicProvider,
  // Model-agnostic tool definitions work across all
});
```

#### Application to Claude Code Skills

**Pattern:** Define agents once with model, instructions, and tools - reuse across application.

**Key Insight:** AI SDK achieves model-agnosticism through the provider registry pattern. Tools defined with Zod schemas work identically across OpenAI, Anthropic, Google, etc.

---

### 3. CrewAI

**Source:** [CrewAI Agents](https://docs.crewai.com/en/concepts/agents), [CrewAI GitHub](https://github.com/crewAIInc/crewAI)

#### Agent Definition Pattern

CrewAI uses **role-based agent design** with three essential attributes:

```python
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

# Tool definition
search_tool = SerperDevTool()

# Agent with role, goal, backstory
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.""",
    tools=[search_tool],
    verbose=True,
    allow_delegation=True,  # Can delegate to other agents
    max_iter=15,           # Iteration limits
    max_rpm=100,           # Rate limiting
)
```

#### YAML Configuration (Recommended)

```yaml
# config/agents.yaml
researcher:
  role: "Senior Research Analyst for {topic}"
  goal: "Uncover groundbreaking technologies in {topic}"
  backstory: >
    You're a seasoned researcher with expertise in {topic}.
    Known for finding the most relevant information.
  tools:
    - SerperDevTool
    - WebScraperTool
  allow_delegation: true
```

Variables like `{topic}` are dynamically replaced at runtime.

#### Tool Definition Pattern

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="The search query")

class CustomSearchTool(BaseTool):
    name: str = "Custom Search"
    description: str = "Search the web for information"
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        # Implementation
        return results
```

#### Multi-Agent Design Patterns

| Pattern | Description |
|---------|-------------|
| **Coordinator-Worker** | Main planner breaks tasks into subtasks for specialized agents |
| **Collaborative Peer Group** | Agents share outputs iteratively, refine each other's results |
| **Hybrid Planner-Executor** | Combines planning, execution, and feedback loops |

#### Application to Claude Code Skills

**Pattern:** Role-based agents with explicit backstory provide context. YAML configuration enables template-based agent definitions.

**Key Insight:** The `backstory` field is similar to skill instructions - provides context for how the agent should behave in its role.

---

### 4. Microsoft AutoGen / Agent Framework

**Source:** [AutoGen GitHub](https://github.com/microsoft/autogen), [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/)

#### Framework Evolution

Microsoft merged **AutoGen** (research) with **Semantic Kernel** (enterprise SDK) into the unified **Microsoft Agent Framework** (GA Q1 2026).

#### Agent Definition Pattern (AutoGen v0.4+)

```python
from autogen import AssistantAgent, UserProxyAgent

# Agent with tools
assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful AI assistant.",
    llm_config={
        "config_list": config_list,
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Search for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    }
)
```

#### Tool Definition with @ai_function (New Pattern)

```python
from semantic_kernel.functions import ai_function

class SearchPlugin:
    @ai_function(
        name="search",
        description="Search the web for information"
    )
    def search(self, query: str) -> str:
        """Search implementation."""
        return results
```

#### Agent-as-Tool Pattern

```python
# Wrap an agent as a tool for hierarchical composition
from autogen import AgentTool

research_agent = AssistantAgent(name="researcher", ...)
research_tool = AgentTool(agent=research_agent)

# Parent agent can invoke research_agent as a tool
orchestrator = AssistantAgent(
    name="orchestrator",
    tools=[research_tool]
)
```

#### Key Architectural Features

- **Asynchronous messaging** - Event-driven agent communication
- **Modular components** - Pluggable agents, tools, memory, models
- **Distributed runtime** - Agents across organizational boundaries
- **OpenTelemetry support** - Built-in observability

#### Application to Claude Code Skills

**Pattern:** The `@ai_function` decorator and Agent-as-Tool pattern provide clean abstractions for hierarchical skill composition.

**Key Insight:** Agent Framework supports MCP, A2A messaging, and OpenAPI-first design for cross-runtime portability.

---

### 5. LangChain / LangGraph

**Source:** [LangChain 1.0](https://www.blog.langchain.com/langchain-langgraph-1dot0/), [LangGraph Skills](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)

#### Skills Pattern

Skills are **prompt-driven specializations** simpler than full sub-agents:

```python
from langchain.tools import tool

# Skill loading tool
@tool
def load_skill(skill_name: str) -> str:
    """Load a skill's instructions and context on-demand."""
    skill_path = f".claude/skills/{skill_name}/SKILL.md"
    return read_skill_content(skill_path)

# Register with agent
agent = create_agent(
    model="gpt-4o",
    tools=[load_skill],
    system_prompt="You have access to skills. Load them when needed."
)
```

#### When to Use Skills vs Sub-Agents

| Use Skills When | Use Sub-Agents When |
|-----------------|---------------------|
| Single agent with many specializations | Complex multi-step coordination |
| No constraints between capabilities | Strict workflow requirements |
| Teams develop capabilities independently | Shared state across steps |

#### Hierarchical Sub-Agent Pattern

```python
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_agent

# Worker agents
research_agent = create_agent(model, research_tools, "Research agent")
writing_agent = create_agent(model, writing_tools, "Writing agent")

# Supervisor routes to workers
def supervisor_router(state):
    # Analyze task, route to appropriate worker
    if "research" in state["task"]:
        return "research"
    return "writing"

# Compose into graph
graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor_agent)
graph.add_node("research", research_agent)
graph.add_node("writing", writing_agent)
graph.add_conditional_edges("supervisor", supervisor_router)
```

#### Composability Features

```python
# Graphs are composable - agents inside custom workflows
from langgraph.prebuilt import create_agent

# Create agent with high-level API
simple_agent = create_agent(model, tools, system_prompt)

# Use inside custom LangGraph workflow
workflow = StateGraph(State)
workflow.add_node("agent", simple_agent)
workflow.add_node("custom_logic", my_custom_function)
```

#### Application to Claude Code Skills

**Pattern:** LangGraph's skills pattern uses a `load_skill` tool that retrieves skill prompts on-demand - exactly matching Claude Code's progressive disclosure.

**Key Insight:** Skills can contain sub-skills in tree structures (e.g., "data_science" skill exposing "pandas_expert" sub-skill).

---

### 6. Google Agent Development Kit (ADK)

**Source:** [Google ADK Docs](https://google.github.io/adk-docs/), [Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)

#### Agent Definition Pattern

```python
from adk import Agent, Tool

# Tool definition
@Tool
def search(query: str) -> str:
    """Search the web for information."""
    return results

# Agent with tools
agent = Agent(
    name="researcher",
    model="gemini-1.5-pro",
    instructions="You are a research assistant.",
    tools=[search]
)
```

#### AgentTool Pattern (Hierarchical Composition)

```python
from adk import Agent, AgentTool

# Sub-agent
research_agent = Agent(
    name="researcher",
    tools=[search_tool, analyze_tool]
)

# Wrap as tool for parent agent
research_tool = AgentTool(research_agent)

# Parent agent invokes sub-agent as a function
orchestrator = Agent(
    name="orchestrator",
    tools=[research_tool]  # Entire sub-agent as one tool
)
```

#### Eight Essential Multi-Agent Patterns

| Pattern | Description |
|---------|-------------|
| **Sequential Pipeline** | Linear workflows, agents pass outputs sequentially |
| **Coordinator/Dispatcher** | Central agent routes to specialists |
| **Parallel Fan-Out/Gather** | Multiple agents execute simultaneously |
| **Hierarchical Decomposition** | Complex tasks broken into sub-tasks |
| **Generator and Critic** | One generates, another validates |
| **Iterative Refinement** | Cycle until quality thresholds met |
| **Human-in-the-Loop** | Humans authorize critical actions |
| **Composite** | Real systems combine multiple patterns |

#### Workflow Agents

```python
from adk import SequentialAgent, ParallelAgent, LoopAgent

# Sequential execution
pipeline = SequentialAgent([
    research_agent,
    analysis_agent,
    report_agent
])

# Parallel execution
parallel = ParallelAgent([
    web_search_agent,
    database_search_agent
])
```

#### Application to Claude Code Skills

**Pattern:** ADK's AgentTool pattern directly maps to skills that spawn sub-agents. The workflow agents (Sequential, Parallel, Loop) provide orchestration primitives.

**Key Insight:** ADK is model-agnostic and supports MCP, LangChain, LlamaIndex, CrewAI tools interoperably.

---

### 7. OpenAI Agents SDK

**Source:** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), [New Tools for Building Agents](https://openai.com/index/new-tools-for-building-agents/)

#### Core Primitives

The SDK has intentionally **few primitives**:

1. **Agents** - LLMs with instructions and tools
2. **Handoffs** - Delegate to other agents
3. **Guardrails** - Input/output validation
4. **Tracing** - Execution visualization

#### Agent Definition Pattern

```python
from openai_agents import Agent, FunctionTool

# Function tool with automatic schema generation
@FunctionTool
def search(query: str) -> str:
    """Search the web for information.

    Args:
        query: The search query
    """
    return results

# Agent definition
agent = Agent(
    name="researcher",
    instructions="You are a research assistant.",
    tools=[search]
)
```

#### Handoff Pattern

```python
from openai_agents import Agent, Handoff

# Specialist agents
research_agent = Agent(name="researcher", ...)
writing_agent = Agent(name="writer", ...)

# Orchestrator can hand off to specialists
orchestrator = Agent(
    name="orchestrator",
    instructions="Route tasks to the appropriate specialist.",
    handoffs=[
        Handoff(research_agent, condition="research needed"),
        Handoff(writing_agent, condition="writing needed")
    ]
)
```

#### Tool Schema with Pydantic

```python
from pydantic import BaseModel, Field
from openai_agents import FunctionTool

class SearchParams(BaseModel):
    query: str = Field(description="The search query")
    max_results: int = Field(default=10, description="Maximum results")

@FunctionTool(args_schema=SearchParams)
def search(query: str, max_results: int = 10) -> str:
    """Search with validated parameters."""
    return results
```

#### Application to Claude Code Skills

**Pattern:** The handoff pattern maps to skills that route to other skills. Pydantic schemas provide type-safe skill parameters.

**Key Insight:** Provider-agnostic design works with 100+ LLMs through Chat Completions API.

---

## Cross-Framework Patterns

### 1. LLM-Agnostic Skill Definitions

**Universal Pattern:** Define skills as structured data (YAML/JSON metadata + Markdown instructions) that any LLM can interpret.

**Implementation Across Frameworks:**

| Framework | Skill Definition |
|-----------|------------------|
| Spring AI | SKILL.md with YAML frontmatter |
| Vercel AI SDK | TypeScript Agent class with Zod schemas |
| CrewAI | YAML config + Python classes |
| AutoGen | @ai_function decorator |
| LangGraph | Tool decorator + skill loader |
| Google ADK | Agent class + Tool decorator |
| OpenAI SDK | FunctionTool + Pydantic schemas |

### 2. Skill Composability Patterns

**a) Hierarchical Composition (Agent-as-Tool):**
```
Parent Agent
  └── Sub-Agent A (wrapped as tool)
        └── Sub-Agent A1 (wrapped as tool)
  └── Sub-Agent B (wrapped as tool)
```

**b) Sequential Composition:**
```
Agent 1 → Agent 2 → Agent 3 → Result
```

**c) Parallel Composition:**
```
         ┌→ Agent A ─┐
Input ───┼→ Agent B ─┼──→ Aggregator → Result
         └→ Agent C ─┘
```

**d) Skill Tree (LangGraph/Claude Code):**
```
data_science (skill)
  ├── pandas_expert (sub-skill)
  ├── visualization (sub-skill)
  └── statistics (sub-skill)
```

### 3. Skill Discovery and Routing

**Tool Search Pattern (Anthropic/Spring AI):**
1. Load only a "search tool" initially
2. Model queries for capabilities when needed
3. Relevant tool definitions expand into context
4. **Result:** 34-64% token savings

**Semantic Matching Pattern:**
1. Extract name + description at startup
2. Match user requests against descriptions
3. Load full skill content when matched

**Hierarchical Routing:**
```
User Request
    ↓
Top Supervisor (routes to domain)
    ↓
Domain Supervisor (routes to worker)
    ↓
Worker Agent (executes task)
```

### 4. Skill Lifecycle Patterns

| Phase | Pattern |
|-------|---------|
| **Registration** | Scan directories, extract metadata |
| **Discovery** | Semantic matching against descriptions |
| **Loading** | Progressive disclosure - full content on-demand |
| **Execution** | Agent processes skill instructions |
| **State Management** | Shared state via `output_key` or session |
| **Cleanup** | Context pruning, state persistence |

### 5. Tool vs Skill vs Agent Distinctions

| Concept | Definition | Example |
|---------|------------|---------|
| **Tool** | Single function with schema | `search(query: str)` |
| **Skill** | Instructions + resources for a domain | PDF processing skill |
| **Agent** | LLM + instructions + tools + state | Research agent |
| **Sub-Agent** | Agent invoked by parent agent | Specialist worker |
| **Handoff** | Explicit delegation between agents | Routing to specialist |

---

## Recommendations for Claude Code Skill Authoring

### 1. SKILL.md Best Practices

Based on cross-framework patterns:

```markdown
---
name: skill-name
description: >
  What the skill does. When to use it.
  Trigger keywords users might say.
  Max 1024 chars, semantic matching critical.
allowed-tools: tool1, tool2
model: optional-specific-llm
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## Instructions
Step-by-step guidance for the agent...

## Examples
Concrete usage examples...
```

### 2. Hierarchical Sub-Agent Skills

```markdown
---
name: data-analysis
description: Analyze data, create visualizations, statistical analysis
sub-skills: pandas-expert, visualization, statistics
---

# Data Analysis Skill

## Sub-Skills
Load specialized sub-skills for specific tasks:
- `pandas-expert` - DataFrame operations
- `visualization` - Charts and graphs
- `statistics` - Statistical tests

## Routing
Match request to appropriate sub-skill...
```

### 3. Skill Discovery Optimization

- Keep descriptions under 1024 characters
- Include specific trigger keywords
- Front-load the most important capabilities
- Use consistent naming patterns

### 4. Composability Design

- Skills should be **atomic** (do one thing well)
- Support **chaining** (output of one feeds another)
- Enable **parallel execution** where independent
- Provide clear **handoff conditions**

---

## Sources

### Spring AI
- [Spring AI Agentic Patterns - Agent Skills](https://spring.io/blog/2026/01/13/spring-ai-generic-agent-skills/)
- [Spring AI Skills Tool Documentation](https://github.com/spring-ai-community/spring-ai-agent-utils/blob/main/spring-ai-agent-utils/docs/SkillsTool.md)
- [Tool Search Tool Pattern](https://spring.io/blog/2025/12/11/spring-ai-tool-search-tools-tzolov/)

### Vercel AI SDK
- [AI SDK Introduction](https://ai-sdk.dev/docs/introduction)
- [AI SDK 6 Announcement](https://vercel.com/blog/ai-sdk-6)
- [Introducing Skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)

### CrewAI
- [CrewAI Agents Documentation](https://docs.crewai.com/en/concepts/agents)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI Guide 2025](https://mem0.ai/blog/crewai-guide-multi-agent-ai-teams)

### Microsoft AutoGen / Agent Framework
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [Microsoft Agent Framework Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)
- [Semantic Kernel + AutoGen Merge](https://visualstudiomagazine.com/articles/2025/10/01/semantic-kernel-autogen--open-source-microsoft-agent-framework.aspx)

### LangChain / LangGraph
- [LangChain and LangGraph 1.0](https://www.blog.langchain.com/langchain-langgraph-1dot0/)
- [LangGraph Multi-Agent Workflows](https://www.blog.langchain.com/langgraph-multi-agent-workflows/)
- [Hierarchical Agent Teams Tutorial](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)
- [LangChain Skills Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)

### Google ADK
- [Agent Development Kit Docs](https://google.github.io/adk-docs/)
- [Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [ADK for TypeScript](https://developers.googleblog.com/introducing-agent-development-kit-for-typescript-build-ai-agents-with-the-power-of-a-code-first-approach/)

### OpenAI Agents SDK
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [New Tools for Building Agents](https://openai.com/index/new-tools-for-building-agents/)
- [OpenAI Swarm (Predecessor)](https://github.com/openai/swarm)

### Model Context Protocol & Industry Standards
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [Agent Skills: Anthropic's Standard](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/)
- [A Year of MCP](https://www.pento.ai/blog/a-year-of-mcp-2025-review)

### Research & Analysis
- [Single-Agent Skills vs Multi-Agent Systems](https://www.arxiv.org/pdf/2601.04748)
- [AI Agent Framework Landscape 2025](https://medium.com/@hieutrantrung.it/the-ai-agent-framework-landscape-in-2025-what-changed-and-what-matters-3cd9b07ef2c3)
- [Agent Design Patterns](https://rlancemartin.github.io/2026/01/09/agent_design/)
