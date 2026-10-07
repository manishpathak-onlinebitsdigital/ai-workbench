"""
Lab 1B: Prompt Engineering Experiment
A structured scientific experiment testing 4 variables that affect LLM output.
Demonstrates: how prompts shape responses, temperature effects, output formatting.

Run individual experiments:
  python prompt_experiment.py 1    # Specificity only
  python prompt_experiment.py 2    # Persona only
  python prompt_experiment.py 3    # Format only
  python prompt_experiment.py 4    # Temperature only
  python prompt_experiment.py      # All experiments
"""

import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SAMPLE_TEXT = """
Artificial intelligence has transformed how businesses operate. Companies now use
machine learning for everything from customer service chatbots to predictive
maintenance in manufacturing. However, the rapid adoption of AI has also raised
concerns about job displacement, algorithmic bias, and data privacy. Experts argue
that responsible AI development requires transparency, fairness, and accountability
at every stage of the development lifecycle.
""".strip()

total_tokens = 0
total_calls = 0


def call_llm(prompt: str, temperature: float = 0.7) -> tuple[str, int]:
    """Call the LLM and return (response_text, tokens_used)."""
    global total_tokens, total_calls
    start = time.time()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=300,
    )

    elapsed = time.time() - start
    tokens = response.usage.total_tokens
    total_tokens += tokens
    total_calls += 1

    text = response.choices[0].message.content
    print(f"  [{tokens} tokens, {elapsed:.1f}s]")
    return text, tokens


def experiment_specificity():
    """Variable 1: Instruction specificity (vague → precise)"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Instruction Specificity")
    print("Question: How does prompt precision affect output quality?")
    print("=" * 60)

    levels = [
        ("Vague", f"Summarize this:\n{SAMPLE_TEXT}"),
        ("Specific", f"Summarize this text in exactly 3 bullet points:\n{SAMPLE_TEXT}"),
        ("Highly specific", f"Summarize this text in 3 bullet points, each under 15 words, focusing only on business impact:\n{SAMPLE_TEXT}"),
    ]

    for label, prompt in levels:
        print(f"\n--- Level: {label} ---")
        print(f"  Prompt: '{prompt.split(chr(10))[0]}'")
        result, _ = call_llm(prompt)
        print(f"  Output:\n{result}")

    print("\n  OBSERVATION: Notice how specificity controls length, format, and focus.")
    print("  → More specific instructions = more predictable, useful outputs.")


def experiment_persona():
    """Variable 2: Persona / audience targeting"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Persona / Audience Targeting")
    print("Question: How does the target audience change the response?")
    print("=" * 60)

    personas = [
        ("CEO", f"You are briefing a CEO who has 30 seconds. Summarize the key business decision from this text:\n{SAMPLE_TEXT}"),
        ("10-year-old", f"Explain this to a curious 10-year-old using simple words and an analogy:\n{SAMPLE_TEXT}"),
        ("Software Engineer", f"Summarize this for a software engineer evaluating AI tools for their team. Focus on technical implications:\n{SAMPLE_TEXT}"),
    ]

    for persona, prompt in personas:
        print(f"\n--- Audience: {persona} ---")
        result, _ = call_llm(prompt)
        print(f"  Output:\n{result}")

    print("\n  OBSERVATION: Same source text, completely different outputs.")
    print("  → The audience instruction reshapes vocabulary, depth, and framing.")


def experiment_format():
    """Variable 3: Output format (free text vs structured)"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Output Format Control")
    print("Question: Can you control the structure of AI output?")
    print("=" * 60)

    formats = [
        ("Free text", f"Summarize this:\n{SAMPLE_TEXT}"),
        ("JSON", f"Summarize this as valid JSON with keys: \"main_point\", \"risks\", \"opportunities\". Output ONLY the JSON:\n{SAMPLE_TEXT}"),
        ("Markdown table", f"Summarize this as a markdown table with columns: Theme | Key Point | Implication. Include 3 rows:\n{SAMPLE_TEXT}"),
    ]

    for fmt, prompt in formats:
        print(f"\n--- Format: {fmt} ---")
        result, _ = call_llm(prompt)
        print(f"  Output:\n{result}")

    print("\n  OBSERVATION: LLMs can output structured data (JSON, tables, lists).")
    print("  → This is how AI integrates with software systems — structured output.")


def experiment_temperature():
    """Variable 4: Temperature effect on same prompt"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: Temperature Effect")
    print("Question: How does temperature change output variability?")
    print("=" * 60)

    prompt = f"Write a one-sentence creative tagline for this technology:\n{SAMPLE_TEXT}"
    temperatures = [0.0, 0.7, 1.5]

    for temp in temperatures:
        print(f"\n--- Temperature: {temp} ---")
        print(f"  Running same prompt twice to compare consistency:")
        results = []
        for run in range(2):
            result, _ = call_llm(prompt, temperature=temp)
            results.append(result)
            print(f"    Run {run + 1}: {result}")

        if results[0] == results[1]:
            print("  → Outputs are IDENTICAL (deterministic)")
        else:
            print("  → Outputs DIFFER (probabilistic sampling)")

    print("\n  OBSERVATION:")
    print("  → temp=0: Same output every time. Use for factual/consistent tasks.")
    print("  → temp=0.7: Balanced. Good default for most applications.")
    print("  → temp=1.5: High variance. Use for creative/brainstorming tasks.")


def print_summary():
    """Print experiment summary with total usage."""
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE — Summary")
    print("=" * 60)
    print(f"  Total API calls made: {total_calls}")
    print(f"  Total tokens used:    {total_tokens}")
    print(f"  Estimated cost:       ${total_tokens * 0.00000015:.4f} (approx)")
    print()
    print("  Key Findings:")
    print("  1. SPECIFICITY: More precise prompts → more useful outputs")
    print("  2. PERSONA: Audience framing changes vocabulary and depth")
    print("  3. FORMAT: LLMs can output structured data (JSON, tables)")
    print("  4. TEMPERATURE: Controls randomness vs consistency")
    print()
    print("  → The prompt IS the program. Master prompts = master AI.")
    print("=" * 60)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set. See .env.example")
        sys.exit(1)

    print("=" * 60)
    print("Lab 1B: Prompt Engineering Experiment")
    print(f"Model: {MODEL}")
    print(f"Sample text: {len(SAMPLE_TEXT)} chars")
    print("=" * 60)

    experiments = {
        "1": experiment_specificity,
        "2": experiment_persona,
        "3": experiment_format,
        "4": experiment_temperature,
    }

    if len(sys.argv) > 1 and sys.argv[1] in experiments:
        experiments[sys.argv[1]]()
    else:
        for exp in experiments.values():
            exp()

    print_summary()
