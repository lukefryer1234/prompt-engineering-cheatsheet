<![CDATA[# Contributing to Prompt Engineering Cheat Sheet

Thank you for your interest in contributing! This project aims to be the most comprehensive and practical prompt engineering reference available. Every contribution — from fixing a typo to adding a new technique — makes it better for the community.

## 📋 Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Code Style Guidelines](#code-style-guidelines)
- [Pull Request Process](#pull-request-process)
- [Adding a New Technique](#adding-a-new-technique)
- [Adding an Example](#adding-an-example)
- [Code of Conduct](#code-of-conduct)

---

## Ways to Contribute

### 🐛 Report Issues
- Found an error in an example? Open an issue.
- Code doesn't work with a specific model? Let us know.
- Technique description is unclear? We want to fix it.

### 💡 Suggest Techniques
- Know a prompting technique we haven't covered? Open a feature request.
- Have benchmarks comparing techniques? We'd love to include them.
- Found an academic paper with new evidence? Share it.

### 📝 Add Examples
- Working code examples in any language are welcome.
- Real-world use cases are especially valuable.
- Examples should be self-contained and runnable.

### 📖 Improve Documentation
- Clarify explanations.
- Fix grammar or spelling.
- Add diagrams or visual aids.
- Translate content.

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/prompt-engineering-cheatsheet.git
   cd prompt-engineering-cheatsheet
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/add-react-technique
   ```
4. **Make your changes** and test them
5. **Commit** with a clear message:
   ```bash
   git commit -m "Add ReAct prompting technique with Python example"
   ```
6. **Push** and **open a Pull Request**

---

## Code Style Guidelines

### Python Examples
- **Python 3.11+** with full type annotations
- Follow **PEP 8** (use `ruff` or `black` for formatting)
- Include **docstrings** for all functions and classes
- Add a **header comment** with:
  - Description of the technique
  - Requirements (`pip install ...`)
  - Usage instructions
  - Link to relevant guide on aipromptarchitect.co.uk
- Use the **OpenAI SDK** for consistency (unless demonstrating another provider)
- Make examples **runnable** — someone should be able to `python your_example.py`

### TypeScript Examples
- **Strict TypeScript** — no `any` types
- Use **ESLint** recommended rules
- Include **JSDoc comments** for public functions

### Markdown
- Use **ATX-style headers** (`#`, `##`, `###`)
- Include a **Table of Contents** for documents longer than 3 sections
- Use **fenced code blocks** with language specification
- Wrap lines at **80 characters** for readability in diffs

---

## Pull Request Process

1. **Ensure your code works** — test all examples before submitting
2. **Update the README** if you've added a new technique or example
3. **Fill out the PR template** with:
   - What you changed and why
   - How to test the changes
   - Any related issues
4. **Wait for review** — we aim to review PRs within 48 hours
5. **Address feedback** — we may ask for changes before merging

### PR Checklist
- [ ] Code runs without errors
- [ ] Type hints included (Python/TypeScript)
- [ ] Docstrings/comments added
- [ ] README updated if applicable
- [ ] No API keys or secrets in code
- [ ] Tested with at least one model

---

## Adding a New Technique

If you're adding a new prompting technique:

1. **Add it to the Quick Reference Table** in `README.md`
2. **Add a Deep Dive section** if the technique warrants detailed explanation
3. **Create an example file** in `examples/` if applicable
4. **Include references** — link to the original paper or documentation
5. **Show when to use it** — and when *not* to use it

### Template for a new technique:

```markdown
### [Technique Name]

[2-3 sentence explanation of what it does and why it works]

**When to use:** [Specific scenarios]
**When NOT to use:** [Anti-patterns]

```python
# Working code example
```

**Key findings:** [Brief summary of evidence/benchmarks]
**Reference:** [Link to original paper or documentation]
```

---

## Adding an Example

Examples should be:
- **Self-contained** — one file, minimal dependencies
- **Well-commented** — explain the *why*, not just the *what*
- **Practical** — solve a real problem, not a toy example
- **Safe** — no hardcoded API keys, use environment variables

### Example file template:

```python
"""
[Technique Name] Example
========================

[Brief description of what this example demonstrates.]

Learn more: https://aipromptarchitect.co.uk/guides/[relevant-guide]

Requirements:
    pip install openai

Usage:
    export OPENAI_API_KEY="sk-..."
    python [filename].py
"""

from openai import OpenAI

client = OpenAI()

# Your example code here...

if __name__ == "__main__":
    # Runnable demo
    pass
```

---

## Code of Conduct

We are committed to providing a welcoming and harassment-free experience for everyone. By participating in this project, you agree to:

- **Be respectful** — disagreements about techniques are fine; personal attacks are not
- **Be constructive** — suggest improvements, don't just criticise
- **Be inclusive** — welcome newcomers and help them get started
- **Be honest** — if a technique has limitations, say so

Violations can be reported to the maintainers. We reserve the right to remove content or ban contributors who violate these principles.

---

## Questions?

- **Technical questions about prompt engineering:** Visit our [guides](https://aipromptarchitect.co.uk/guides/best-ai-prompt-techniques)
- **Questions about contributing:** Open a [Discussion](https://github.com/lukefryer1234/prompt-engineering-cheatsheet/discussions)
- **General enquiries:** Visit [aipromptarchitect.co.uk](https://aipromptarchitect.co.uk)

---

This project is maintained by [AI Prompt Architect](https://aipromptarchitect.co.uk). Visit our [guides](https://aipromptarchitect.co.uk/guides/best-ai-prompt-techniques) for comprehensive prompt engineering resources.
]]>
