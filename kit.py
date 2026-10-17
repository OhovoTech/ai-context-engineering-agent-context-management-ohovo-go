"""
Context engineering primitives — pure Python, zero lag.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple


class PointerStore:
    """
    Externalize large content: store it, return a short pointer + summary.
    Agent keeps only the pointer in context; fetches full content only when needed.
    """

    def __init__(self, root: str | Path = ".pointers"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def store(self, content: str, summary: str | None = None, prefix: str = "ptr") -> dict:
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        ptr_id = f"{prefix}_{content_hash}"
        path = self.root / f"{ptr_id}.json"
        data = {
            "id": ptr_id,
            "summary": summary or content[:200] + ("..." if len(content) > 200 else ""),
            "length": len(content),
            "stored_at": time.time(),
            "content": content,
        }
        path.write_text(json.dumps(data), encoding="utf-8")
        # What the agent actually sees in context
        return {
            "pointer": ptr_id,
            "summary": data["summary"],
            "length": data["length"],
            "hint": f"Use load_pointer('{ptr_id}') if full content is required",
        }

    def load(self, ptr_id: str) -> str | None:
        path = self.root / f"{ptr_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("content")


def compress_text(text: str, max_sentences: int = 5) -> str:
    """
    Simple extractive compression: keep first + last + highest-keyword-density sentences.
    No model required.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) <= max_sentences:
        return text
    # Keep head, tail, and a couple of middle ones with most words
    scored = sorted(
        enumerate(sentences),
        key=lambda x: len(x[1].split()),
        reverse=True,
    )
    keep_idx = set([0, len(sentences) - 1])
    for idx, _ in scored:
        if len(keep_idx) >= max_sentences:
            break
        keep_idx.add(idx)
    return " ".join(sentences[i] for i in sorted(keep_idx))


def select_relevant(query: str, documents: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    """Keyword overlap scorer — instant."""
    q_tokens = set(re.findall(r"\w+", query.lower()))
    scored = []
    for doc in documents:
        d_tokens = set(re.findall(r"\w+", doc.lower()))
        if not q_tokens:
            score = 0.0
        else:
            score = len(q_tokens & d_tokens) / len(q_tokens)
        scored.append((doc, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def isolate_context(full_context: dict, agent_id: str, allowed_keys: List[str] | None = None) -> dict:
    """
    Give each sub-agent only the keys it needs.
    Prevents context pollution across agents.
    """
    if allowed_keys is None:
        # default: only give the agent its own slice + shared pointers
        allowed_keys = [k for k in full_context if k.startswith(agent_id) or k.startswith("shared_")]
    return {k: full_context[k] for k in allowed_keys if k in full_context}
