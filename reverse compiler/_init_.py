# 📌 __init__.py for Morley-IR
# Main module initializer for core components and utilities

# Import core parsers and compilers
from .ll_parser import parse_ladder_logic
from .plutusladder_compiler import ll_to_plutus
from .reverse_plutusladder_compiler import plutus_to_ll, reverse_compile_plutus_to_ll

# Import utility functions
from .utils import (
    save_to_file,
    load_plutus_script,
    log_error,
    validate_file,
    clean_line,
    split_tokens,
    is_comment
)

# Module version
__version__ = "1.0.0"

# Exported symbols
__all__ = [
    "parse_ladder_logic",
    "ll_to_plutus",
    "plutus_to_ll",
    "reverse_compile_plutus_to_ll",
    "save_to_file",
    "load_plutus_script",
    "log_error",
    "validate_file",
    "clean_line",
    "split_tokens",
    "is_comment"
]
