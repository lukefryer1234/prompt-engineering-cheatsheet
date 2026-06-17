<![CDATA[<div align="center">

# 🧠 Prompt Engineering Cheat Sheet 2026 — Complete Reference

[![Stars](https://img.shields.io/github/stars/lukefryer1234/prompt-engineering-cheatsheet?style=flat-square&color=f6c700)](https://github.com/lukefryer1234/prompt-engineering-cheatsheet/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/lukefryer1234/prompt-engineering-cheatsheet?style=flat-square&color=brightgreen)](https://github.com/lukefryer1234/prompt-engineering-cheatsheet/commits/main)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-orange.svg?style=flat-square)](CONTRIBUTING.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/lukefryer1234/prompt-engineering-cheatsheet/pulls)

**The only prompt engineering reference you need.** Techniques, frameworks, code examples, and security patterns — all in one place.

[Quick Reference](#-quick-reference-table) · [Deep Dives](#-core-techniques-deep-dive) · [Examples](examples/) · [Security](#-prompt-injection-defence) · [Further Reading](#-further-reading)

</div>

---

## Why This Exists

Prompt engineering in 2026 is no longer about clever hacks — it's a core engineering discipline. With context windows exceeding 1M tokens, multi-modal reasoning, and structured output as a first-class feature, the gap between a naive prompt and an engineered one is the difference between a demo and a production system.

This cheat sheet distils the most impactful techniques into a quick reference you can use daily. Every technique includes working code, not just theory.

---

## 📋 Quick Reference Table

| Technique | When to Use | Complexity | Best For |
|-----------|------------|------------|----------|
| **Zero-Shot** | Simple, well-defined tasks | ⭐ | Classification, translation, summarisation |
| **Few-Shot** *(k-shot)* | Model needs output format examples | ⭐⭐ | Format-sensitive tasks, domain-specific outputs |
| **Chain of Thought (CoT)** | Multi-step reasoning required | ⭐⭐ | Maths, logic, planning, debugging |
| **Tree of Thought (ToT)** | Complex problems with multiple solution paths | ⭐⭐⭐⭐ | Strategy, creative problem-solving, game playing |
| **ReAct** *(Reason + Act)* | Tasks needing external tool use | ⭐⭐⭐ | Agents, research, data retrieval |
| **[STCO](STCO-FRAMEWORK.md)** *(Situation, Task, Context, Output)* | Structured prompt construction | ⭐⭐ | Any task needing consistent, high-quality output |
| **Self-Consistency** | High-stakes decisions needing reliability | ⭐⭐⭐ | Maths, factual QA, code generation |
| **Automatic Prompt Engineering (APE)** | Optimising prompts at scale | ⭐⭐⭐⭐ | Production systems, prompt tuning |
| **RAG** *(Retrieval-Augmented Generation)* | Knowledge-grounded responses | ⭐⭐⭐ | QA over documents, enterprise search |
| **Context Engineering** | Managing what goes into the context window | ⭐⭐⭐ | Long-context apps, multi-turn conversations |
| **Structured Output / JSON Mode** | Machine-readable responses needed | ⭐⭐ | APIs, data pipelines, tool use |
| **System Prompt Design** | Setting model behaviour & persona | ⭐⭐ | Chatbots, assistants, role-specific tools |
| **Prompt Chaining** | Complex workflows with dependencies | ⭐⭐⭐ | Multi-step generation, validation pipelines |
| **Role Prompting** | Domain expertise needed | ⭐ | Specialised analysis, creative writing |
| **Metacognitive Prompting** | Self-evaluation and reflection | ⭐⭐⭐ | Critical reasoning, bias detection |
| **Constrained Decoding** | Strict format requirements | ⭐⭐⭐ | Grammar-constrained output, regex-guided generation |

---

## 🔬 Core Techniques Deep Dive

### 1. Chain of Thought (CoT)

Chain of Thought prompting asks the model to show its reasoning process before arriving at an answer. This dramatically improves accuracy on tasks requiring multi-step reasoning.

**Zero-Shot CoT** — just add "Let's think step by step":

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": (
            "A farmer has 3 fields. The first field produces 240 kg of wheat, "
            "the second produces 1.5x the first, and the third produces half "
            "the second. What is the total production?\n\n"
            "Let's think step by step."
        )
    }]
)
print(response.choices[0].message.content)
```

```typescript
import OpenAI from "openai";

const client = new OpenAI();

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{
    role: "user",
    content: `A farmer has 3 fields. The first field produces 240 kg of wheat,
the second produces 1.5x the first, and the third produces half
the second. What is the total production?

Let's think step by step.`,
  }],
});
console.log(response.choices[0].message.content);
```

**Few-Shot CoT** — provide reasoning examples:

```python
COT_EXAMPLES = """
Q: Roger has 5 tennis balls. He buys 2 cans of 3 balls each. How many does he have?
A: Roger starts with 5 balls. He buys 2 cans × 3 balls = 6 balls. Total: 5 + 6 = 11. The answer is 11.

Q: A restaurant has 23 apples. They use 20 for lunch and buy 6 more. How many do they have?
A: They start with 23. After lunch: 23 - 20 = 3. After buying: 3 + 6 = 9. The answer is 9.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Solve problems step by step, showing your reasoning."},
        {"role": "user", "content": f"{COT_EXAMPLES}\nQ: {user_question}\nA:"}
    ]
)
```

→ See full example: [`examples/chain-of-thought.py`](examples/chain-of-thought.py)

---

### 2. Few-Shot Learning

Provide *k* examples to teach the model your expected input→output format.

```python
def few_shot_sentiment(text: str) -> str:
    """Classify sentiment using few-shot examples."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Classify the sentiment as positive, negative, or neutral."},
            # Example 1
            {"role": "user", "content": "The product exceeded my expectations!"},
            {"role": "assistant", "content": "positive"},
            # Example 2
            {"role": "user", "content": "Worst purchase I've ever made."},
            {"role": "assistant", "content": "negative"},
            # Example 3
            {"role": "user", "content": "It works as described, nothing special."},
            {"role": "assistant", "content": "neutral"},
            # Actual input
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content
```

```typescript
async function fewShotSentiment(text: string): Promise<string> {
  const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "Classify the sentiment as positive, negative, or neutral." },
      { role: "user", content: "The product exceeded my expectations!" },
      { role: "assistant", content: "positive" },
      { role: "user", content: "Worst purchase I've ever made." },
      { role: "assistant", content: "negative" },
      { role: "user", content: "It works as described, nothing special." },
      { role: "assistant", content: "neutral" },
      { role: "user", content: text },
    ],
    temperature: 0,
  });
  return response.choices[0].message.content!;
}
```

**Tips for effective few-shot:**
- Use 3–5 examples for most tasks (diminishing returns after 8)
- Include edge cases in your examples
- Keep examples representative of your actual distribution
- Order matters: put the most similar example last

---

### 3. STCO Framework

**STCO** (Situation → Task → Context → Output) is a structured framework for constructing prompts that consistently produce high-quality results. It eliminates the guesswork from prompt design.

```python
STCO_PROMPT = """
**Situation:** You are a senior Python developer conducting a code review
for a fintech startup that processes financial transactions.

**Task:** Review the following function for bugs, security vulnerabilities,
and performance issues. Suggest concrete improvements.

**Context:**
- This function handles payment processing for amounts up to £1M
- It runs in production serving 10,000 requests/minute
- The codebase uses Python 3.12, SQLAlchemy, and FastAPI
- PCI-DSS compliance is required

**Output:** Provide your review as a structured report with:
1. Critical issues (must fix before merge)
2. Warnings (should fix soon)
3. Suggestions (nice to have)
Each item should include the line number, issue description, and fix.
"""
```

→ Full guide: [**STCO-FRAMEWORK.md**](STCO-FRAMEWORK.md)

---

### 4. Structured Output

Force models to respond with valid JSON that matches your schema:

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class ReviewAnalysis(BaseModel):
    sentiment: str
    score: float
    key_topics: list[str]
    recommendation: str

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Analyse the product review and extract structured data."},
        {"role": "user", "content": "The laptop's battery life is incredible — 18 hours! But the keyboard feels cheap."}
    ],
    response_format=ReviewAnalysis,
)

analysis = response.choices[0].message.parsed
print(f"Sentiment: {analysis.sentiment}, Score: {analysis.score}")
print(f"Topics: {', '.join(analysis.key_topics)}")
```

```typescript
import OpenAI from "openai";
import { z } from "zod";
import { zodResponseFormat } from "openai/helpers/zod";

const ReviewSchema = z.object({
  sentiment: z.string(),
  score: z.number(),
  key_topics: z.array(z.string()),
  recommendation: z.string(),
});

const response = await client.beta.chat.completions.parse({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "Analyse the product review and extract structured data." },
    { role: "user", content: "The laptop's battery life is incredible — 18 hours! But the keyboard feels cheap." },
  ],
  response_format: zodResponseFormat(ReviewSchema, "review_analysis"),
});

const analysis = response.choices[0].message.parsed;
console.log(`Sentiment: ${analysis.sentiment}, Score: ${analysis.score}`);
```

→ See full example: [`examples/structured-output.py`](examples/structured-output.py)

---

### 5. Context Engineering

Context engineering is the discipline of designing what goes into the context window — selecting, ordering, and compressing information so the model has exactly what it needs.

**Key principles:**

| Principle | Description |
|-----------|------------|
| **Relevance Filtering** | Only include information directly relevant to the task |
| **Recency Bias** | Place most important context near the beginning and end of the prompt |
| **Chunking** | Break large documents into semantic chunks, not arbitrary splits |
| **Summarisation Layers** | Use progressive summarisation for long conversations |
| **Metadata Injection** | Add structured metadata (timestamps, sources, confidence scores) |

```python
def build_context(
    system_prompt: str,
    user_query: str,
    retrieved_docs: list[str],
    conversation_history: list[dict],
    max_context_tokens: int = 8000,
) -> list[dict]:
    """Build an optimised context window with priority-based inclusion."""
    messages = [{"role": "system", "content": system_prompt}]

    # 1. Always include recent conversation (last 5 turns)
    recent_history = conversation_history[-10:]  # 5 turns = 10 messages
    messages.extend(recent_history)

    # 2. Inject retrieved documents with source attribution
    if retrieved_docs:
        doc_context = "\n\n".join(
            f"[Source {i+1}]: {doc}" for i, doc in enumerate(retrieved_docs[:5])
        )
        messages.append({
            "role": "system",
            "content": f"Relevant documents:\n{doc_context}"
        })

    # 3. Add the user query last (recency bias)
    messages.append({"role": "user", "content": user_query})

    return messages
```

→ Deep dive: [Context Engineering Guide](https://aipromptarchitect.co.uk/guides/context-engineering)

---

## 🛡️ Prompt Injection Defence

Prompt injection is the #1 security risk in LLM applications. If your app takes user input and includes it in prompts, you need defences.

**Quick defence checklist:**
- ✅ Sanitise all user inputs before prompt inclusion
- ✅ Use XML/delimiter tagging to separate instructions from data
- ✅ Implement the sandwich defence pattern
- ✅ Add canary tokens to detect prompt extraction
- ✅ Use LLM-as-judge for high-stakes outputs
- ✅ Rate-limit and monitor for adversarial patterns

→ Full guide: [**INJECTION-DEFENCE.md**](INJECTION-DEFENCE.md)
→ See example: [`examples/injection-defence.py`](examples/injection-defence.py)

---

## 💻 IDE Integration — `.cursorrules`

Configure your AI coding assistant with prompt engineering best practices built in. The [`.cursorrules`](.cursorrules) file in this repo provides a production-ready template covering:

- STCO framework conventions for prompt templates
- Security-first defaults (injection defence, input sanitisation)
- Code style guidelines optimised for prompt engineering code
- Testing patterns for prompt validation

→ Full guide: [Ultimate .cursorrules Blueprint for Next.js](https://aipromptarchitect.co.uk/blog/ultimate-cursorrules-blueprint-nextjs)

---

## 📂 Examples

Runnable Python examples demonstrating each technique:

| File | Technique | Description |
|------|-----------|-------------|
| [`chain-of-thought.py`](examples/chain-of-thought.py) | CoT | Zero-shot, few-shot, and self-consistency CoT |
| [`structured-output.py`](examples/structured-output.py) | Structured Output | JSON mode with Pydantic models |
| [`stco-template.py`](examples/stco-template.py) | STCO | Programmatic STCO prompt builder |
| [`injection-defence.py`](examples/injection-defence.py) | Security | Sanitisation, canary tokens, sandwich defence |

```bash
# Install dependencies
pip install openai pydantic

# Set your API key
export OPENAI_API_KEY="sk-..."

# Run any example
python examples/chain-of-thought.py
```

---

## 📚 Further Reading

For comprehensive guides with benchmarks, interactive examples, and production patterns:

| Resource | Description |
|----------|-------------|
| [Complete Guide to AI Prompt Techniques](https://aipromptarchitect.co.uk/guides/best-ai-prompt-techniques) | In-depth guide covering every technique with real-world benchmarks |
| [Context Engineering Guide](https://aipromptarchitect.co.uk/guides/context-engineering) | How to design optimal context windows for production AI systems |
| [Prompt Engineering Evidence & Research](https://aipromptarchitect.co.uk/research/prompt-engineering-evidence) | Academic research and empirical evidence behind prompt engineering |
| [Prompt Injection Prevention](https://aipromptarchitect.co.uk/guides/prompt-injection-prevention) | Security-focused guide to defending against prompt injection attacks |
| [STCO Prompt Framework](https://aipromptarchitect.co.uk/guides/stco-prompt-framework) | Complete guide to the Situation-Task-Context-Output framework |
| [Ultimate .cursorrules Blueprint](https://aipromptarchitect.co.uk/blog/ultimate-cursorrules-blueprint-nextjs) | Production-grade .cursorrules configuration for Next.js projects |

---

## 🤝 Contributing

We welcome contributions! Whether it's a new technique, a better example, or a typo fix — see [**CONTRIBUTING.md**](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built and maintained by the team at **[AI Prompt Architect](https://aipromptarchitect.co.uk)** — the prompt engineering platform for professionals.

⭐ If this cheat sheet helped you, consider giving it a star!

</div>
]]>
