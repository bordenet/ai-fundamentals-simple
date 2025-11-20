# AI Fundamentals for Technical Leaders

Educational materials on AI concepts, terminology, and frameworks for engineering leaders.

## Overview

This repository contains documentation and guides covering AI fundamentals, with a focus on practical knowledge for technical decision-makers. Content includes explanations of LLM architecture, agentic AI systems, and enterprise integration patterns.

## Audience

- Engineering leaders evaluating AI adoption
- Technical staff learning AI concepts
- Teams planning AI integration

## Content

### Directory Structure

- `instructor/` - Topic guides on LLM foundations, agentic AI, MCP, RAG systems, and enterprise integration
- `docs/` - Reference materials and planning frameworks
- `notes/` - Technical deep-dives on transformers and inference

## Topics Covered

### LLM Foundations
- Transformer architecture and attention mechanisms
- Tokenization and context windows
- Training and fine-tuning approaches
- Enterprise AI tools (GitHub Copilot, CodeWhisperer, Claude, Azure OpenAI)

### Inference and Implementation
- Model serving architectures
- Optimization techniques
- API design for AI services
- Monitoring and observability

### Agentic AI
- LangGraph framework
- Agent design patterns
- Multi-agent coordination
- Tool integration

### Model Context Protocol (MCP)
- Architecture and design principles
- Context management
- Integration patterns

### RAG Systems
- Retrieval mechanisms
- Vector databases
- Hybrid search approaches

## References

### Papers
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer architecture
- [BERT](https://arxiv.org/abs/1810.04805) - Bidirectional transformers
- [GPT-3](https://arxiv.org/abs/2005.14165) - Large language models
- [RAG](https://arxiv.org/abs/2005.11401) - Retrieval-augmented generation

### Documentation
- [The Annotated Transformer](https://nlp.seas.harvard.edu/2018/04/03/attention.html)
- [HuggingFace Documentation](https://huggingface.co/docs)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)

## Getting Started

See `docs/getting_started.md` for orientation and `docs/course_agenda.md` for topic progression.

### Guides

- `instructor/01-llm-foundations.md` - LLM concepts and transformer architecture
- `instructor/02-agentic-ai.md` - Agentic AI systems and design patterns
- `instructor/03-mcp-implementation.md` - Model Context Protocol
- `instructor/04-rag-systems.md` - Retrieval Augmented Generation
- `instructor/05-enterprise-integration.md` - Enterprise AI strategy
- `instructor/06-pr-faq-validator.md` - Case study

## Development

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

### Commands

```bash
make test    # Run tests and linting
make lint    # Run flake8
make format  # Format code with black and isort
make clean   # Remove build artifacts
```

### Tools

- flake8 with plugins (docstrings, bugbear, comprehensions, simplify, pep8-naming)
- black (line length: 100)
- isort
- pytest
- pre-commit hooks

## License

CC0 1.0 Universal - See LICENSE file.
