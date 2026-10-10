"""
Provider-agnostic LLM client.
Architecture: defines a common interface — swap providers by changing config, not code.
Currently implements: OpenAI. Same pattern works for Anthropic, AWS Bedrock.
"""

import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai")
MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")


def generate(task_prompt: str, user_text: str) -> dict:
    """
    Send a completion request to the configured LLM provider.
    Returns dict with 'content' and 'tokens_used' keys.
    """
    if PROVIDER == "openai":
        return _call_openai(task_prompt, user_text)
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}. Supported: openai")


def _call_openai(task_prompt: str, user_text: str) -> dict:
    from openai import OpenAI, RateLimitError, AuthenticationError, APIConnectionError

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not configured")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": task_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else None,
        }
    except AuthenticationError:
        raise PermissionError("Invalid API key. Check your OPENAI_API_KEY.")
    except RateLimitError:
        raise RuntimeError("Rate limit exceeded. Please wait and try again.")
    except APIConnectionError:
        raise ConnectionError("Cannot reach the LLM API. Check your network.")


def get_provider_info() -> dict:
    return {"provider": PROVIDER, "model": MODEL}
