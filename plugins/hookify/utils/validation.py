"""Input validation utilities for hookify plugin.

Provides validation functions to prevent injection attacks and ensure
data integrity according to security best practices.
"""

import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""
    field: str
    message: str
    severity: str  # "error", "warning"


class InputValidator:
    """Validates hook input data against security rules."""

    # Allowlist pattern for file paths - only allow safe characters
    # Alphanumeric, dots, dashes, underscores, forward slashes
    SAFE_PATH_PATTERN = re.compile(r'^[a-zA-Z0-9._/\-]+$')
    
    # Allowlist for regex patterns - prevent catastrophic backtracking
    MAX_REGEX_LENGTH = 500
    
    # Maximum sizes to prevent DoS
    MAX_COMMAND_LENGTH = 10000
    MAX_FILE_PATH_LENGTH = 4096
    MAX_TEXT_LENGTH = 1_000_000  # 1MB

    @staticmethod
    def validate_file_path(path: str) -> List[ValidationError]:
        """Validate file path for safety.
        
        Args:
            path: File path to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not path:
            errors.append(ValidationError(
                field="file_path",
                message="File path cannot be empty",
                severity="error"
            ))
            return errors
            
        if len(path) > InputValidator.MAX_FILE_PATH_LENGTH:
            errors.append(ValidationError(
                field="file_path",
                message=f"File path exceeds maximum length of {InputValidator.MAX_FILE_PATH_LENGTH}",
                severity="error"
            ))
            
        # Check for path traversal attempts
        if ".." in path:
            errors.append(ValidationError(
                field="file_path",
                message="Path traversal detected (..)",
                severity="error"
            ))
            
        # Warn on absolute paths outside workspace
        if path.startswith("/") and not path.startswith("/workspace"):
            errors.append(ValidationError(
                field="file_path",
                message="Absolute path outside workspace",
                severity="warning"
            ))
            
        return errors

    @staticmethod
    def validate_bash_command(command: str) -> List[ValidationError]:
        """Validate bash command for dangerous patterns.
        
        Args:
            command: Bash command to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not command:
            return errors
            
        if len(command) > InputValidator.MAX_COMMAND_LENGTH:
            errors.append(ValidationError(
                field="command",
                message=f"Command exceeds maximum length of {InputValidator.MAX_COMMAND_LENGTH}",
                severity="error"
            ))
            
        # Check for dangerous command patterns
        dangerous_patterns = [
            (r'\brm\s+-rf\s+/', "Recursive force delete from root"),
            (r'\bchmod\s+777', "Overly permissive file permissions"),
            (r'\beval\s+', "Arbitrary code execution via eval"),
            (r'\bcurl\s+.*\|\s*bash', "Piping remote scripts to bash"),
            (r'\bwget\s+.*\|\s*bash', "Piping remote scripts to bash"),
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                errors.append(ValidationError(
                    field="command",
                    message=f"Dangerous pattern detected: {description}",
                    severity="warning"
                ))
        
        return errors

    @staticmethod
    def validate_regex_pattern(pattern: str) -> List[ValidationError]:
        """Validate regex pattern for safety.
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not pattern:
            return errors
            
        if len(pattern) > InputValidator.MAX_REGEX_LENGTH:
            errors.append(ValidationError(
                field="pattern",
                message=f"Regex pattern exceeds maximum length of {InputValidator.MAX_REGEX_LENGTH}",
                severity="error"
            ))
            
        # Test if pattern compiles
        try:
            re.compile(pattern)
        except re.error as e:
            errors.append(ValidationError(
                field="pattern",
                message=f"Invalid regex pattern: {e}",
                severity="error"
            ))
            
        # Check for potentially dangerous patterns (catastrophic backtracking)
        if re.search(r'(\.\*){2,}|\(\.\+\){2,}', pattern):
            errors.append(ValidationError(
                field="pattern",
                message="Pattern may cause catastrophic backtracking",
                severity="warning"
            ))
            
        return errors

    @staticmethod
    def validate_text_length(text: str, field_name: str = "text") -> List[ValidationError]:
        """Validate text length to prevent DoS.
        
        Args:
            text: Text to validate
            field_name: Name of the field for error messages
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if len(text) > InputValidator.MAX_TEXT_LENGTH:
            errors.append(ValidationError(
                field=field_name,
                message=f"Text exceeds maximum length of {InputValidator.MAX_TEXT_LENGTH}",
                severity="error"
            ))
            
        return errors
