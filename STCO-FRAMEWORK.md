<![CDATA[# 🎯 STCO Prompt Framework — Complete Guide

A structured approach to writing prompts that consistently produce high-quality results.

**STCO** stands for **Situation → Task → Context → Output**. It's a four-part framework that eliminates ambiguity and gives language models exactly the information they need to deliver what you want.

---

## Table of Contents

- [Why STCO?](#why-stco)
- [The Four Components](#the-four-components)
- [Practical Examples](#practical-examples)
- [STCO vs Other Frameworks](#stco-vs-other-frameworks)
- [Tips for Maximum Effectiveness](#tips-for-maximum-effectiveness)
- [Programmatic Usage](#programmatic-usage)
- [Resources](#resources)

---

## Why STCO?

Most prompts fail for the same reasons:
- ❌ No clear role or perspective defined
- ❌ Vague task description
- ❌ Missing constraints or background
- ❌ No specification of desired output format

STCO addresses all four by giving you a repeatable structure. The framework works across any model (GPT-4o, Claude, Gemini, Llama) and any domain.

---

## The Four Components

### **S** — Situation

Set the scene. Define *who* the AI is, *what role* it's playing, and *what perspective* it should adopt.

The Situation grounds the model's behaviour. Without it, the model defaults to a generic assistant persona, which produces generic results.

**Good Situation statements:**
```
You are a senior backend engineer at a fintech company that processes 
50,000 transactions per second. You specialise in distributed systems 
and have 15 years of experience with high-availability architectures.
```

```
You are a clinical data analyst working for a pharmaceutical company. 
You are reviewing Phase III trial data for regulatory submission to the 
MHRA. You follow ICH E9 statistical guidelines.
```

**What to include:**
- Role / job title
- Domain expertise
- Organisation context
- Experience level
- Perspective or mindset

---

### **T** — Task

State *exactly* what needs to be done. Be specific about the action, scope, and any sub-tasks.

The Task should be unambiguous. If you can interpret it two ways, the model can interpret it twenty ways.

**Weak task:** "Review this code"
**Strong task:** "Review this Python function for security vulnerabilities, focusing on SQL injection, input validation, and authentication bypass. Flag each issue with a severity rating (critical/high/medium/low)."

**What to include:**
- The primary action (review, write, analyse, compare, generate)
- Scope boundaries (what to include, what to exclude)
- Specific aspects to focus on
- Any sub-tasks or steps

---

### **C** — Context

Provide the background information, constraints, and data the model needs to complete the task.

Context is where most prompts are under-specified. The model can't read your mind — if a constraint matters, state it explicitly.

**What to include:**
- Relevant data, code, or documents
- Technical constraints (language, framework, versions)
- Business constraints (budget, timeline, regulations)
- Audience (who will read the output)
- Previous decisions or attempts
- What you've already tried

---

### **O** — Output

Define the *exact format*, *structure*, *length*, and *tone* of the expected response.

Without an Output specification, you'll spend more time reformatting the response than the model spent generating it.

**What to include:**
- Format (markdown, JSON, bullet points, prose, table)
- Structure (sections, headings, specific fields)
- Length (word count, number of items)
- Tone (formal, conversational, technical)
- What to include/exclude in the response
- Examples of the desired output shape

---

## Practical Examples

### Example 1: Code Review

```
**Situation:** You are a principal engineer conducting a mandatory code review 
before a production deployment. The codebase is a Python 3.12 FastAPI service 
handling financial data subject to PCI-DSS compliance.

**Task:** Review the following pull request diff for:
1. Security vulnerabilities (especially injection and auth issues)
2. Performance concerns at scale (the service handles 5,000 req/s)
3. API contract violations against our OpenAPI spec
4. Missing error handling or edge cases

**Context:**
- Framework: FastAPI 0.115 with SQLAlchemy 2.0 ORM
- Database: PostgreSQL 16 with read replicas
- Auth: JWT tokens with RS256 signing, validated via middleware
- The function below is a new endpoint being added to the payments module
- We have 95% test coverage requirement; the PR includes tests

```python
@router.post("/payments/{payment_id}/refund")
async def process_refund(payment_id: str, amount: float, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment.amount < amount:
        raise HTTPException(400, "Refund exceeds payment")
    refund = Refund(payment_id=payment_id, amount=amount)
    db.add(refund)
    db.commit()
    return {"status": "refunded", "amount": amount}
```

**Output:** Structured review with:
- 🔴 Critical issues (block merge)
- 🟡 Warnings (should fix)
- 🟢 Suggestions (nice to have)
Each item: line reference, issue, severity, and concrete fix with code.
```

---

### Example 2: Marketing Copy

```
**Situation:** You are a conversion-focused copywriter for a B2B SaaS company 
selling an AI-powered prompt engineering platform. The brand voice is confident, 
technically credible, and approachable — not hype-driven.

**Task:** Write a landing page hero section (headline + subheading + CTA) for 
a new feature: an AI prompt analyser that scores prompts and suggests improvements.

**Context:**
- Target audience: software engineers and product managers at mid-size companies
- The feature analyses prompt quality across 12 dimensions (clarity, specificity, 
  context richness, output specification, etc.)
- Competitors position prompt engineering as "magic" — we position it as engineering
- Current conversion rate is 2.3%; we need to beat 3%
- A/B test: this will compete against "Upgrade Your Prompts with AI"

**Output:**
- Headline: Max 10 words, power word at the start
- Subheading: 20-30 words, addresses the pain point
- CTA button text: 3-5 words
- Provide 3 variants to A/B test
- Include a brief rationale for each variant (1 sentence)
```

---

### Example 3: Data Analysis

```
**Situation:** You are a data analyst at an e-commerce company that sells 
consumer electronics across the UK and EU. You report to the VP of Operations 
and your analyses directly inform inventory decisions.

**Task:** Analyse the following 6 months of sales data to identify:
1. Top 5 products by revenue with month-over-month growth trends
2. Products at risk of stockout (< 2 weeks inventory remaining)
3. Seasonal patterns that should inform Q3 purchasing
4. Any anomalies in the data that warrant investigation

**Context:**
- Data covers January-June 2026
- We use a rolling 30-day average for trend analysis
- Warehouse capacity is 85% full — we can't over-order
- Lead time from suppliers is 4-6 weeks
- Q3 historically sees a 15% dip before the September back-to-school spike
- Last year's Q3 stockout of wireless earbuds cost us £340K in lost revenue

[DATA TABLE WOULD GO HERE]

**Output:**
- Executive summary (3-4 sentences for the VP)
- Detailed findings table with columns: Product | Revenue | MoM Growth | 
  Inventory Status | Recommendation
- Risk alerts sorted by urgency
- Specific purchasing recommendations with quantities and timing
- Charts described in markdown (I'll create them in Excel)
```

---

### Example 4: Technical Documentation

```
**Situation:** You are a technical writer creating API documentation for a 
developer audience. The documentation follows the Diátaxis framework (tutorials, 
how-to guides, references, explanations).

**Task:** Write a "How-to Guide" for implementing webhook event handling in our 
payments API. Developers need to receive and process payment status change events 
(created, processing, succeeded, failed, refunded).

**Context:**
- API uses REST with JSON payloads, webhook events are signed with HMAC-SHA256
- SDK available in Python, TypeScript, and Go
- Common failure: developers forget to return 200 quickly and the webhook times out 
  (5-second timeout), leading to retries
- Events are delivered at-least-once — handlers must be idempotent
- Our docs site uses MDX with code tabs for multi-language examples

**Output:**
- Title following pattern: "How to [verb] [thing]"
- Prerequisites section (what they need before starting)
- Step-by-step instructions (numbered, 5-8 steps)
- Code examples in Python and TypeScript (use tabs)
- "Common pitfalls" callout box with the timeout and idempotency issues
- "Next steps" linking to related guides
- Length: 800-1200 words
```

---

## STCO vs Other Frameworks

| Framework | Components | Strengths | Weaknesses |
|-----------|-----------|-----------|------------|
| **STCO** | Situation, Task, Context, Output | Complete coverage, production-ready, natural flow | Slightly longer prompts |
| **CRISP** | Context, Role, Instructions, Specifics, Parameters | Good for simple tasks | Role and Context overlap |
| **RISEN** | Role, Instructions, Steps, End goal, Narrowing | Good for step-by-step tasks | Lacks output format specification |
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | Good for creative content | Over-indexes on style vs substance |
| **APE** | Auto-generated prompts | No manual effort | Black box, hard to debug |

**Why STCO wins for production use:**
1. **Situation** is more powerful than just "Role" — it includes organisational context, expertise level, and perspective
2. **Output specification** is a first-class component, not an afterthought
3. The framework maps directly to how engineering teams think about requirements
4. It's composable — you can template and programmatically generate STCO prompts

---

## Tips for Maximum Effectiveness

### 1. Be Specific in the Situation
❌ "You are a developer"
✅ "You are a senior TypeScript developer who specialises in React Server Components and has experience with streaming SSR in production"

### 2. Make Tasks Measurable
❌ "Improve this code"
✅ "Reduce the time complexity from O(n²) to O(n log n) while maintaining the existing API contract"

### 3. Context Should Include Constraints
❌ "Here's some data"
✅ "Here's Q2 sales data. Note: rows 15-22 contain incomplete records due to a system migration on March 3rd. Exclude these from trend analysis."

### 4. Output Specifications Should Be Exact
❌ "Give me a summary"
✅ "Provide a 3-paragraph summary: paragraph 1 = key findings, paragraph 2 = methodology concerns, paragraph 3 = recommended next steps. Use British English. No bullet points."

### 5. Iterate on the Weakest Component
If the output isn't right, identify which STCO component is weakest:
- Wrong perspective? → Fix **Situation**
- Wrong scope? → Fix **Task**
- Missing information? → Fix **Context**
- Wrong format? → Fix **Output**

---

## Programmatic Usage

STCO templates can be built programmatically for production systems:

```python
from dataclasses import dataclass

@dataclass
class STCOPrompt:
    situation: str
    task: str
    context: str
    output: str

    def render(self) -> str:
        return (
            f"**Situation:** {self.situation}\n\n"
            f"**Task:** {self.task}\n\n"
            f"**Context:** {self.context}\n\n"
            f"**Output:** {self.output}"
        )

# Create reusable templates
code_review = STCOPrompt(
    situation="You are a senior {language} developer reviewing code for production readiness.",
    task="Review the following code for {review_focus}.",
    context="Tech stack: {tech_stack}. Requirements: {requirements}.",
    output="Structured review with severity ratings. Format as markdown with code suggestions.",
)

# Render with specific values
prompt = code_review.render().format(
    language="Python",
    review_focus="security and performance",
    tech_stack="FastAPI, SQLAlchemy, PostgreSQL",
    requirements="PCI-DSS compliance, 99.9% uptime SLA",
)
```

→ See full example: [`examples/stco-template.py`](examples/stco-template.py)

---

## Resources

For a comprehensive interactive guide to STCO, visit **[AI Prompt Architect's STCO Framework Guide](https://aipromptarchitect.co.uk/guides/stco-prompt-framework)**.

### Related Resources

- [Complete Guide to AI Prompt Techniques](https://aipromptarchitect.co.uk/guides/best-ai-prompt-techniques) — covers all major techniques with benchmarks and comparisons
- [Context Engineering Guide](https://aipromptarchitect.co.uk/guides/context-engineering) — how to design optimal context windows
- [Prompt Engineering Evidence & Research](https://aipromptarchitect.co.uk/research/prompt-engineering-evidence) — academic research behind these techniques

---

<div align="center">

Built by the team at **[AI Prompt Architect](https://aipromptarchitect.co.uk)** — the prompt engineering platform for professionals.

</div>
]]>
