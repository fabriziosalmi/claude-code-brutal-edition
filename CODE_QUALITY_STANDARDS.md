# Code Quality Standards and Anti-Patterns

This document defines code quality standards and anti-patterns to avoid, ensuring the project maintains enterprise-level engineering practices.

## Critical Code Anti-Patterns (NEVER DO)

### 1. Hardcoded Secrets and Credentials

❌ **NEVER:**

```python
API_KEY = "sk-abc123xyz456"
DATABASE_URL = "postgres://user:password@localhost/db"
```

✅ **ALWAYS:**

```python
import os
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")
```

### 2. Empty Exception Handlers (Silent Failures)

❌ **NEVER:**

```python
try:
    dangerous_operation()
except:
    pass  # Silent failure
```

✅ **ALWAYS:**

```python
try:
    dangerous_operation()
except SpecificError as e:
    logger.error("Operation failed", error=e)
    # Take appropriate action: retry, fallback, or fail fast
    raise
```

### 3. Magic Numbers

❌ **NEVER:**

```python
time.sleep(86400)  # What is 86400?
if len(data) > 1048576:  # What is this limit?
```

✅ **ALWAYS:**

```python
SECONDS_PER_DAY = 86400
MAX_FILE_SIZE_BYTES = 1024 * 1024  # 1MB

time.sleep(SECONDS_PER_DAY)
if len(data) > MAX_FILE_SIZE_BYTES:
```

### 4. God Objects and Overly Complex Functions

❌ **NEVER:**

- Functions with >50 lines
- Functions with >5 parameters
- Classes with >1000 lines
- Files handling multiple unrelated concerns

✅ **ALWAYS:**

- Single Responsibility Principle
- Extract methods and classes
- Use composition over inheritance
- Limit function parameters (use objects/dataclasses for complex params)

### 5. Commented-Out Code

❌ **NEVER:**

```python
def process_data(data):
    # Old way - don't delete, might need later
    # result = legacy_process(data)
    # return result

    return new_process(data)
```

✅ **ALWAYS:**

- Use Git for version history
- Delete dead code
- Add comments explaining WHY, not WHAT

### 6. Debug Statements in Production

❌ **NEVER:**

```typescript
console.log("User data:", userData);  // Leaks PII to logs
print(f"Password: {password}")  // Security vulnerability
```

✅ **ALWAYS:**

```typescript
logger.debug("Processing user request", { userId: userData.id });
logger.info("Authentication successful"); // No sensitive data
```

### 7. String Concatenation for SQL/Shell Commands

❌ **NEVER:**

```python
query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection
command = f"rm -rf {user_input}"  # Command injection
```

✅ **ALWAYS:**

```python
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))

# For shell commands, use subprocess with list args
subprocess.run(["rm", "-rf", validated_path])
```

### 8. Global State and Mutable Defaults

❌ **NEVER:**

```python
global_config = {}  # Mutable global state

def add_item(item, items=[]):  # Mutable default argument
    items.append(item)
    return items
```

✅ **ALWAYS:**

```python
# Use configuration objects
config = Config.load()

def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## SOTA Engineering Patterns (DO THIS)

### 1. Structured Logging

```python
from hookify.utils.logging import StructuredLogger

logger = StructuredLogger("component_name")
logger.info("Operation completed", {
    "duration_ms": 150,
    "items_processed": 42
})
```

### 2. Input Validation (Allowlist, not Denylist)

```python
from hookify.utils.validation import InputValidator

errors = InputValidator.validate_file_path(user_path)
if errors:
    for error in errors:
        logger.error("Validation failed", {"error": error.message})
    raise ValueError("Invalid file path")
```

### 3. Explicit Error Handling

```python
try:
    result = risky_operation()
except FileNotFoundError as e:
    logger.warning("File not found, using default", error=e)
    result = default_value
except PermissionError as e:
    logger.error("Permission denied", error=e)
    raise  # Re-raise for caller to handle
except (IOError, OSError) as e:
    logger.error("I/O error", error=e)
    # Take recovery action
```

### 4. Configuration Validation

```python
from hookify.utils.config_validation import ConfigValidator

# Validate on startup
results = ConfigValidator.validate_all()
if not results["valid"]:
    ConfigValidator.print_validation_report(results)
    sys.exit(1)
```

### 5. Type Hints for Safety

```python
from typing import List, Dict, Optional

def process_items(
    items: List[str],
    config: Dict[str, Any],
    timeout: Optional[int] = None
) -> Dict[str, int]:
    """Process items with configuration.

    Args:
        items: List of item identifiers
        config: Configuration dictionary
        timeout: Optional timeout in seconds

    Returns:
        Dictionary mapping item IDs to result codes

    Raises:
        ValueError: If items list is empty
        TimeoutError: If operation exceeds timeout
    """
    pass
```

### 6. Idempotency Keys for Operations

```python
def apply_change(change_id: str, operation: Callable) -> None:
    """Apply change with idempotency guarantee.

    Args:
        change_id: Unique identifier for this change
        operation: Function to execute
    """
    if is_already_applied(change_id):
        logger.info("Change already applied", {"change_id": change_id})
        return

    operation()
    mark_applied(change_id)
```

### 7. Circuit Breaker for External Services

```python
class CircuitBreaker:
    """Prevents cascading failures when external service is down."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None

    def call(self, func: Callable) -> Any:
        if self.is_open():
            raise CircuitBreakerOpen("Service unavailable")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
```

### 8. Graceful Degradation

```python
def get_user_data(user_id: str) -> Dict[str, Any]:
    """Get user data with fallback to cached version."""
    try:
        return fetch_from_api(user_id)
    except (NetworkError, TimeoutError) as e:
        logger.warning("API unavailable, using cache", error=e)
        cached_data = get_from_cache(user_id)
        if cached_data:
            return cached_data
        raise  # No fallback available
```

## Code Review Checklist

Before merging code:

- [ ] No hardcoded secrets or credentials
- [ ] All exceptions handled explicitly (no bare `except:`)
- [ ] No magic numbers (use named constants)
- [ ] Functions are focused (<50 lines)
- [ ] No commented-out code
- [ ] No debug print/console.log statements
- [ ] SQL/shell commands use parameterization
- [ ] Type hints on public functions
- [ ] Docstrings on public APIs
- [ ] Input validation on external data
- [ ] Structured logging instead of print
- [ ] Error messages are helpful and specific
- [ ] No global mutable state
- [ ] Tests for critical logic paths
- [ ] No security vulnerabilities (linter passed)

## Automated Quality Tools

Use these tools to enforce standards:

### Python

```bash
# Type checking
mypy plugins/hookify/

# Linting
pylint plugins/hookify/
flake8 plugins/hookify/

# Security scanning
bandit -r plugins/hookify/

# Code formatting
black plugins/hookify/
isort plugins/hookify/
```

### TypeScript

```bash
# Type checking
tsc --noEmit

# Linting
eslint --ext .ts,.tsx .

# Security scanning
npm audit

# Code formatting
prettier --write "**/*.{ts,tsx,json}"
```

## Performance Considerations

### Memory Management

- Use generators for large datasets
- Close file handles explicitly (use context managers)
- Limit cache sizes (use `@lru_cache(maxsize=128)`)
- Avoid memory leaks (remove event listeners)

### Algorithmic Complexity

- Document Big-O complexity for critical paths
- Use appropriate data structures (sets for membership, dicts for lookups)
- Profile before optimizing
- Avoid premature optimization

### I/O Operations

- Batch operations when possible
- Use async/await for concurrent I/O
- Implement backpressure mechanisms
- Set reasonable timeouts

## Security Best Practices

1. **Validate All Input**: Never trust user input
2. **Use Allowlists**: Not denylists for validation
3. **Fail Securely**: Default to deny
4. **Log Security Events**: Audit trails for investigation
5. **Encrypt Sensitive Data**: At rest and in transit
6. **Rotate Credentials**: Regularly update secrets
7. **Principle of Least Privilege**: Minimal permissions needed
8. **Defense in Depth**: Multiple security layers

## Monitoring and Observability

### Structured Logging

- Use JSON format for machine parsing
- Include context (user_id, request_id, etc.)
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Never log sensitive data (passwords, API keys, PII)

### Metrics

- Track operation duration
- Count errors by type
- Monitor resource usage (CPU, memory, disk)
- Set up alerts for anomalies

### Tracing

- Use correlation IDs across services
- Implement distributed tracing (OpenTelemetry)
- Track request flows through system
- Identify bottlenecks and failures
