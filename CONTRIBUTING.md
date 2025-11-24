# Contributing Guidelines

Thank you for considering contributing to Claude Code! This document provides guidelines and standards for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and constructive in all interactions
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

Unacceptable behavior includes harassment, trolling, insulting comments, and personal attacks. Violations may result in removal from the project.

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Node.js**: Version 18 or higher ([download](https://nodejs.org/))
- **Git**: Version control system ([download](https://git-scm.com/))
- **Python**: Version 3.10+ (for plugin development)
- **A code editor**: VS Code recommended

### Forking the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-code.git
   cd claude-code
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/anthropics/claude-code.git
   ```

## Development Environment Setup

### Installing Dependencies

```bash
# Install Node.js dependencies
npm install

# For Python plugin development
pip install -r requirements-dev.txt  # If file exists
```

### Environment Variables

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Fill in required values in `.env`:
   - `ANTHROPIC_API_KEY`: Your API key from [console.anthropic.com](https://console.anthropic.com/)
   - Other variables as needed for your development

**CRITICAL**: Never commit `.env` files or hardcoded secrets.

### Verify Setup

```bash
# Run tests to verify setup
npm test

# For plugins
cd plugins/hookify
python -m pytest tests/
```

## Code Standards

This project follows strict code quality standards. Please review:

- [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) - Code anti-patterns and best practices
- [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) - Documentation guidelines

### Key Requirements

#### All Code

- No hardcoded secrets or credentials
- No magic numbers (use named constants)
- Explicit error handling (no empty catch blocks)
- Structured logging for observability
- Input validation on all external data

#### Python

- Type hints on all public functions
- Docstrings following Google style
- Black formatting (`black --line-length 100`)
- Pylint score >= 8.0

#### TypeScript

- Strict TypeScript mode enabled
- ESLint passing with no warnings
- Prettier formatting
- JSDoc comments on public APIs

#### Documentation

- No condescending language ("simply", "just")
- Inclusive terminology (see DOCUMENTATION_STANDARDS.md)
- Prerequisites clearly stated with versions
- Code examples tested and working

## Testing Requirements

### Running Tests

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- path/to/test

# Run with coverage
npm test -- --coverage
```

### Writing Tests

All new features require tests:

1. **Unit Tests**: Test individual functions in isolation
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete user workflows

Minimum coverage requirements:

- New code: 80% coverage
- Critical paths: 100% coverage

### Test Quality

- Tests must be deterministic (no flaky tests)
- Use descriptive test names
- Include both success and failure cases
- Test edge cases and error conditions
- Mock external dependencies

Example:

```typescript
describe("InputValidator.validateFilePath", () => {
  it("should reject paths with traversal attempts", () => {
    const errors = InputValidator.validateFilePath("../etc/passwd");
    expect(errors).toHaveLength(1);
    expect(errors[0].message).toContain("Path traversal detected");
  });

  it("should accept valid workspace paths", () => {
    const errors = InputValidator.validateFilePath("/workspace/src/file.ts");
    expect(errors).toHaveLength(0);
  });
});
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:

   - Follow code standards
   - Add tests
   - Update documentation

3. **Run quality checks**:

   ```bash
   # TypeScript
   npm run lint
   npm run type-check
   npm test

   # Python
   black plugins/hookify/
   pylint plugins/hookify/
   pytest plugins/hookify/tests/
   ```

4. **Commit with clear messages**:

   ```bash
   git commit -m "feat: Add input validation for file paths

   - Implement allowlist-based path validation
   - Add tests for path traversal prevention
   - Update documentation with security notes

   Fixes #123"
   ```

   Use conventional commit prefixes:

   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation only
   - `refactor:` Code restructuring
   - `test:` Adding tests
   - `chore:` Maintenance tasks

### Submitting the PR

1. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**:

   - Use the PR template
   - Link related issues
   - Describe changes clearly
   - Add screenshots/examples if applicable

3. **PR Checklist**:
   - [ ] Tests passing
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Commit messages are clear
   - [ ] No merge conflicts
   - [ ] Reviewers assigned

### Review Process

- Maintainers will review within 3-5 business days
- Address review feedback promptly
- Keep PRs focused (one feature/fix per PR)
- Be open to suggestions and constructive criticism

### After Approval

- Squash commits if requested
- Ensure CI/CD pipeline passes
- Maintainer will merge when ready

## Issue Reporting

### Bug Reports

Use the `/bug` command in Claude Code or file a [GitHub issue](https://github.com/anthropics/claude-code/issues) with:

1. **Clear title**: Describe the bug concisely
2. **Steps to reproduce**: Exact steps to trigger the bug
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Node.js version
   - Claude Code version
6. **Logs/Screenshots**: Any relevant error messages

### Feature Requests

1. **Check existing issues**: Avoid duplicates
2. **Describe the use case**: Why is this needed?
3. **Propose solution**: How could this work?
4. **Consider alternatives**: What other approaches exist?

### Security Vulnerabilities

**DO NOT** open public issues for security vulnerabilities.

Follow the process in [SECURITY.md](./SECURITY.md):

- Report privately via [HackerOne](https://hackerone.com/anthropic-vdp/reports/new)
- Provide detailed reproduction steps
- Allow time for fix before disclosure

## Plugin Development

For developing new plugins, see:

- [plugins/README.md](./plugins/README.md) - Plugin overview
- [plugins/plugin-dev/](./plugins/plugin-dev/) - Plugin development guide

## Questions?

- **Discord**: Join the [Claude Developers Discord](https://anthropic.com/discord)
- **Discussions**: Use [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)
- **Documentation**: Read the [official docs](https://docs.anthropic.com/en/docs/claude-code/overview)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see [LICENSE.md](./LICENSE.md)).

---

Thank you for contributing to Claude Code! 🚀
