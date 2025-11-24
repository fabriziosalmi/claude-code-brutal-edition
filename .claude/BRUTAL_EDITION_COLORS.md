# BRUTAL EDITION Color Scheme

This document defines the official color scheme for Claude Code BRUTAL EDITION to ensure consistency across all terminal output, banners, and CLI interfaces.

## Color Palette

### Primary Colors

| Color              | Code      | ANSI Escape  | Usage                                            |
| ------------------ | --------- | ------------ | ------------------------------------------------ |
| **BRUTAL Magenta** | `#FF00FF` | `\033[1;35m` | Primary brand color, headers, important features |
| **BRUTAL Cyan**    | `#00FFFF` | `\033[1;36m` | Secondary color, information, dividers           |
| **BRUTAL Gold**    | `#FFD700` | `\033[1;33m` | Highlights, warnings, calls-to-action            |

### Status Colors (Standard)

| Color             | Code      | ANSI Escape  | Usage                                         |
| ----------------- | --------- | ------------ | --------------------------------------------- |
| **Success Green** | `#00FF00` | `\033[1;32m` | Success messages, checkmarks, completed items |
| **Error Red**     | `#FF0000` | `\033[1;31m` | Errors, critical warnings, failures           |
| **Info Gray**     | `#808080` | `\033[0;90m` | Secondary text, descriptions, hints           |
| **White**         | `#FFFFFF` | `\033[1;37m` | Primary text, headings                        |

### Background Colors (Use Sparingly)

| Color            | ANSI Escape | Usage                           |
| ---------------- | ----------- | ------------------------------- |
| Black Background | `\033[40m`  | For high-contrast text          |
| Reset            | `\033[0m`   | Always reset after colored text |

## Usage Guidelines

### DO ✓

- Use **BRUTAL Magenta** for brand elements (logos, headers)
- Use **BRUTAL Cyan** for informational elements (dividers, links)
- Use **BRUTAL Gold** for attention-grabbing elements (tips, warnings)
- Use **Green** only for success/completion indicators
- Use **Red** only for errors and critical issues
- Use **Gray** for secondary information
- Always reset colors with `\033[0m` after use

### DON'T ✗

- Don't mix random colors without purpose
- Don't use more than 3 colors in a single message
- Don't use color as the only indicator (accessibility)
- Don't use blue (reserved for links in some terminals)
- Don't use dim colors on dark terminals

## Code Examples

### Bash/Shell

```bash
# Define colors at top of script
BRUTAL_MAGENTA='\033[1;35m'
BRUTAL_CYAN='\033[1;36m'
BRUTAL_GOLD='\033[1;33m'
BRUTAL_GREEN='\033[1;32m'
BRUTAL_RED='\033[1;31m'
BRUTAL_GRAY='\033[0;90m'
BRUTAL_WHITE='\033[1;37m'
RESET='\033[0m'

# Usage
echo -e "${BRUTAL_MAGENTA}BRUTAL EDITION${RESET}"
echo -e "${BRUTAL_GREEN}✓${RESET} ${BRUTAL_GRAY}Task completed${RESET}"
echo -e "${BRUTAL_RED}✗${RESET} ${BRUTAL_GRAY}Operation failed${RESET}"
```

### Python

```python
# ANSI color codes
class Colors:
    BRUTAL_MAGENTA = '\033[1;35m'
    BRUTAL_CYAN = '\033[1;36m'
    BRUTAL_GOLD = '\033[1;33m'
    BRUTAL_GREEN = '\033[1;32m'
    BRUTAL_RED = '\033[1;31m'
    BRUTAL_GRAY = '\033[0;90m'
    BRUTAL_WHITE = '\033[1;37m'
    RESET = '\033[0m'

# Usage
print(f"{Colors.BRUTAL_MAGENTA}BRUTAL EDITION{Colors.RESET}")
print(f"{Colors.BRUTAL_GREEN}✓{Colors.RESET} {Colors.BRUTAL_GRAY}Success{Colors.RESET}")
```

### TypeScript/JavaScript

```typescript
// ANSI color codes
const COLORS = {
  BRUTAL_MAGENTA: "\x1b[1;35m",
  BRUTAL_CYAN: "\x1b[1;36m",
  BRUTAL_GOLD: "\x1b[1;33m",
  BRUTAL_GREEN: "\x1b[1;32m",
  BRUTAL_RED: "\x1b[1;31m",
  BRUTAL_GRAY: "\x1b[0;90m",
  BRUTAL_WHITE: "\x1b[1;37m",
  RESET: "\x1b[0m",
};

// Usage
console.log(`${COLORS.BRUTAL_MAGENTA}BRUTAL EDITION${COLORS.RESET}`);
console.log(`${COLORS.BRUTAL_GREEN}✓${COLORS.RESET} Success`);
```

## UI Component Guidelines

### Headers

```
BRUTAL_MAGENTA for main title
BRUTAL_CYAN for dividers (━━━)
BRUTAL_WHITE for subtitles
```

### Lists

```
BRUTAL_GREEN ✓ for completed items
BRUTAL_GOLD ⚡ for important items
BRUTAL_RED ✗ for failed items
BRUTAL_GRAY for description text
```

### Links

```
BRUTAL_MAGENTA for label (e.g., "Repository:")
BRUTAL_GOLD for URL
```

### Messages

```
BRUTAL_GREEN for success messages
BRUTAL_RED for error messages
BRUTAL_GOLD for warnings
BRUTAL_CYAN for information
BRUTAL_GRAY for hints/tips
```

## Examples in Context

### Success Message

```bash
echo -e "${BRUTAL_GREEN}✓${RESET} ${BRUTAL_GRAY}Operation completed successfully${RESET}"
echo -e "  ${BRUTAL_CYAN}→${RESET} ${BRUTAL_GRAY}Next: Run${RESET} ${BRUTAL_GOLD}npm test${RESET}"
```

### Error Message

```bash
echo -e "${BRUTAL_RED}✗${RESET} ${BRUTAL_WHITE}Build failed${RESET}"
echo -e "  ${BRUTAL_GRAY}Error:${RESET} ${BRUTAL_RED}Module not found${RESET}"
echo -e "  ${BRUTAL_CYAN}→${RESET} ${BRUTAL_GRAY}Solution: Run${RESET} ${BRUTAL_GOLD}npm install${RESET}"
```

### Information Block

```bash
echo -e "${BRUTAL_CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BRUTAL_MAGENTA}🚀 BRUTAL EDITION${RESET} ${BRUTAL_WHITE}v1.0.0${RESET}"
echo -e "${BRUTAL_CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  ${BRUTAL_GRAY}Feature:${RESET} ${BRUTAL_WHITE}Zero vibecoding anti-patterns${RESET}"
echo -e "  ${BRUTAL_GRAY}Status:${RESET} ${BRUTAL_GREEN}Enabled${RESET}"
```

## Accessibility Considerations

1. **Never use color alone** - Always pair with symbols (✓, ✗, ⚡, etc.)
2. **Sufficient contrast** - All colors chosen have high contrast ratios
3. **Fallback text** - Include text descriptions with colored output
4. **Terminal compatibility** - Test on both dark and light terminals

## Testing Colors

Run this test script to verify colors in your terminal:

```bash
#!/bin/bash
echo -e "\033[1;35m■ BRUTAL Magenta (Primary)\033[0m"
echo -e "\033[1;36m■ BRUTAL Cyan (Secondary)\033[0m"
echo -e "\033[1;33m■ BRUTAL Gold (Highlights)\033[0m"
echo -e "\033[1;32m■ Success Green\033[0m"
echo -e "\033[1;31m■ Error Red\033[0m"
echo -e "\033[0;90m■ Info Gray\033[0m"
echo -e "\033[1;37m■ White Text\033[0m"
```

## Version History

- **v1.0** (2025-11-24): Initial BRUTAL EDITION color scheme
  - Magenta primary, Cyan secondary, Gold highlights
  - Standard green/red for status
  - Gray for secondary text

---

**Maintain consistency**: When creating new terminal output, banners, or CLI features, always reference this color scheme to maintain the BRUTAL EDITION brand identity.
