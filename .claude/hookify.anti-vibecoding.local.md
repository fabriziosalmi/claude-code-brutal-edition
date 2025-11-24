---
name: anti-vibecoding-enforcement
enabled: true
event: all
action: warn
---

# Anti-Vibecoding Enforcement System

This hook enforces enterprise-level code quality standards by detecting and preventing common "vibecoding" anti-patterns before they enter the codebase.

## Critical Security Patterns (BLOCK)

When any of these patterns are detected, the operation will be **BLOCKED**:

### 1. Hardcoded Secrets Detection

- API keys matching patterns: `sk-[a-zA-Z0-9]{20,}`, `AKIA[0-9A-Z]{16}`
- Passwords in plain text
- Authentication tokens
- Private keys or certificates
- Database connection strings with credentials

### 2. SQL Injection Vulnerabilities

- String concatenation in SQL queries
- Unparameterized database queries
- Use of `eval()` or `exec()` with user input
- Direct string interpolation in ORM queries

### 3. Command Injection

- Shell command concatenation with user input
- Unescaped variables in bash commands
- `chmod 777` on any file
- `os.system()` or `subprocess.call()` with shell=True and user input

### 4. Committed Sensitive Files

- `.env` files checked into git
- `node_modules/` directory committed
- Credentials files (`.pem`, `.key`, `.p12`)
- IDE-specific settings with secrets (`.vscode/settings.json` with tokens)

### 5. XSS Vulnerabilities

- `innerHTML` without sanitization
- `dangerouslySetInnerHTML` in React without DOMPurify
- Direct DOM manipulation with user input
- eval() with string concatenation

### 6. Insecure Transport

- HTTP URLs for API endpoints (require HTTPS)
- Missing `rel="noopener noreferrer"` on external links with `target="_blank"`
- Unencrypted WebSocket connections (`ws://` instead of `wss://`)
- FTP instead of SFTP/SCP

## Code Quality Patterns (WARN)

These patterns trigger warnings with guidance:

### 7. Magic Numbers

- Unexplained numeric literals (except 0, 1, -1)
- Suggest using named constants
- Port numbers, timeouts, buffer sizes without explanation

### 8. Poor Error Handling

- Empty catch/except blocks
- Generic exception catching without re-throw
- Silent failures
- Using `|| {}` to hide errors
- `try-catch` wrapping entire functions

### 9. Debug Code in Production

- `console.log()` statements
- `print()` debugging
- `debugger;` statements
- `var_dump()`, `dd()`, or similar debugging functions

### 10. Code Organization Issues

- Functions >50 lines
- Files >1000 lines
- Functions with >5 parameters
- Deeply nested conditionals (>3 levels)
- Circular dependencies between modules
- Unused imports or variables
- Dead code (commented-out blocks)

### 11. Documentation Anti-Patterns

- Condescending language: "simply", "just", "obviously", "easily"
- Non-inclusive terminology: "master/slave", "sanity check", "blacklist/whitelist"
- Placeholder text: "TODO", "FIXME", "WIP" without tracking
- Missing documentation on public APIs
- Outdated comments contradicting code

### 12. Performance Anti-Patterns

- Infinite loops without exit conditions
- N+1 query patterns in database access
- Synchronous operations blocking event loop
- Memory leaks (event listeners not cleaned up)
- Large files loaded entirely into memory

### 13. File System Anti-Patterns

- Hardcoded absolute paths (`C:\Users\...`, `/home/user/...`)
- File names with spaces or special characters
- Missing file existence checks before operations
- No error handling on file I/O operations
- Using `rm -rf` without safeguards

### 14. Accessibility Violations

- Missing `alt` attributes on images
- No ARIA labels on interactive elements
- Color-only information conveyance
- Missing keyboard navigation support
- Disabled form elements without explanation

### 15. Developer Experience Issues

- No input validation feedback
- Missing loading states
- Error messages without context
- No confirmation for destructive actions
- "Coming Soon" placeholders in documentation

## Enforcement Strategy

This system provides:

1. **Real-time validation** during code generation
2. **Contextual guidance** on SOTA alternatives
3. **Educational feedback** explaining WHY the pattern is problematic
4. **Actionable suggestions** for immediate fixes

## SOTA Pattern Recommendations

When anti-patterns are detected, the system suggests:

- **Structured logging** instead of console.log (`StructuredLogger` with JSON output)
- **Input validation frameworks** instead of direct string concatenation (allowlist-based validation)
- **Named constants** instead of magic numbers (`const MAX_RETRIES = 3`)
- **Specific exception handling** instead of generic catches (`except ValueError as e:`)
- **Type hints and documentation** for all public APIs
- **Environment variables** for configuration (never hardcoded secrets)
- **Parameterized queries** for all database operations
- **Path validation** using allowlists (`os.path.normpath()` + validation)
- **Dependency injection** instead of circular imports
- **Semantic HTML** with ARIA labels for accessibility
- **Loading states** and error boundaries for better UX
- **Confirmation dialogs** for destructive operations
- **Comprehensive error messages** with actionable guidance

## Pattern Detection Examples

### ❌ BAD: Hardcoded credentials

```python
api_key = "sk-1234567890abcdef"
db_url = "postgres://user:password@localhost/db"
```

### ✅ GOOD: Environment variables

```python
import os
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable required")
```

### ❌ BAD: SQL injection risk

```javascript
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

### ✅ GOOD: Parameterized query

```javascript
const query = "SELECT * FROM users WHERE id = ?";
db.execute(query, [userId]);
```

### ❌ BAD: Magic number

```python
time.sleep(300)  # What is 300?
```

### ✅ GOOD: Named constant

```python
CACHE_TTL_SECONDS = 300
time.sleep(CACHE_TTL_SECONDS)
```

### ❌ BAD: Silent error

```python
try:
    result = dangerous_operation()
except:
    pass
```

### ✅ GOOD: Explicit error handling

```python
try:
    result = dangerous_operation()
except OperationError as e:
    logger.error("Operation failed", error=str(e), context={"operation": "dangerous"})
    raise
```
