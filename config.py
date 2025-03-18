import os

LANGSMITH_TRACING = "true"
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = "TestingLLM"
GROK_API_KEYs = "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"#os.environ.get("GROK_API_KEY")

if not GROK_API_KEYs:
    raise ValueError("Missing 'GROK_API_KEY'. Set it in environment variables.")
