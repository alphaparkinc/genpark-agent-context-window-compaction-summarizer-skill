"""Context Window Compaction Summarizer Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any

class ContextWindowCompactionSummarizer:
    """Maintains agent conversation continuity within tight token budgets via recursive semantic bridges."""
    def __init__(self, max_token_budget: int = 150):
        self.max_tokens = max_token_budget

    def _estimate_tokens(self, text: str) -> int:
        return len(text.split())

    def compact_history(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        total_tokens = sum(self._estimate_tokens(m.get("content", "")) for m in messages)
        if total_tokens <= self.max_tokens:
            return {"compacted": False, "messages": messages, "tokens_used": total_tokens}

        system_msgs = [m for m in messages if m.get("role") == "system"]
        conversation = [m for m in messages if m.get("role") != "system"]

        if len(conversation) <= 2:
            return {"compacted": False, "messages": messages, "tokens_used": total_tokens}

        keep_recent = conversation[-2:]
        evicted = conversation[:-2]

        summary_text = (
            f"[Context Bridge: Condensed {len(evicted)} historical turns: "
            + "; ".join(e.get("content", "")[:30].replace("\n", " ") for e in evicted)
            + "]"
        )
        bridge = {"role": "system", "content": summary_text}

        compacted_msgs = system_msgs + [bridge] + keep_recent
        new_token_count = sum(self._estimate_tokens(m["content"]) for m in compacted_msgs)
        return {
            "compacted": True,
            "original_tokens": total_tokens,
            "compacted_tokens": new_token_count,
            "evicted_turns": len(evicted),
            "messages": compacted_msgs
        }
