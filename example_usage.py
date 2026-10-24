from client import ContextWindowCompactionSummarizer

summarizer = ContextWindowCompactionSummarizer(max_token_budget=20)
dialogue = [
    {"role": "system", "content": "You are a helpful research agent."},
    {"role": "user", "content": "Step 1: Ingest server metrics and database connections."},
    {"role": "assistant", "content": "Ingested 50 servers and confirmed steady state."},
    {"role": "user", "content": "Step 2: Scan for rogue background processes."},
    {"role": "assistant", "content": "Scan complete with 0 alerts."},
    {"role": "user", "content": "Step 3: What is the final status of deployment?"}
]

result = summarizer.compact_history(dialogue)
print("=== Context Compaction Telemetry ===")
print("Compacted:", result["compacted"])
print(f"Tokens: {result['original_tokens']} -> {result['compacted_tokens']}")
for msg in result["messages"]:
    print(f"  [{msg['role']}]: {msg['content']}")
