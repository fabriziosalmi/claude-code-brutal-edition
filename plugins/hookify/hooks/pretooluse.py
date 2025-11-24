#!/usr/bin/env python3
"""PreToolUse hook executor for hookify plugin.

This script is called by Claude Code before any tool executes.
It reads .claude/hookify.*.local.md files and evaluates rules.
"""

import os
import sys
import json

# CRITICAL: Add plugin root to Python path for imports
# We need to add the parent of the plugin directory so Python can find "hookify" package
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT')
if PLUGIN_ROOT:
    # Add the parent directory of the plugin
    parent_dir = os.path.dirname(PLUGIN_ROOT)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Also add PLUGIN_ROOT itself in case we have other scripts
    if PLUGIN_ROOT not in sys.path:
        sys.path.insert(0, PLUGIN_ROOT)

try:
    from hookify.core.config_loader import load_rules
    from hookify.core.rule_engine import RuleEngine
    from hookify.utils.logging import StructuredLogger, LogLevel
except ImportError as e:
    # If imports fail, allow operation and log error
    error_msg = {
        "systemMessage": f"Hookify import error: {e}",
        "error": {
            "type": "ImportError",
            "message": str(e),
            "component": "pretooluse"
        }
    }
    print(json.dumps(error_msg), file=sys.stdout)
    sys.exit(0)


logger = StructuredLogger("pretooluse", min_level=LogLevel.INFO)


def main():
    """Main entry point for PreToolUse hook."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        logger.debug("PreToolUse hook triggered", {
            "tool_name": input_data.get("tool_name")
        })

        # Determine event type for filtering
        # For PreToolUse, we use tool_name to determine "bash" vs "file" event
        tool_name = input_data.get('tool_name', '')

        event = None
        if tool_name == 'Bash':
            event = 'bash'
        elif tool_name in ['Edit', 'Write', 'MultiEdit']:
            event = 'file'

        # Load rules
        rules = load_rules(event=event)
        
        logger.debug("Rules loaded", {"count": len(rules), "event": event})

        # Evaluate rules
        engine = RuleEngine()
        result = engine.evaluate_rules(rules, input_data)

        # Always output JSON (even if empty)
        print(json.dumps(result), file=sys.stdout)
        
        if result:
            logger.info("Hook matched rules", {
                "has_block": "hookSpecificOutput" in result,
                "has_warning": "systemMessage" in result and "hookSpecificOutput" not in result
            })

    except json.JSONDecodeError as e:
        # Invalid JSON input
        logger.error("Failed to parse hook input JSON", error=e)
        error_output = {
            "systemMessage": "Hookify error: Invalid JSON input"
        }
        print(json.dumps(error_output), file=sys.stdout)
    except FileNotFoundError as e:
        # Configuration file not found
        logger.warning("Configuration file not found", error=e)
        print(json.dumps({}), file=sys.stdout)
    except PermissionError as e:
        # Permission denied reading config
        logger.error("Permission denied reading configuration", error=e)
        error_output = {
            "systemMessage": "Hookify error: Permission denied"
        }
        print(json.dumps(error_output), file=sys.stdout)
    except Exception as e:
        # Catch-all for unexpected errors - allow operation but log
        logger.critical("Unexpected error in PreToolUse hook", error=e)
        error_output = {
            "systemMessage": f"Hookify error: {str(e)}"
        }
        print(json.dumps(error_output), file=sys.stdout)

    finally:
        # ALWAYS exit 0 - never block operations due to hook errors
        sys.exit(0)


if __name__ == '__main__':
    main()
