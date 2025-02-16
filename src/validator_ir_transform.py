"""
Validator-Based IR Transformation - Enhanced
Ensures IR is structured correctly before being passed to the PlutusLadder Compiler.
"""

def validate_ir_structure(ir_data):
    """
    Checks the IR for missing components and structural integrity.
    """
    required_keys = ["instructions", "timers", "counters", "math_operations", "comparators", "set_reset_latches", "jump_instructions", "function_blocks"]
    for key in required_keys:
        if key not in ir_data:
            return False, f"Missing key: {key}"

    return True, "Valid IR Structure"

if __name__ == "__main__":
    example_ir = {
        "instructions": [{"type": "INPUT", "args": ["X1"]}],
        "timers": {},
        "counters": {},
        "math_operations": {},
        "comparators": {},
        "set_reset_latches": {},
        "jump_instructions": {},
        "function_blocks": {}
    }

    valid, message = validate_ir_structure(example_ir)
    print(f"Validation Result: {message}")
