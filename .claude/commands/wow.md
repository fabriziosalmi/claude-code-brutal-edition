---
name: wow
allowed-tools: ["AskUserQuestion"]
---

# /wow - Quick Wins & Best Practices

Get instant access to best practices, quick wins, and BRUTAL EDITION features.

## What This Command Does

Shows you **actionable quick wins** you can implement right now to improve your code quality, security, and development workflow.

## Categories

### 🚀 Quick Security Wins

1. **Check for hardcoded secrets**

   ```bash
   grep -r "API_KEY\s*=\s*['\"]" . --exclude-dir=node_modules
   grep -r "password\s*=\s*['\"]" . --exclude-dir=node_modules
   ```

2. **Validate .env setup**

   ```bash
   # Ensure .env is in .gitignore
   grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore

   # Copy .env.example if it exists
   [ -f .env.example ] && cp .env.example .env
   ```

3. **Enable pre-commit hooks**

   ```bash
   # Install pre-commit framework
   pip install pre-commit

   # Add to .pre-commit-config.yaml
   cat > .pre-commit-config.yaml << 'EOF'
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.5.0
       hooks:
         - id: check-added-large-files
         - id: check-json
         - id: check-yaml
         - id: detect-private-key
         - id: end-of-file-fixer
         - id: trailing-whitespace
   EOF

   pre-commit install
   ```

### ⚡ Quick Code Quality Wins

1. **Add type hints to Python functions**

   ```python
   # Before
   def process(data):
       return result

   # After
   from typing import List, Dict

   def process(data: List[str]) -> Dict[str, Any]:
       """Process data and return results."""
       return result
   ```

2. **Replace console.log with structured logging**

   ```typescript
   // Before
   console.log("User logged in:", user);

   // After
   logger.info("User authentication successful", {
     userId: user.id,
     timestamp: new Date().toISOString(),
   });
   ```

3. **Extract magic numbers**

   ```python
   # Before
   time.sleep(86400)

   # After
   SECONDS_PER_DAY = 86400
   time.sleep(SECONDS_PER_DAY)
   ```

### 🛡️ Quick Validation Wins

1. **Add input validation**

   ```python
   from hookify.utils.validation import InputValidator

   def process_file(path: str) -> str:
       errors = InputValidator.validate_file_path(path)
       if errors:
           raise ValueError(f"Invalid path: {errors[0].message}")

       with open(path, 'r') as f:
           return f.read()
   ```

2. **Use parameterized queries**

   ```python
   # Before - SQL INJECTION RISK!
   query = f"SELECT * FROM users WHERE id = {user_id}"

   # After - SAFE
   query = "SELECT * FROM users WHERE id = ?"
   cursor.execute(query, (user_id,))
   ```

3. **Validate environment variables on startup**

   ```python
   import os

   REQUIRED_VARS = ["API_KEY", "DATABASE_URL"]

   for var in REQUIRED_VARS:
       if not os.environ.get(var):
           raise ValueError(f"{var} environment variable is required")
   ```

### 📚 Quick Documentation Wins

1. **Remove condescending language**

   ```markdown
   <!-- Before -->

   Simply run: npm install
   Just add this line...

   <!-- After -->

   Run: npm install
   Add this line:
   ```

2. **Add .env.example**

   ```bash
   # Create template
   cat > .env.example << 'EOF'
   # Database Configuration
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname

   # API Keys
   API_KEY=your_api_key_here

   # Feature Flags
   ENABLE_FEATURE_X=false
   EOF
   ```

3. **Add README prerequisites**

   ```markdown
   ## Prerequisites

   - Node.js 18+ ([download](https://nodejs.org/))
   - Python 3.10+ ([download](https://python.org/))
   - PostgreSQL 14+ ([download](https://postgresql.org/))
   - 4GB RAM minimum
   - 2GB disk space
   ```

### 🎨 BRUTAL EDITION Features

1. **Structured logging framework**

   ```python
   from hookify.utils.logging import StructuredLogger

   logger = StructuredLogger("my-component")
   logger.info("Operation started", {"user_id": 123})
   logger.error("Operation failed", {"reason": "timeout"}, error=e)
   ```

2. **Input validation framework**

   ```python
   from hookify.utils.validation import InputValidator

   # Validate file paths
   errors = InputValidator.validate_file_path(path)

   # Validate bash commands
   errors = InputValidator.validate_bash_command(cmd)

   # Validate regex patterns
   errors = InputValidator.validate_regex_pattern(pattern)
   ```

3. **Configuration validation**

   ```python
   from hookify.utils.config_validation import ConfigValidator

   # Run all validations
   results = ConfigValidator.validate_all()

   if not results["valid"]:
       ConfigValidator.print_validation_report(results)
       sys.exit(1)
   ```

### 🔥 One-Liner Improvements

```bash
# Find all TODO comments
grep -rn "TODO\|FIXME\|XXX" . --exclude-dir=node_modules

# Find files without type hints
grep -L "from typing import" **/*.py

# Check for console.log in production
grep -rn "console\.log" src/ --exclude-dir=node_modules

# Find long functions (>50 lines)
awk '/^def |^function / { start=NR } /^$/ && start { if (NR-start > 50) print FILENAME":"start }' **/*.py

# Find hardcoded IPs
grep -rn "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" . --exclude-dir=node_modules
```

## BRUTAL EDITION Standards

All improvements should align with:

- **CODE_QUALITY_STANDARDS.md** - Code anti-patterns and SOTA patterns
- **DOCUMENTATION_STANDARDS.md** - Documentation guidelines
- **ENGINEERING_STANDARDS.md** - LLM coding standards

## Next Steps

After implementing quick wins:

1. Run quality checks:

   ```bash
   # Python
   pylint src/
   mypy src/
   bandit -r src/

   # TypeScript
   npm run lint
   npm run type-check
   ```

2. Set up CI/CD validation
3. Enable pre-commit hooks
4. Document improvements in CHANGELOG.md

---

**Pro tip:** Implement one quick win at a time, test thoroughly, then move to the next. Small, verified improvements compound into major quality gains.
