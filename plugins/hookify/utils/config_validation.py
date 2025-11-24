"""
Configuration validation for hookify plugin.

Ensures all required environment variables and settings are properly configured
before the plugin executes. Prevents silent failures due to misconfiguration.
"""

import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ConfigError:
    """Represents a configuration error."""
    setting: str
    message: str
    severity: str  # "critical", "error", "warning"
    resolution: str  # How to fix


class ConfigValidator:
    """Validates plugin configuration and environment."""

    # Required environment variables
    REQUIRED_ENV_VARS = []  # Hookify doesn't require any env vars
    
    # Optional but recommended environment variables
    RECOMMENDED_ENV_VARS = {
        'CLAUDE_PLUGIN_ROOT': 'Required for Python imports to work correctly'
    }

    @staticmethod
    def validate_environment() -> List[ConfigError]:
        """Validate environment variables.
        
        Returns:
            List of configuration errors
        """
        errors = []

        # Check required variables
        for var in ConfigValidator.REQUIRED_ENV_VARS:
            if not os.environ.get(var):
                errors.append(ConfigError(
                    setting=var,
                    message=f"Required environment variable {var} is not set",
                    severity="critical",
                    resolution=f"Set {var} in your environment or .env file"
                ))

        # Check recommended variables
        for var, description in ConfigValidator.RECOMMENDED_ENV_VARS.items():
            if not os.environ.get(var):
                errors.append(ConfigError(
                    setting=var,
                    message=f"Recommended environment variable {var} is not set: {description}",
                    severity="warning",
                    resolution=f"Set {var} for optimal functionality"
                ))

        return errors

    @staticmethod
    def validate_plugin_structure() -> List[ConfigError]:
        """Validate plugin directory structure.
        
        Returns:
            List of configuration errors
        """
        errors = []
        
        plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
        if not plugin_root:
            return []  # Can't validate without knowing the root
            
        # Check required directories exist
        required_dirs = [
            'core',
            'hooks',
            'utils'
        ]
        
        for dir_name in required_dirs:
            dir_path = os.path.join(plugin_root, dir_name)
            if not os.path.isdir(dir_path):
                errors.append(ConfigError(
                    setting=f"directory:{dir_name}",
                    message=f"Required directory {dir_name} not found",
                    severity="error",
                    resolution=f"Ensure plugin structure is complete"
                ))
        
        # Check required files exist
        required_files = [
            'core/config_loader.py',
            'core/rule_engine.py',
            'hooks/pretooluse.py'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(plugin_root, file_path)
            if not os.path.isfile(full_path):
                errors.append(ConfigError(
                    setting=f"file:{file_path}",
                    message=f"Required file {file_path} not found",
                    severity="error",
                    resolution=f"Restore missing file from plugin repository"
                ))
                
        return errors

    @staticmethod
    def validate_permissions() -> List[ConfigError]:
        """Validate file permissions.
        
        Returns:
            List of configuration errors
        """
        errors = []
        
        plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
        if not plugin_root:
            return []
            
        # Check hook scripts are executable
        hook_scripts = [
            'hooks/pretooluse.py',
            'hooks/posttooluse.py',
            'hooks/stop.py',
            'hooks/userpromptsubmit.py'
        ]
        
        for script in hook_scripts:
            script_path = os.path.join(plugin_root, script)
            if os.path.isfile(script_path):
                if not os.access(script_path, os.X_OK):
                    errors.append(ConfigError(
                        setting=f"permissions:{script}",
                        message=f"Hook script {script} is not executable",
                        severity="error",
                        resolution=f"Run: chmod +x {script_path}"
                    ))
                    
        return errors

    @staticmethod
    def validate_all() -> Dict[str, Any]:
        """Run all validation checks.
        
        Returns:
            Dict with validation results:
            {
                "valid": bool,
                "errors": List[ConfigError],
                "warnings": List[ConfigError]
            }
        """
        all_errors = []
        
        # Run all validations
        all_errors.extend(ConfigValidator.validate_environment())
        all_errors.extend(ConfigValidator.validate_plugin_structure())
        all_errors.extend(ConfigValidator.validate_permissions())
        
        # Separate errors and warnings
        critical_errors = [e for e in all_errors if e.severity == "critical"]
        errors = [e for e in all_errors if e.severity == "error"]
        warnings = [e for e in all_errors if e.severity == "warning"]
        
        return {
            "valid": len(critical_errors) == 0 and len(errors) == 0,
            "critical": critical_errors,
            "errors": errors,
            "warnings": warnings
        }

    @staticmethod
    def print_validation_report(results: Dict[str, Any]) -> None:
        """Print human-readable validation report.
        
        Args:
            results: Results from validate_all()
        """
        print("\n=== Hookify Configuration Validation ===\n", file=sys.stderr)
        
        if results["valid"]:
            print("✓ Configuration is valid\n", file=sys.stderr)
        else:
            print("✗ Configuration has errors\n", file=sys.stderr)
            
        # Print critical errors
        if results["critical"]:
            print("CRITICAL ERRORS:", file=sys.stderr)
            for error in results["critical"]:
                print(f"  ✗ {error.setting}: {error.message}", file=sys.stderr)
                print(f"    Resolution: {error.resolution}\n", file=sys.stderr)
                
        # Print errors
        if results["errors"]:
            print("ERRORS:", file=sys.stderr)
            for error in results["errors"]:
                print(f"  ✗ {error.setting}: {error.message}", file=sys.stderr)
                print(f"    Resolution: {error.resolution}\n", file=sys.stderr)
                
        # Print warnings
        if results["warnings"]:
            print("WARNINGS:", file=sys.stderr)
            for warning in results["warnings"]:
                print(f"  ⚠ {warning.setting}: {warning.message}", file=sys.stderr)
                print(f"    Resolution: {warning.resolution}\n", file=sys.stderr)


if __name__ == '__main__':
    # Run validation when executed directly
    results = ConfigValidator.validate_all()
    ConfigValidator.print_validation_report(results)
    
    # Exit with error code if validation failed
    sys.exit(0 if results["valid"] else 1)
