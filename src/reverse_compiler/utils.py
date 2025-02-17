"""
Utility functions for the Morley Reverse Compiler.
"""

def save_to_file(filename, content):
    """
    Saves generated Ladder Logic code to a .ll file.
    """
    with open(filename, "w") as f:
        f.write(content)

def load_plutus_script(filename):
    """
    Loads a Morley-specific Plutus script from a file.
    """
    with open(filename, "r") as f:
        return f.read()
