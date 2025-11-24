"""Structured logging utilities for hookify plugin.

Provides consistent, machine-readable logging with severity levels
and context information for operations, debugging, and monitoring.
"""

import json
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class LogLevel(Enum):
    """Log severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StructuredLogger:
    """Structured logger for outputting JSON-formatted logs."""

    def __init__(self, component: str, min_level: LogLevel = LogLevel.INFO):
        """Initialize structured logger.
        
        Args:
            component: Name of the component logging (e.g., 'rule_engine', 'pretooluse')
            min_level: Minimum log level to output
        """
        self.component = component
        self.min_level = min_level

    def _should_log(self, level: LogLevel) -> bool:
        """Check if message at given level should be logged."""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4
        }
        return level_order[level] >= level_order[self.min_level]

    def _log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None
    ) -> None:
        """Output structured log entry.
        
        Args:
            level: Log severity level
            message: Human-readable log message
            context: Additional structured context data
            error: Exception object if logging an error
        """
        if not self._should_log(level):
            return

        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.value,
            "component": self.component,
            "message": message
        }

        if context:
            log_entry["context"] = context

        if error:
            log_entry["error"] = {
                "type": type(error).__name__,
                "message": str(error)
            }

        # Write to stderr for logs (stdout reserved for hook output)
        print(json.dumps(log_entry), file=sys.stderr)

    def debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, context)

    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log info message."""
        self._log(LogLevel.INFO, message, context)

    def warning(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message."""
        self._log(LogLevel.WARNING, message, context)

    def error(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None
    ) -> None:
        """Log error message."""
        self._log(LogLevel.ERROR, message, context, error)

    def critical(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None
    ) -> None:
        """Log critical error message."""
        self._log(LogLevel.CRITICAL, message, context, error)
