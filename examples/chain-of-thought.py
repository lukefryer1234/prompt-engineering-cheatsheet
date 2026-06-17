<![CDATA["""
Chain of Thought (CoT) Prompting Examples
==========================================

Demonstrates zero-shot CoT, few-shot CoT, and self-consistency
using the OpenAI Python SDK.

Learn more: https://aipromptarchitect.co.uk/guides/best-ai-prompt-techniques

Requirements:
    pip install openai

Usage:
    export OPENAI_API_KEY="sk-..."
    python chain-of-thought.py
"""

from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


# ---------------------------------------------------------------------------
# 1. Zero-Shot Chain of Thought
# ---------------------------------------------------------------------------

def zero_shot_cot(question: str) -> str:
    """
    Zero-shot CoT: Simply append "Let's think step by step" to the question.
    
    This technique improves accuracy on reasoning tasks by 40-70% compared
    to direct prompting, with zero additional examples needed.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": f"{question}\n\nLet's think step by step.",
        }],
        temperature=0,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# 2. Few-Shot Chain of Thought
# ---------------------------------------------------------------------------

COT_EXAMPLES = [
    {
        "question": (
            "Roger has 5 tennis balls. He buys 2 cans of 3 tennis balls each. "
            "How many tennis balls does he have now?"
        ),
        "reasoning": (
            "Roger starts with 5 balls. "
            "He buys 2 cans × 3 balls per can = 6 balls. "
            "Total: 5 + 6 = 11 balls."
        ),
        "answer": "11",
    },
    {
        "question": (
            "A restaurant had 23 apples. They used 20 to make lunch and bought "
            "6 more. How many apples do they have?"
        ),
        "reasoning": (
            "Start with 23 apples. "
            "After lunch: 23 - 20 = 3 apples. "
            "After buying more: 3 + 6 = 9 apples."
        ),
        "answer": "9",
    },
    {
        "question": (
            "A juggler can juggle 16 balls. Half of the balls are golf balls, "
            "and half of the golf balls are blue. How many blue golf balls?"
        ),
        "reasoning": (
            "Total balls: 16. "
            "Golf balls: 16 / 2 = 8. "
            "Blue golf balls: 8 / 2 = 4."
        ),
        "answer": "4",
    },
]


def few_shot_cot(question: str) -> str:
    """
    Few-shot CoT: Provide examples that show the reasoning process.
    
    The model learns to mimic the step-by-step reasoning pattern
    from the provided examples.
    """
    # Build the example string
    examples_text = ""
    for ex in COT_EXAMPLES:
        examples_text += (
            f"Q: {ex['question']}\n"
            f"A: {ex['reasoning']} The answer is {ex['answer']}.\n\n"
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful maths tutor. Solve problems step by step, "
                    "showing your reasoning clearly before giving the final answer."
                ),
            },
            {
                "role": "user",
                "content": f"{examples_text}Q: {question}\nA:",
            },
        ],
        temperature=0,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# 3. Self-Consistency (Multiple CoT Paths)
# ---------------------------------------------------------------------------

def self_consistency_cot(
    question: str,
    num_paths: int = 5,
    temperature: float = 0.7,
) -> dict:
    """
    Self-consistency: Generate multiple reasoning paths and take a majority vote.
    
    This technique is especially effective for maths and logic problems where 
    there's a single correct answer. By sampling diverse reasoning paths,
    correct answers tend to cluster while errors are random.
    
    Args:
        question: The question to answer.
        num_paths: Number of independent reasoning paths to generate.
        temperature: Higher temperature = more diverse reasoning paths.
    
    Returns:
        Dict with 'answer', 'confidence', 'paths', and 'vote_distribution'.
    """
    paths = []

    for _ in range(num_paths):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": (
                    f"{question}\n\n"
                    "Think step by step, then provide your final answer "
                    "on the last line in the format: ANSWER: <your answer>"
                ),
            }],
            temperature=temperature,
        )

        full_response = response.choices[0].message.content
        paths.append(full_response)

    # Extract answers from each path
    answers = []
    for path in paths:
        # Look for "ANSWER: <answer>" pattern
        lines = path.strip().split("\n")
        for line in reversed(lines):
            if "ANSWER:" in line.upper():
                answer = line.split(":", 1)[-1].strip()
                answers.append(answer)
                break

    # Majority vote
    if not answers:
        return {
            "answer": "Could not extract answers",
            "confidence": 0.0,
            "paths": paths,
            "vote_distribution": {},
        }

    from collections import Counter
    vote_counts = Counter(answers)
    best_answer, best_count = vote_counts.most_common(1)[0]
    confidence = best_count / len(answers)

    return {
        "answer": best_answer,
        "confidence": confidence,
        "paths": paths,
        "vote_distribution": dict(vote_counts),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_question = (
        "A store sells notebooks for £2.50 each. Sarah buys 4 notebooks "
        "and pays with a £20 note. She also has a 10% discount coupon. "
        "How much change does she receive?"
    )

    print("=" * 60)
    print("ZERO-SHOT CHAIN OF THOUGHT")
    print("=" * 60)
    result = zero_shot_cot(test_question)
    print(result)
    print()

    print("=" * 60)
    print("FEW-SHOT CHAIN OF THOUGHT")
    print("=" * 60)
    result = few_shot_cot(test_question)
    print(result)
    print()

    print("=" * 60)
    print("SELF-CONSISTENCY (5 PATHS)")
    print("=" * 60)
    result = self_consistency_cot(test_question, num_paths=5)
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print(f"Vote distribution: {result['vote_distribution']}")
]]>
