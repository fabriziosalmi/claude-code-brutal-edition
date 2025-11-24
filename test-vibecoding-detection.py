#!/usr/bin/env python3
"""
Test file to verify anti-vibecoding enforcement
This should trigger multiple warnings/blocks
"""

# ANTI-PATTERN 1: Hardcoded secrets (BLOCK)
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
AWS_KEY = "AKIA1234567890ABCDEF"
password = "MyPassword123!"

# ANTI-PATTERN 2: SQL Injection risk (BLOCK)
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # String interpolation
    return db.execute(query)

# ANTI-PATTERN 3: eval() with user input (BLOCK)
def calculate(expression):
    return eval(expression)  # Dangerous!

# ANTI-PATTERN 4: Magic numbers (WARN)
def process_data():
    time.sleep(300)  # What is 300?
    buffer = [0] * 1024  # What is 1024?
    return 42  # What is 42?

# ANTI-PATTERN 5: Poor error handling (WARN)
try:
    dangerous_operation()
except:  # Bare except
    pass  # Silent failure

# ANTI-PATTERN 6: Debug code (WARN)
print("Debug: user_id =", user_id)
console.log("This shouldn't be here")
debugger;

# ANTI-PATTERN 7: chmod 777 (BLOCK)
import os
os.chmod("/tmp/file", 0o777)

# ANTI-PATTERN 8: Hardcoded paths (WARN)
LOG_FILE = "C:\\Users\\Admin\\logs\\app.log"
CONFIG_PATH = "/home/fabrizio/config.json"
