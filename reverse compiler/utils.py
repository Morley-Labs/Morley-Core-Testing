# 📌 Utils: Comprehensive Helper Functions for Morley-IR
# Contains enhanced file handling, error logging, validation, and string manipulation utilities

import json
import os
from datetime import datetime

# Enhanced Save to File
def save_to_file(data, filename):
    """
    Save data to a file.
    Supports saving dictionaries, lists, and plain text with JSON serialization.
    """
    try:
        with open(filename, "w") as f:
            if isinstance(data, dict) or isinstance(data, list):
                json.dump(data, f, indent=2)
            else:
                f.write(data)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        log_error(f"Failed to save to {filename}: {str(e)}")

# Enhanced Load Plutus Script
def load_plutus_script(filename):
    """
    Loads a Morley-specific Plutus script from a file with error handling and logging.
    """
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        log_error(f"File not found: {filename}")
    except Exception as e:
        log_error(f"Failed to load Plutus script from {filename}: {str(e)}")
    return ""

# Enhanced Error Logging with Timestamps
def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")
    print(f"ERROR: {message}")

# File Validation
def validate_file(filename, file_type):
    if not os.path.exists(filename):
        log_error(f"{file_type} file not found: {filename}")
        return False
    if file_type == "Ladder Logic" and not filename.endswith(".ll"):
        log_error(f"Invalid Ladder Logic file extension: {filename}")
        return False
    if file_type == "Plutus" and not filename.endswith(".plutus"):
        log_error(f"Invalid Plutus file extension: {filename}")
        return False
    return True

# String Manipulation Helpers
def clean_line(line):
    return line.strip().replace("\t", " ")

def split_tokens(line):
    return line.split()

def is_comment(line):
    return line.startswith("--") or line.startswith("//")
