# AI Fundamentals for Technical Leaders

> **Created by Matt Bordenet, August 2025. Built with Claude Code.**

No-code AI curriculum for engineering leaders. Six modules covering LLMs, transformers, RAG, MCP, and enterprise integration. Read time: 4-6 hours total.

## Who This Is For

Engineering leaders who need to speak AI fluently in technical discussions and make informed adoption decisions. Covers what you need to know without requiring you to train models or write inference code.

**Assumptions:** You know software architecture. You've used GitHub Copilot or ChatGPT. You don't know why transformers work or how to evaluate RAG vs fine-tuning.

## What You'll Learn

After completing this curriculum:

1. **Explain transformer architecture** to your team (attention, tokens, context windows)
2. **Evaluate AI tools** for your stack (Copilot vs CodeWhisperer vs Claude vs Azure OpenAI)
3. **Recognize when RAG beats fine-tuning** and when neither is the right choice
4. **Understand MCP** and how agentic AI differs from chat interfaces
5. **Estimate costs and latency** for production AI deployments
6. **Identify AI security risks** specific to LLM-based systems

## Quick Start

```bash
# Start here
cat docs/getting_started.md

# Then work through modules in order
ls instructor/
# 01-llm-foundations.md      (45 min)
# 02-agentic-ai.md           (30 min)
# 03-mcp-implementation.md   (45 min)
# 04-rag-systems.md          (45 min)
# 05-enterprise-integration.md (30 min)
# 06-pr-faq-validator.md     (case study, 30 min)
```

## Curriculum

### Module 1: LLM Foundations (45 min)

How transformers work, why attention matters, what tokens actually are.

| Topic | You'll Understand |
|-------|-------------------|
| Attention mechanism | Why "Attention Is All You Need" changed NLP |
| Tokenization | Why GPT-4 charges per token, not per word |
| Context windows | Why 128K context costs more than 8K |
| Training vs inference | When to fine-tune, when to prompt-engineer |

### Module 2: Enterprise AI Tools (30 min)

Side-by-side comparison of tools your team is probably already using.

| Tool | Best For | Watch Out For |
|------|----------|---------------|
| GitHub Copilot | IDE integration, code completion | Training data concerns |
| Amazon CodeWhisperer | AWS-native, security scanning | Smaller model than Copilot |
| Claude (Anthropic) | Long documents, reasoning tasks | API rate limits |
| Azure OpenAI | Enterprise compliance, on-prem options | Complex pricing |

### Module 3: Agentic AI & MCP (45 min)

Agents aren't just chatbots. MCP is how they coordinate.

- LangGraph: Stateful workflows with decision trees
- Multi-agent patterns: When one LLM orchestrates others
- Tool calling: How agents execute code, query databases, call APIs
- MCP: The protocol for context sharing between agents

### Module 4: RAG Systems (45 min)

Retrieval-Augmented Generation: when to use it, how to build it.

| Approach | Use When | Avoid When |
|----------|----------|------------|
| RAG | Data changes frequently, need citations | Latency-critical (<100ms) |
| Fine-tuning | Stable domain, specific style needed | Data changes often |
| Prompt engineering | Quick iteration, small dataset | Complex reasoning required |

### Module 5: Enterprise Integration (30 min)

Production concerns: latency, cost, security, compliance.

- **Cost modeling**: GPT-4 at scale costs $X per 1M tokens (do the math for your volume)
- **Latency budgets**: Streaming vs batch, cold start penalties
- **Security**: Prompt injection, data leakage, output filtering
- **Compliance**: SOC2, HIPAA considerations for AI workloads

### Module 6: Case Study (30 min)

Real implementation: [pr-faq-validator](https://github.com/bordenet/pr-faq-validator) - a Go tool that scores documents without an LLM (deterministic), plus optional GPT-4 feedback.

---

## Repository Structure

```
ai-fundamentals-simple/
├── instructor/           # Main curriculum (6 modules)
├── docs/                 # Reference materials
│   ├── getting_started.md
│   ├── course_agenda.md
│   ├── enterprise-ai-tools.md
│   └── ai-first-transformation.md
└── Learnings/            # Supplemental deep-dives
```
## References

### Papers Worth Reading

| Paper | Why It Matters |
|-------|----------------|
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | The 2017 paper that started everything. Read the abstract and Section 3. |
| [BERT](https://arxiv.org/abs/1810.04805) | Bidirectional training explained |
| [GPT-3](https://arxiv.org/abs/2005.14165) | Where "emergent capabilities" became real |
| [RAG](https://arxiv.org/abs/2005.11401) | Original retrieval-augmented generation paper |

### Hands-On Resources

- [The Annotated Transformer](https://nlp.seas.harvard.edu/2018/04/03/attention.html) - Line-by-line code walkthrough
- [HuggingFace Docs](https://huggingface.co/docs) - Model hub and APIs
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction.html) - Agent framework

---

## License

MIT - See [LICENSE](LICENSE)

## Author

Matt Bordenet ([@bordenet](https://github.com/bordenet))