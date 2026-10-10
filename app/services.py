"""
Business logic layer — maps each task to its prompt template.
Separated from routing (main.py) and LLM transport (llm_client.py).
"""

from .llm_client import generate

PROMPTS = {
    "summarize": "Summarize the following text concisely in 3-5 bullet points.",
    "rewrite": "Rewrite the following text in a clear, professional tone.",
    "keypoints": "Extract the key points from the following text as a numbered list.",
    "explain": "Explain the following concept in simple terms that anyone can understand.",
}


def process_task(task: str, text: str) -> dict:
    if task not in PROMPTS:
        raise ValueError(f"Unknown task: {task}. Available: {list(PROMPTS.keys())}")

    result = generate(PROMPTS[task], text)
    return {
        "task": task,
        "content": result["content"],
        "tokens_used": result["tokens_used"],
    }
