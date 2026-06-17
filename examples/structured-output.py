<![CDATA["""
Structured Output Examples
==========================

Demonstrates how to get reliable, typed JSON output from LLMs using
OpenAI's structured output API with Pydantic models.

Learn more: https://aipromptarchitect.co.uk/guides/best-ai-prompt-techniques

Requirements:
    pip install openai pydantic

Usage:
    export OPENAI_API_KEY="sk-..."
    python structured-output.py
"""

from __future__ import annotations

import json
from enum import Enum

from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI()
MODEL = "gpt-4o"


# ---------------------------------------------------------------------------
# 1. Basic Structured Output with Pydantic
# ---------------------------------------------------------------------------

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class ReviewAnalysis(BaseModel):
    """Structured analysis of a product review."""

    sentiment: Sentiment = Field(description="Overall sentiment of the review")
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence score between 0 and 1",
    )
    key_topics: list[str] = Field(
        description="Main topics or aspects mentioned in the review",
    )
    pros: list[str] = Field(description="Positive points mentioned")
    cons: list[str] = Field(description="Negative points mentioned")
    summary: str = Field(
        description="One-sentence summary of the review",
        max_length=200,
    )


def analyse_review(review_text: str) -> ReviewAnalysis:
    """
    Analyse a product review and return structured data.
    
    Uses OpenAI's beta structured output to guarantee the response 
    matches the Pydantic model schema.
    """
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a product review analyst. Analyse the given review "
                    "and extract structured information. Be precise and objective."
                ),
            },
            {"role": "user", "content": review_text},
        ],
        response_format=ReviewAnalysis,
        temperature=0,
    )

    return response.choices[0].message.parsed


# ---------------------------------------------------------------------------
# 2. Complex Nested Structures
# ---------------------------------------------------------------------------

class CodeIssue(BaseModel):
    """A single issue found during code review."""

    line_number: int | None = Field(description="Line number where the issue occurs")
    severity: str = Field(description="critical, high, medium, or low")
    category: str = Field(
        description="Category: security, performance, correctness, style, or maintainability",
    )
    description: str = Field(description="Clear description of the issue")
    suggestion: str = Field(description="Concrete suggestion for fixing the issue")
    code_snippet: str | None = Field(
        default=None,
        description="Suggested code fix, if applicable",
    )


class CodeReview(BaseModel):
    """Structured code review output."""

    overall_quality: int = Field(
        ge=1, le=10,
        description="Overall code quality score from 1 to 10",
    )
    summary: str = Field(description="Brief summary of the code's quality")
    issues: list[CodeIssue] = Field(description="List of issues found")
    positive_aspects: list[str] = Field(
        description="Things done well in the code",
    )
    test_coverage_assessment: str = Field(
        description="Assessment of test coverage and suggestions",
    )


def review_code(code: str, language: str = "python") -> CodeReview:
    """Review code and return structured findings."""
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a senior {language} developer. Review the code for "
                    "bugs, security issues, performance problems, and style. "
                    "Be thorough but fair."
                ),
            },
            {"role": "user", "content": f"```{language}\n{code}\n```"},
        ],
        response_format=CodeReview,
        temperature=0,
    )

    return response.choices[0].message.parsed


# ---------------------------------------------------------------------------
# 3. Structured Output with Enums and Validation
# ---------------------------------------------------------------------------

class Priority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskCategory(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    DOCUMENTATION = "documentation"
    REFACTOR = "refactor"


class ExtractedTask(BaseModel):
    """A task extracted from a meeting transcript or conversation."""

    title: str = Field(description="Short, actionable task title", max_length=100)
    description: str = Field(description="Detailed task description")
    assignee: str | None = Field(description="Person responsible, if mentioned")
    priority: Priority = Field(description="Task priority")
    category: TaskCategory = Field(description="Task category")
    estimated_hours: float | None = Field(
        default=None,
        description="Estimated hours to complete, if inferrable",
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="Other tasks this depends on",
    )


class MeetingExtraction(BaseModel):
    """Structured extraction from a meeting transcript."""

    meeting_summary: str = Field(description="2-3 sentence meeting summary")
    key_decisions: list[str] = Field(description="Decisions made during the meeting")
    action_items: list[ExtractedTask] = Field(description="Tasks to be done")
    open_questions: list[str] = Field(description="Unresolved questions")
    next_meeting_topics: list[str] = Field(
        default_factory=list,
        description="Topics deferred to next meeting",
    )


def extract_meeting_tasks(transcript: str) -> MeetingExtraction:
    """Extract structured tasks and decisions from a meeting transcript."""
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a meeting analyst. Extract all action items, decisions, "
                    "and key information from the meeting transcript. Be thorough — "
                    "don't miss any commitments people made."
                ),
            },
            {"role": "user", "content": transcript},
        ],
        response_format=MeetingExtraction,
        temperature=0,
    )

    return response.choices[0].message.parsed


# ---------------------------------------------------------------------------
# 4. Error Handling and Fallbacks
# ---------------------------------------------------------------------------

def safe_structured_output(
    prompt: str,
    response_model: type[BaseModel],
    max_retries: int = 3,
) -> BaseModel | None:
    """
    Robust structured output with retries and error handling.
    
    Falls back to JSON mode if structured output fails.
    """
    # Attempt 1: Native structured output
    for attempt in range(max_retries):
        try:
            response = client.beta.chat.completions.parse(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format=response_model,
                temperature=0,
            )

            parsed = response.choices[0].message.parsed
            if parsed is not None:
                return parsed

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt == max_retries - 1:
                # Fallback: try JSON mode with manual parsing
                return _fallback_json_mode(prompt, response_model)

    return None


def _fallback_json_mode(
    prompt: str,
    response_model: type[BaseModel],
) -> BaseModel | None:
    """Fallback to JSON mode with manual Pydantic parsing."""
    try:
        schema_str = json.dumps(
            response_model.model_json_schema(), indent=2,
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Respond with valid JSON matching this schema:\n"
                        f"{schema_str}"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )

        raw_json = response.choices[0].message.content
        return response_model.model_validate_json(raw_json)

    except Exception as e:
        print(f"Fallback JSON mode also failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example 1: Review Analysis
    print("=" * 60)
    print("REVIEW ANALYSIS")
    print("=" * 60)

    review = (
        "The laptop's battery life is absolutely incredible — I consistently get "
        "18 hours of mixed use. The display is gorgeous with deep blacks and "
        "vibrant colours. However, the keyboard feels cheap and plasticky for "
        "a £2,000 machine, and the trackpad is slightly off-centre which is "
        "annoying. The speakers are decent but not as good as my previous MacBook. "
        "Overall, I'd recommend it if you prioritise battery and screen quality."
    )

    analysis = analyse_review(review)
    print(f"Sentiment: {analysis.sentiment.value} ({analysis.confidence:.0%})")
    print(f"Summary: {analysis.summary}")
    print(f"Pros: {', '.join(analysis.pros)}")
    print(f"Cons: {', '.join(analysis.cons)}")
    print(f"Topics: {', '.join(analysis.key_topics)}")
    print()

    # Example 2: Code Review
    print("=" * 60)
    print("CODE REVIEW")
    print("=" * 60)

    sample_code = '''
def process_payment(user_id, amount, card_number):
    db = get_connection()
    query = f"SELECT balance FROM users WHERE id = '{user_id}'"
    result = db.execute(query)
    if result[0] > amount:
        db.execute(f"UPDATE users SET balance = balance - {amount} WHERE id = '{user_id}'")
        log(f"Payment processed: {card_number} charged {amount}")
        return True
    return False
'''

    review_result = review_code(sample_code)
    print(f"Quality Score: {review_result.overall_quality}/10")
    print(f"Summary: {review_result.summary}")
    print(f"\nIssues ({len(review_result.issues)}):")
    for issue in review_result.issues:
        print(f"  [{issue.severity.upper()}] {issue.category}: {issue.description}")
]]>
