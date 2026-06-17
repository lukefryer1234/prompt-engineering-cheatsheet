<![CDATA["""
STCO (Situation, Task, Context, Output) Prompt Template Builder
===============================================================

A reusable framework for constructing structured prompts using
the STCO methodology. Includes template management, variable
interpolation, and ready-to-use templates for common tasks.

STCO Framework Guide: https://aipromptarchitect.co.uk/guides/stco-prompt-framework

Requirements:
    pip install openai

Usage:
    export OPENAI_API_KEY="sk-..."
    python stco-template.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


# ---------------------------------------------------------------------------
# Core STCO Builder
# ---------------------------------------------------------------------------

@dataclass
class STCOPrompt:
    """
    A structured prompt following the STCO framework.
    
    STCO ensures every prompt has four essential components:
    - Situation: Who is the AI? What role and perspective?
    - Task: What specific action needs to be performed?
    - Context: What background, constraints, and data are relevant?
    - Output: What format, structure, and tone should the response use?
    """

    situation: str
    task: str
    context: str
    output: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def render(self, **variables: str) -> str:
        """
        Render the prompt with optional variable interpolation.
        
        Variables are substituted using {variable_name} syntax in any
        of the four STCO components.
        
        Args:
            **variables: Key-value pairs to interpolate into the template.
        
        Returns:
            Formatted prompt string ready for LLM consumption.
        """
        parts = {
            "Situation": self.situation,
            "Task": self.task,
            "Context": self.context,
            "Output": self.output,
        }

        rendered_parts = []
        for label, content in parts.items():
            if variables:
                try:
                    content = content.format(**variables)
                except KeyError as e:
                    raise ValueError(
                        f"Missing variable {e} in {label} component. "
                        f"Available variables: {list(variables.keys())}"
                    ) from e
            rendered_parts.append(f"**{label}:** {content}")

        return "\n\n".join(rendered_parts)

    def to_messages(self, **variables: str) -> list[dict[str, str]]:
        """
        Convert STCO prompt to OpenAI messages format.
        
        Uses the Situation as a system message and the rest as user content.
        """
        situation = self.situation
        if variables:
            situation = situation.format(**variables)

        user_content_parts = []
        for label, content in [("Task", self.task), ("Context", self.context), ("Output", self.output)]:
            if variables:
                content = content.format(**variables)
            user_content_parts.append(f"**{label}:** {content}")

        return [
            {"role": "system", "content": situation},
            {"role": "user", "content": "\n\n".join(user_content_parts)},
        ]

    def execute(self, temperature: float = 0, **variables: str) -> str:
        """Render the prompt and send it to the LLM."""
        messages = self.to_messages(**variables)
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Template Library
# ---------------------------------------------------------------------------

class STCOTemplates:
    """A collection of pre-built STCO templates for common tasks."""

    @staticmethod
    def code_review(language: str = "Python") -> STCOPrompt:
        """Template for thorough code reviews."""
        return STCOPrompt(
            situation=(
                "You are a principal {language} engineer with 15+ years of experience "
                "in production systems. You are known for thorough, constructive code "
                "reviews that catch subtle bugs while mentoring junior developers."
            ),
            task=(
                "Review the following code for:\n"
                "1. Correctness — logic errors, edge cases, off-by-one errors\n"
                "2. Security — injection, authentication, data exposure\n"
                "3. Performance — algorithmic complexity, resource leaks, N+1 queries\n"
                "4. Maintainability — naming, structure, SOLID principles\n"
                "5. Error handling — missing try/catch, unhandled edge cases"
            ),
            context=(
                "Tech stack: {tech_stack}\n"
                "Code to review:\n```{language}\n{code}\n```\n"
                "Additional context: {additional_context}"
            ),
            output=(
                "Provide your review as a structured report:\n\n"
                "## Summary\nOne paragraph overall assessment.\n\n"
                "## Critical Issues 🔴\nMust fix before merge.\n\n"
                "## Warnings 🟡\nShould fix soon.\n\n"
                "## Suggestions 🟢\nNice to have improvements.\n\n"
                "## Positive Aspects ✅\nThings done well.\n\n"
                "For each issue, include: line number, description, and a concrete fix."
            ),
            metadata={"category": "engineering", "language": language},
        )

    @staticmethod
    def marketing_copy() -> STCOPrompt:
        """Template for generating marketing copy."""
        return STCOPrompt(
            situation=(
                "You are a senior conversion copywriter specialising in {industry}. "
                "Your copy consistently achieves above-average click-through rates "
                "because you focus on specific benefits, not vague claims. Your tone "
                "is {tone} — never hyperbolic."
            ),
            task=(
                "Write {content_type} for the following product/feature: {product}. "
                "The primary goal is {goal}."
            ),
            context=(
                "Target audience: {audience}\n"
                "Key differentiators: {differentiators}\n"
                "Competitor positioning: {competitors}\n"
                "Constraints: {constraints}"
            ),
            output=(
                "Provide {num_variants} variants for A/B testing.\n"
                "For each variant include:\n"
                "- The copy itself\n"
                "- Rationale (1 sentence explaining the angle)\n"
                "- Predicted strength (which audience segment it targets)\n\n"
                "Format: Markdown with clear variant labels (Variant A, B, C...)."
            ),
            metadata={"category": "marketing"},
        )

    @staticmethod
    def data_analysis() -> STCOPrompt:
        """Template for data analysis tasks."""
        return STCOPrompt(
            situation=(
                "You are a senior data analyst at a {company_type} company. "
                "You report to {stakeholder} and your analyses directly inform "
                "{decision_type} decisions. You prioritise actionable insights "
                "over exhaustive statistics."
            ),
            task=(
                "Analyse the following data to answer: {analysis_question}\n\n"
                "Specifically:\n{specific_questions}"
            ),
            context=(
                "Data description: {data_description}\n"
                "Time period: {time_period}\n"
                "Known issues: {data_caveats}\n"
                "Data:\n{data}"
            ),
            output=(
                "Structure your response as:\n"
                "1. Executive Summary (3-4 sentences for {stakeholder})\n"
                "2. Key Findings (numbered list with supporting data)\n"
                "3. Detailed Analysis (with tables where appropriate)\n"
                "4. Recommendations (specific, actionable, prioritised)\n"
                "5. Caveats & Limitations\n\n"
                "Use British English. Include specific numbers, not vague qualifiers."
            ),
            metadata={"category": "analytics"},
        )

    @staticmethod
    def technical_documentation() -> STCOPrompt:
        """Template for writing technical documentation."""
        return STCOPrompt(
            situation=(
                "You are a technical writer creating {doc_type} documentation "
                "for {audience}. You follow the Diátaxis framework and prioritise "
                "clarity over comprehensiveness. You write in British English."
            ),
            task=(
                "Write a {doc_type} for {topic}. "
                "The reader should be able to {reader_goal} after reading this."
            ),
            context=(
                "Technology: {technology}\n"
                "Prerequisites: {prerequisites}\n"
                "Common pitfalls: {common_pitfalls}\n"
                "Related docs: {related_docs}"
            ),
            output=(
                "Format:\n"
                "- Title following the pattern: {title_pattern}\n"
                "- Prerequisites section\n"
                "- Step-by-step instructions (numbered)\n"
                "- Code examples in {code_languages}\n"
                "- 'Common Pitfalls' callout section\n"
                "- 'Next Steps' with links\n"
                "- Length: {target_length}"
            ),
            metadata={"category": "documentation"},
        )


# ---------------------------------------------------------------------------
# Prompt Registry (for managing templates across a project)
# ---------------------------------------------------------------------------

class PromptRegistry:
    """
    A registry for managing STCO prompt templates.
    
    Use this to centralise all prompts in your application,
    making them easy to version, test, and audit.
    """

    def __init__(self) -> None:
        self._templates: dict[str, STCOPrompt] = {}

    def register(self, name: str, template: STCOPrompt) -> None:
        """Register a template by name."""
        self._templates[name] = template

    def get(self, name: str) -> STCOPrompt:
        """Retrieve a registered template."""
        if name not in self._templates:
            available = ", ".join(self._templates.keys())
            raise KeyError(
                f"Template '{name}' not found. Available: {available}"
            )
        return self._templates[name]

    def list_templates(self) -> list[str]:
        """List all registered template names."""
        return list(self._templates.keys())

    def execute(self, name: str, temperature: float = 0, **variables: str) -> str:
        """Retrieve and execute a template in one call."""
        template = self.get(name)
        return template.execute(temperature=temperature, **variables)


# ---------------------------------------------------------------------------
# Main — Demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Set up a registry with pre-built templates
    registry = PromptRegistry()
    registry.register("code_review", STCOTemplates.code_review("Python"))
    registry.register("marketing", STCOTemplates.marketing_copy())
    registry.register("analysis", STCOTemplates.data_analysis())
    registry.register("docs", STCOTemplates.technical_documentation())

    print("Registered templates:", registry.list_templates())
    print()

    # Demo: Render a code review prompt (without executing)
    review_template = registry.get("code_review")
    rendered = review_template.render(
        language="Python",
        tech_stack="FastAPI, SQLAlchemy, PostgreSQL",
        code=(
            "def get_user(id):\n"
            "    return db.execute(f'SELECT * FROM users WHERE id = {id}')"
        ),
        additional_context="This handles PII data and must be GDPR compliant.",
    )

    print("=" * 60)
    print("RENDERED STCO PROMPT")
    print("=" * 60)
    print(rendered)
    print()

    # Demo: Build a custom STCO prompt from scratch
    custom = STCOPrompt(
        situation=(
            "You are a DevOps engineer responsible for a Kubernetes cluster "
            "running 50 microservices in production."
        ),
        task=(
            "Diagnose why the payment-service pod is experiencing OOMKilled "
            "restarts every 4-6 hours."
        ),
        context=(
            "Pod memory limit: 512Mi\n"
            "Current usage pattern: starts at 200Mi, grows linearly to 512Mi\n"
            "Language: Java 21 with Spring Boot 3.2\n"
            "Recent changes: Added Redis caching layer 3 days ago\n"
            "Heap dump shows growing HashMap entries in CacheManager"
        ),
        output=(
            "Provide:\n"
            "1. Most likely root cause\n"
            "2. Diagnostic commands to confirm\n"
            "3. Short-term fix (to stop the restarts now)\n"
            "4. Long-term fix (to prevent recurrence)\n"
            "Format as markdown with code blocks for commands."
        ),
    )

    print("=" * 60)
    print("CUSTOM STCO PROMPT")
    print("=" * 60)
    print(custom.render())
]]>
