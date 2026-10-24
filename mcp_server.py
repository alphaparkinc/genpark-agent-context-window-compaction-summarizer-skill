import sys
import json
from client import ContextWindowCompactionSummarizer

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compact_messages",
                        "description": "Prunes conversation history and inserts semantic summary bridges.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "messages": {"type": "array"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        args = params.get("arguments", {})
        summarizer = ContextWindowCompactionSummarizer()
        res = summarizer.compact_history(args.get("messages", []))
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    summarizer = ContextWindowCompactionSummarizer()
    print(json.dumps(summarizer.compact_history([{"role": "user", "content": "test"}]), indent=2))

if __name__ == "__main__":
    main()
