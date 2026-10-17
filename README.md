# Ohovo Contextoo – Context Engineering Kit for AI Agents

**Lightweight tools to externalize, select, compress, and isolate context for AI agents.**  
Prevents context bloat and “lost in the middle” problems.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Local-first](https://img.shields.io/badge/local--first-yes-brightgreen.svg)](#)

## What is Ohovo Contextoo?

Ohovo Contextoo (package name: `context-engineering-kit`) gives you simple, fast primitives that implement the classic context-engineering pattern:

- **Externalize** – store large content outside the prompt and keep only a pointer (`PointerStore`)
- **Select** – keep only the most relevant pieces (`select_relevant`)
- **Compress** – shorten text while preserving meaning (`compress_text`)
- **Isolate** – give different agents their own clean context views (`isolate_context`)

Everything runs locally with zero required external services and virtually no lag.

## Compatible AI Models & Frameworks

Works with any model or agent that can call Python functions:

- Claude / Claude Code
- GPT-4o, o-series / Codex
- Grok, Gemini
- Local models (Ollama, llama.cpp, vLLM…)
- LangGraph, CrewAI, AutoGen, Cursor, OpenHands, custom agents

## Installation

```bash
pip install -e .
# later: pip install ohovo-contextoo
```

## Quick Start

```python
from context_engineering_kit import PointerStore, compress_text, select_relevant, isolate_context

# 1. Externalize large content → get a short pointer
store = PointerStore(root=".pointers")
big_content = "Very long log or document..." * 500
pointer = store.store(big_content, summary="Large log containing important error")
print(pointer)
# {'pointer': 'ptr_...', 'summary': '...', 'length': ..., 'hint': '...'}

# 2. Compress text
short = compress_text("Sentence one. Sentence two is longer and has more words. Final.", max_sentences=2)
print(short)

# 3. Select only relevant items
items = ["dogs bark loudly", "cats are fluffy", "the weather is rainy today"]
relevant = select_relevant("dog bark", items)
print(relevant)

# 4. Isolate context per agent
full_context = {"agent_a_plan": "do X", "agent_b_plan": "do Y", "shared_ptr": "ptr_123"}
isolated = isolate_context(full_context, agent_id="agent_a", keep_shared=True)
print(isolated)
```

## How to Use – User Guide

### Externalize (PointerStore)
Store large blobs outside the prompt. The agent receives only a short pointer + summary. Load the full content later only when needed with `store.load(pointer_id)`.

### Compress
Simple extractive compression that keeps the most important sentences. Useful before sending tool outputs into the context window.

### Select
Rank a list of strings by relevance to a query (keyword overlap). Fast and dependency-free.

### Isolate
Give each agent its own filtered view of a shared context dictionary so agents do not see each other’s private keys.

## Why Ohovo Contextoo?

- Implements the proven “externalize / select / compress / isolate” pattern
- Zero lag, pure Python
- Perfect companion to any agent memory system
- Ready for future paid model-specific optimizers

## License

Apache-2.0
