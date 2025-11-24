# Claude Code - BRUTAL EDITION 🔥

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code) ![](https://img.shields.io/badge/BRUTAL-EDITION-red?style=flat-square&logo=github) ![](https://img.shields.io/badge/Enterprise-Grade-blue?style=flat-square)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

**Claude Code BRUTAL EDITION** is an enterprise-hardened fork that enforces zero-tolerance for "vibecoding" anti-patterns. Every line of code generated follows SOTA (State of the Art) engineering practices with built-in security validation, structured logging, and comprehensive quality standards.

Built on top of the original Claude Code agentic coding tool, this edition adds:
- ✅ **Zero hardcoded secrets** - Environment variables enforced
- ✅ **Zero SQL/command injection** - Input validation framework
- ✅ **Zero silent failures** - Explicit error handling required
- ✅ **SOTA patterns** - Circuit breakers, structured logging, idempotency
- ✅ **Enterprise documentation** - Inclusive language, no condescending tone
- ✅ **Security-first** - Allowlist validation, secrets management

> **Original Claude Code**: An agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows -- all through natural language commands.

**Learn more:**
- [Official Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [BRUTAL EDITION Repository](https://github.com/fabriziosalmi/claude-code-brutal-edition)

<img src="./demo.gif" />

## What Makes BRUTAL EDITION Different?

### 🛡️ Enterprise-Grade Engineering Standards

This edition enforces 300+ quality checks covering:

1. **Security Hardening**
   - No hardcoded secrets (validated via hooks)
   - SQL/Command injection prevention
   - Input validation with allowlist approach
   - Secrets management best practices

2. **Code Quality Enforcement**
   - Structured logging (JSON format)
   - Explicit error handling (no silent failures)
   - Type hints required on all public functions
   - Named constants (no magic numbers)
   - Function complexity limits (<50 lines, <5 params)

3. **Documentation Standards**
   - Inclusive language (main/replica, allowlist/denylist)
   - No condescending tone ("simply", "just")
   - Prerequisites clearly stated with versions
   - Real examples (no Lorem Ipsum)

4. **SOTA Architectural Patterns**
   - Circuit breaker pattern
   - Idempotency keys
   - Event sourcing capabilities
   - Graceful degradation
   - Dependency injection

See [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) and [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) for complete details.

## Get Started

1. Install Claude Code:

**MacOS/Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Homebrew (MacOS):**
```bash
brew install --cask claude-code
```

**Windows:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**NPM:**
```bash
npm install -g @anthropic-ai/claude-code
```

NOTE: If installing with NPM, you also need to install [Node.js 18+](https://nodejs.org/en/download/)

2. Navigate to your project directory and run `claude`.

3. **BRUTAL EDITION Banner**: On startup, you'll see the custom banner with quality standards enforcement active.

## BRUTAL EDITION Features

### Active Quality Enforcement

The BRUTAL EDITION includes several enforcement mechanisms:

- **Pre-commit Hooks**: Validates code before generation
- **Input Validation Framework**: `plugins/hookify/utils/validation.py`
- **Structured Logging**: `plugins/hookify/utils/logging.py`
- **Configuration Validation**: Ensures proper setup
- **Anti-Vibecoding Rules**: Real-time pattern detection

### New Documentation

- `CODE_QUALITY_STANDARDS.md` - 400+ lines covering all anti-patterns and SOTA solutions
- `DOCUMENTATION_STANDARDS.md` - Professional documentation guidelines
- `CONTRIBUTING.md` - Complete contribution workflow
- `.env.example` - Secure environment variable template
- `.claude/ENGINEERING_STANDARDS.md` - LLM guidance for code generation

### Validation Utilities

```python
# Input validation
from hookify.utils.validation import InputValidator

errors = InputValidator.validate_file_path(user_path)
errors += InputValidator.validate_bash_command(command)
errors += InputValidator.validate_regex_pattern(pattern)

# Structured logging
from hookify.utils.logging import StructuredLogger

logger = StructuredLogger("component")
logger.error("Operation failed", {"user_id": 123}, error=exception)
```

## Plugins

This repository includes several Claude Code plugins that extend functionality with custom commands and agents. See the [plugins directory](./plugins/README.md) for detailed documentation on available plugins.

## Reporting Bugs

We welcome your feedback. Use the `/bug` command to report issues directly within Claude Code, or file a [GitHub issue](https://github.com/fabriziosalmi/claude-code-brutal-edition/issues).

For the original Claude Code issues: [anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines on:
- Development environment setup
- Code quality standards
- Testing requirements
- Pull request process
- Security vulnerability reporting

## Connect on Discord

Join the [Claude Developers Discord](https://anthropic.com/discord) to connect with other developers using Claude Code. Get help, share feedback, and discuss your projects with the community.

## Data collection, usage, and retention

When you use Claude Code, we collect feedback, which includes usage data (such as code acceptance or rejections), associated conversation data, and user feedback submitted via the `/bug` command.

### How we use your data

See our [data usage policies](https://docs.anthropic.com/en/docs/claude-code/data-usage).

### Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information, restricted access to user session data, and clear policies against using feedback for model training.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).
