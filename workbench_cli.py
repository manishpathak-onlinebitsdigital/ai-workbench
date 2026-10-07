"""
Lab 1C: AI Workbench CLI v1
A menu-driven CLI application with 4 AI tasks.
Demonstrates: separation of prompts from logic, function reuse, user interaction loop.

Architecture:
  User input → Task selection → Prompt template → LLM API → Formatted response

This same architecture becomes a REST API in Week 2.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

# Ensure box-drawing characters render on Windows terminals (cp1252 default).
# Harmless on macOS/Linux, which are already UTF-8. Guarded for older Pythons.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# --- PROMPT TEMPLATES ---
# Each task = a different system prompt. Adding a new AI capability = adding an entry here.
TASKS = {
    "1": {
        "name": "Summarize",
        "prompt": "You are a concise summarizer. Summarize the user's text in 3-5 clear bullet points. Focus on the most important information.",
    },
    "2": {
        "name": "Rewrite",
        "prompt": "You are a professional editor. Rewrite the user's text in a clear, professional tone. Maintain the original meaning but improve clarity and readability.",
    },
    "3": {
        "name": "Key Points",
        "prompt": "You are an analyst. Extract the key points from the user's text as a numbered list. Each point should be one clear sentence.",
    },
    "4": {
        "name": "Explain",
        "prompt": "You are a patient teacher. Explain the user's text in simple terms that a non-expert can understand. Use analogies where helpful.",
    },
}


def call_llm(system_prompt: str, user_text: str) -> dict:
    """
    Call the LLM with a system prompt and user text.
    Returns dict with 'content', 'tokens', and 'model' keys.
    Handles errors gracefully with specific messages.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return {
            "content": response.choices[0].message.content,
            "tokens": response.usage.total_tokens,
            "model": response.model,
        }
    except AuthenticationError:
        return {"content": "Error: Invalid API key. Check your .env file.", "tokens": 0, "model": "N/A"}
    except RateLimitError:
        return {"content": "Error: Rate limit hit. Wait a moment and try again.", "tokens": 0, "model": "N/A"}
    except APIConnectionError:
        return {"content": "Error: Cannot connect to OpenAI. Check your internet.", "tokens": 0, "model": "N/A"}
    except Exception as e:
        return {"content": f"Error: {e}", "tokens": 0, "model": "N/A"}


def display_menu():
    print("\n┌──────────────────────────────────────┐")
    print("│        AI WORKBENCH CLI v1           │")
    print("├──────────────────────────────────────┤")
    for key, task in TASKS.items():
        print(f"│  {key}. {task['name']:<32}│")
    print("├──────────────────────────────────────┤")
    print("│  q. Quit                             │")
    print("└──────────────────────────────────────┘")


def get_user_text() -> str:
    print("\n  Paste your text below.")
    print("  (Press Enter on an empty line to submit)")
    print("  " + "─" * 36)
    lines = []
    while True:
        try:
            line = input("  │ ")
        except EOFError:
            break
        if line == "":
            if lines:
                break
        else:
            lines.append(line)
    return "\n".join(lines)


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("┌──────────────────────────────────────┐")
        print("│  ERROR: OPENAI_API_KEY not set        │")
        print("│                                       │")
        print("│  1. Copy .env.example → .env          │")
        print("│  2. Add your API key                  │")
        print("│  3. Run again                         │")
        print("└──────────────────────────────────────┘")
        sys.exit(1)

    print("\n  Welcome to AI Workbench!")
    print(f"  Model: {MODEL}")
    print(f"  Tasks available: {len(TASKS)}")

    session_tokens = 0

    while True:
        display_menu()
        choice = input("\n  Select a task (1-4 or q): ").strip()

        if choice.lower() == "q":
            print(f"\n  Session total: {session_tokens} tokens used")
            print("  Goodbye!\n")
            break

        if choice not in TASKS:
            print("  Invalid choice. Enter 1-4 or q.")
            continue

        task = TASKS[choice]
        print(f"\n  → Task: {task['name']}")
        user_text = get_user_text()

        if not user_text.strip():
            print("  No text provided. Try again.")
            continue

        print(f"\n  Processing ({task['name']})...")
        result = call_llm(task["prompt"], user_text)

        print(f"\n  {'━' * 38}")
        print(f"  Result ({task['name']}):")
        print(f"  {'━' * 38}")
        print()
        for line in result["content"].split("\n"):
            print(f"  {line}")
        print()
        print(f"  {'━' * 38}")
        print(f"  Tokens: {result['tokens']} | Model: {result['model']}")
        print(f"  {'━' * 38}")

        session_tokens += result["tokens"]


if __name__ == "__main__":
    main()
