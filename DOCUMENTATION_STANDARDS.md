# Documentation Quality Standards

This document defines the quality standards and anti-patterns to avoid in all project documentation.

## Critical Anti-Patterns to Avoid

### 1. Condescending Language

❌ **NEVER USE:**

- "Simply..."
- "Just..."
- "Obviously..."
- "Clearly..."

✅ **USE INSTEAD:**

- Direct instructions without qualifiers
- "To do X, run Y"
- "Configure the setting by..."

### 2. Inclusive Language

❌ **AVOID:**

- "master/slave" → Use "main/replica" or "primary/secondary"
- "sanity check" → Use "validation check" or "integrity check"
- "guys" → Use "team", "folks", or "everyone"
- "blacklist/whitelist" → Use "denylist/allowlist"

### 3. Vague Promises

❌ **NEVER CLAIM:**

- "Setup in 5 minutes" (unless verified across environments)
- "Works out of the box"
- "Zero configuration required"

✅ **BE SPECIFIC:**

- "Setup requires: Node.js 18+, 2GB RAM, and 10 minutes"
- "Prerequisites: X, Y, Z"
- Document actual time and system requirements

### 4. Broken Links and References

- Run link checkers regularly
- Remove or update dead external links
- Don't reference internal company URLs in public docs
- Use relative paths for internal documentation

### 5. Hardcoded Secrets in Examples

❌ **NEVER:**

```bash
API_KEY="sk-abc123xyz"  # Real key in documentation
```

✅ **ALWAYS:**

```bash
API_KEY="your_api_key_here"  # Placeholder in documentation
```

### 6. AI-Generated Fluff

❌ **DELETE:**

- "In today's fast-paced digital world..."
- "Leveraging cutting-edge technology..."
- Generic introductions that add no technical value

✅ **START WITH:**

- Direct problem statement
- Technical context
- Actionable information

## Quality Checklist

- [ ] All prerequisites explicitly stated with versions
- [ ] Code examples actually run (tested)
- [ ] No condescending language ("simply", "just")
- [ ] Inclusive terminology (no master/slave, sanity, etc.)
- [ ] All links verified and working
- [ ] Alt text on all images (WCAG compliance)
- [ ] No hardcoded secrets in examples
- [ ] Environment variables documented in .env.example
- [ ] Error messages are helpful and specific
- [ ] Dates in ISO 8601 format (YYYY-MM-DD)
- [ ] Acronyms defined on first use
- [ ] Active voice preferred over passive
- [ ] Table of contents for docs >500 words
- [ ] Spell-checked with .cspell.json
- [ ] No Lorem Ipsum or placeholder text
- [ ] Setup time estimates realistic and tested

## Documentation Types

### README.md

Must include:

- Clear project description
- Prerequisites with versions
- Installation instructions (tested)
- Basic usage examples
- Link to full documentation
- License information
- How to report issues
- Contributing guidelines link

### CONTRIBUTING.md

Must include:

- Development environment setup
- How to run tests
- Code style guidelines
- PR submission process
- Review expectations

### SECURITY.md

Must include:

- How to report vulnerabilities privately
- Security policy
- Supported versions
- Response timeline expectations

### .env.example

Must include:

- All required environment variables
- Clear descriptions of each variable
- Example values (never real secrets)
- Security warnings
- Where to obtain credentials

## Accessibility Requirements

All documentation must be accessible according to WCAG 2.1 Level AA:

1. **Images**: Alt text describing content and purpose
2. **Links**: Descriptive text (not "click here")
3. **Color**: Never use color alone to convey information
4. **Headings**: Proper hierarchy (H1 → H2 → H3)
5. **Code**: Syntax highlighting with language specified
6. **Tables**: Header rows clearly marked

## Version Control

- Document breaking changes clearly
- Maintain CHANGELOG.md using Keep a Changelog format
- Use Semantic Versioning (SemVer)
- Archive old documentation instead of deleting
- Tag documentation versions with code releases

## Review Process

Before merging documentation changes:

1. Spell check (cspell)
2. Link validation
3. Markdown linting (markdownlint)
4. Accessibility check
5. Code example verification
6. Peer review for technical accuracy

## Maintenance

- Review quarterly for outdated information
- Update screenshots when UI changes
- Verify external links monthly
- Rotate example credentials/keys
- Archive deprecated features
