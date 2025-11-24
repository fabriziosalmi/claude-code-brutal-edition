# Claude Code Engineering Standards Enforcement

This document provides **system-level guidance** for Claude Code's LLM to ensure all generated code follows enterprise-level engineering standards and avoids "vibecoding" anti-patterns.

## Core Principles

When generating code, Claude Code MUST:

1. **Never compromise security** - No hardcoded secrets, SQL injection, or command injection
2. **Fail explicitly** - No silent failures or empty catch blocks
3. **Validate all input** - Use allowlist-based validation, never trust user input
4. **Log structured data** - Use JSON logging, not console.log/print
5. **Document assumptions** - Explain WHY, not just WHAT
6. **Use inclusive language** - main/replica, allowlist/denylist, validation check

## Critical Security Rules (MUST NEVER VIOLATE)

### 1. Secret Management

```python
# ❌ NEVER DO THIS
API_KEY = "sk-abc123xyz"
password = "admin123"
db_url = "postgres://user:pass@localhost/db"

# ✅ ALWAYS DO THIS
import os
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required. See .env.example")
```

### 2. SQL Injection Prevention

```python
# ❌ NEVER DO THIS
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ✅ ALWAYS DO THIS
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### 3. Command Injection Prevention

```python
# ❌ NEVER DO THIS
os.system(f"rm -rf {user_path}")
command = f"git commit -m '{user_message}'"

# ✅ ALWAYS DO THIS
subprocess.run(["rm", "-rf", validated_path], check=True)
subprocess.run(["git", "commit", "-m", user_message], check=True)
```

### 4. Input Validation

```python
# ❌ NEVER DO THIS
def process_file(path):
    with open(path) as f:  # No validation!
        return f.read()

# ✅ ALWAYS DO THIS
from hookify.utils.validation import InputValidator

def process_file(path: str) -> str:
    errors = InputValidator.validate_file_path(path)
    if errors:
        raise ValueError(f"Invalid file path: {errors[0].message}")

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
```

## Code Quality Rules (MUST FOLLOW)

### 5. Error Handling - Explicit, Never Silent

```python
# ❌ NEVER DO THIS
try:
    risky_operation()
except:
    pass  # Silent failure

except Exception as e:
    pass  # Too generic

# ✅ ALWAYS DO THIS
from hookify.utils.logging import StructuredLogger

logger = StructuredLogger("component")

try:
    risky_operation()
except FileNotFoundError as e:
    logger.warning("File not found, using default", error=e)
    return default_value
except PermissionError as e:
    logger.error("Permission denied", error=e)
    raise  # Re-raise for caller
except (IOError, OSError) as e:
    logger.error("I/O error", {"operation": "risky_operation"}, error=e)
    raise
```

### 6. No Magic Numbers

```python
# ❌ NEVER DO THIS
time.sleep(86400)
if len(data) > 1048576:
    return

# ✅ ALWAYS DO THIS
SECONDS_PER_DAY = 86400
MAX_FILE_SIZE_BYTES = 1024 * 1024  # 1MB

time.sleep(SECONDS_PER_DAY)
if len(data) > MAX_FILE_SIZE_BYTES:
    return
```

### 7. Structured Logging, Not Debug Prints

```typescript
// ❌ NEVER DO THIS
console.log("Processing user:", userData);
print(f"Error: {error}")

// ✅ ALWAYS DO THIS
logger.info("Processing user request", { userId: userData.id });
logger.error("Operation failed", { operation: "processUser" }, error);
```

### 8. Type Hints and Documentation

```python
# ❌ NEVER DO THIS
def process(data):
    return result

# ✅ ALWAYS DO THIS
from typing import List, Dict, Optional

def process_items(
    items: List[str],
    config: Dict[str, Any],
    timeout: Optional[int] = None
) -> Dict[str, int]:
    """Process items with configuration.

    Args:
        items: List of item identifiers to process
        config: Configuration dictionary with processing parameters
        timeout: Optional timeout in seconds (default: no timeout)

    Returns:
        Dictionary mapping item IDs to result codes (0 = success)

    Raises:
        ValueError: If items list is empty
        TimeoutError: If operation exceeds timeout
    """
    if not items:
        raise ValueError("items list cannot be empty")
    # Implementation...
```

### 9. Function Complexity Limits

```python
# ❌ NEVER DO THIS - Function too long
def process_everything(a, b, c, d, e, f):  # >5 params, >50 lines
    # 200 lines of code doing everything
    pass

# ✅ ALWAYS DO THIS - Single Responsibility
@dataclass
class ProcessConfig:
    """Configuration for processing operations."""
    setting_a: str
    setting_b: int
    setting_c: bool

def process_data(data: List[str], config: ProcessConfig) -> Result:
    """Process data with configuration.

    Function is <50 lines, single purpose, clear parameters.
    """
    validated_data = _validate_data(data)
    transformed = _transform(validated_data, config)
    return _finalize(transformed)
```

### 10. No Commented-Out Code

```python
# ❌ NEVER DO THIS
def new_function():
    # Old implementation - keeping for reference
    # result = old_way(data)
    # if result:
    #     return result
    return new_way(data)

# ✅ ALWAYS DO THIS
def new_function():
    """Process data using the new algorithm.

    Note: Migrated from legacy implementation in commit abc123.
    See git history for previous approach.
    """
    return new_way(data)
```

## Documentation Rules (MUST FOLLOW)

### 11. No Condescending Language

```markdown
❌ NEVER WRITE:

- "Simply run this command..."
- "Just add this line..."
- "Obviously, you need to..."
- "It's easy to..."

✅ ALWAYS WRITE:

- "Run this command:"
- "Add this line:"
- "Configure the setting:"
- "To accomplish X, run Y:"
```

### 12. Inclusive Language

```markdown
❌ AVOID:

- master/slave → Use main/replica or primary/secondary
- blacklist/whitelist → Use denylist/allowlist
- sanity check → Use validation check or integrity check
- guys → Use team, folks, or everyone

✅ USE:

- main branch (not master)
- allowlist/denylist
- validation check
- team, folks, everyone
```

### 13. Precise Prerequisites

```markdown
❌ NEVER SAY:

- "Setup in 5 minutes"
- "Works out of the box"
- "No configuration needed"

✅ ALWAYS SPECIFY:

- "Prerequisites: Node.js 18+, 2GB RAM, 10 minutes setup time"
- "Required configuration: See .env.example"
- "System requirements: Python 3.10+, 4GB disk space"
```

### 14. Real Examples, No Placeholders

```markdown
❌ NEVER USE:

- Lorem ipsum dolor sit amet
- TODO: Add documentation here
- Coming soon...
- [Insert description]

✅ ALWAYS PROVIDE:

- Real, working code examples
- Complete documentation or don't include the section
- Actual descriptions and examples
```

## Architecture Rules (MUST FOLLOW)

### 15. Separation of Concerns

```python
# ❌ NEVER DO THIS - Mixed concerns
class UserController:
    def create_user(self, data):
        # Validation
        if not data.get('email'):
            return {"error": "invalid"}
        # Database access
        db.insert("users", data)
        # Email sending
        smtp.send(data['email'], "Welcome")
        # Logging
        print("User created")

# ✅ ALWAYS DO THIS - Separated concerns
class UserValidator:
    def validate(self, data: Dict) -> List[ValidationError]:
        """Validate user data."""
        pass

class UserRepository:
    def create(self, user: User) -> User:
        """Persist user to database."""
        pass

class EmailService:
    def send_welcome(self, email: str) -> None:
        """Send welcome email."""
        pass

class UserController:
    def __init__(
        self,
        validator: UserValidator,
        repository: UserRepository,
        email_service: EmailService,
        logger: StructuredLogger
    ):
        self.validator = validator
        self.repository = repository
        self.email_service = email_service
        self.logger = logger

    def create_user(self, data: Dict) -> Result[User]:
        """Create new user with validation and notifications."""
        errors = self.validator.validate(data)
        if errors:
            self.logger.warning("Validation failed", {"errors": errors})
            return Err(errors)

        user = self.repository.create(User.from_dict(data))
        self.logger.info("User created", {"user_id": user.id})

        self.email_service.send_welcome(user.email)
        return Ok(user)
```

### 16. Dependency Injection

```python
# ❌ NEVER DO THIS - Hard dependencies
class Service:
    def __init__(self):
        self.db = PostgresDatabase()  # Hardcoded dependency
        self.logger = ConsoleLogger()  # Can't test

# ✅ ALWAYS DO THIS - Injected dependencies
class Service:
    def __init__(
        self,
        database: Database,  # Interface
        logger: Logger        # Interface
    ):
        self.db = database
        self.logger = logger
```

## Testing Rules (MUST FOLLOW)

### 17. Meaningful Tests

```python
# ❌ NEVER DO THIS
def test_function():
    assert True == True  # Useless test

# ✅ ALWAYS DO THIS
def test_validate_file_path_rejects_traversal():
    """Validator should reject paths containing '..' for security."""
    errors = InputValidator.validate_file_path("../etc/passwd")

    assert len(errors) == 1
    assert errors[0].severity == "error"
    assert "traversal" in errors[0].message.lower()

def test_validate_file_path_accepts_workspace_paths():
    """Validator should accept valid paths within workspace."""
    errors = InputValidator.validate_file_path("/workspace/src/file.py")

    assert len(errors) == 0
```

## When to Apply These Rules

### ALWAYS:

- When generating new code files
- When modifying existing code
- When creating documentation
- When writing commit messages
- When suggesting fixes or improvements

### Context Awareness:

- If existing code violates these rules, suggest refactoring
- When editing existing files, match the existing style BUT add a comment suggesting migration to standards
- For quick fixes, apply minimum standards (no secrets, no SQL injection)
- For new features, apply all standards

## Enforcement Checklist

Before generating any code, verify:

- [ ] No hardcoded secrets or credentials
- [ ] No SQL/command injection vulnerabilities
- [ ] Input validation on all external data
- [ ] Structured logging instead of print/console.log
- [ ] Specific exception handling (no bare except)
- [ ] Type hints on public functions
- [ ] Docstrings explaining WHY and edge cases
- [ ] Named constants instead of magic numbers
- [ ] Functions <50 lines, <5 parameters
- [ ] No commented-out code
- [ ] Inclusive language in docs and comments
- [ ] No condescending language ("simply", "just")
- [ ] Prerequisites clearly stated
- [ ] Error messages are helpful and actionable

## References

See these files for complete standards:

- `/workspace/CODE_QUALITY_STANDARDS.md` - Code anti-patterns and SOTA patterns
- `/workspace/DOCUMENTATION_STANDARDS.md` - Documentation guidelines
- `/workspace/CONTRIBUTING.md` - Contribution process
- `/workspace/.env.example` - Environment variable template
