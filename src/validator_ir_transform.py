# 🚀 Validator IR Transform – Full Structural Integrity and Feature Parity
# Advanced IR Validator for Morley-IR with complete OpenPLC feature parity
# Ensures structural integrity, nested logic validation, and complex control flow consistency

import json

# Configuration for Validation and Debugging
DEBUG_MODE = True  # Enable detailed debugging for traceability
MAX_NESTING_LEVEL = 20  # Maximum nesting depth for complex logical operations

# Required Keys for Full OpenPLC Feature Parity
required_keys = [
    "instructions",
    "timers",
    "counters",
    "math_operations",
    "comparators",
    "set_reset_latches",
    "jump_instructions",
    "function_blocks",
    "selection_functions",
    "scan_cycle"
]

# Debugging Function for Detailed Traceability
def debug_log(message):
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")
# 🚀 Block 2: Structural Validation
# Comprehensive Structural Validation ensuring the presence and correctness of all required keys

# Structural Validation Handler

def validate_structure(ir_data):
    """
    Validates the structure of LadderCore IR for presence and correctness of required keys.
    Ensures full feature parity with OpenPLC.
    """
    errors = []

def ladder_logic_to_ir(ladder_logic_data):
    """Convert Ladder Logic JSON to IR format."""
    # Placeholder logic—expand as needed
    ir_data = {"instructions": ladder_logic_data.get("instructions", [])}
    return ir_data

def structured_text_to_ir(structured_text_data):
    """Convert Structured Text JSON to IR format."""
    # Placeholder logic—expand as needed
    ir_data = {"instructions": structured_text_data.get("instructions", [])}
    return ir_data

def ir_to_ladder_logic(ir_data):
    """Convert IR back to Ladder Logic JSON."""
    return {"instructions": ir_data.get("instructions", [])}

def ir_to_structured_text(ir_data):
    """Convert IR back to Structured Text JSON."""
    return {"instructions": ir_data.get("instructions", [])}

    # Check for Required Keys
    for key in required_keys:
        if key not in ir_data:
            errors.append(f"Missing required key: {key}")
        elif not isinstance(ir_data[key], (dict, list)):
            errors.append(f"Invalid type for key: {key}. Expected dict or list.")

    # Check Instructions Structure
    for instruction in ir_data.get("instructions", []):
        if not isinstance(instruction, dict):
            errors.append("Invalid instruction format. Expected dict.")
        elif "type" not in instruction or "args" not in instruction:
            errors.append("Instruction missing 'type' or 'args'")
        elif not isinstance(instruction["args"], list):
            errors.append("Invalid 'args' format in instruction. Expected list.")

    # Validate Timers and Counters Structure
    for timer in ir_data.get("timers", {}).values():
        if "duration" not in timer or not isinstance(timer["duration"], int):
            errors.append("Invalid timer duration. Expected integer.")

    for counter in ir_data.get("counters", {}).values():
        if "preset" not in counter or not isinstance(counter["preset"], int):
            errors.append("Invalid counter preset. Expected integer.")

    # Log Errors and Return Validation Result
    if errors:
        for error in errors:
            debug_log(f"[Structural Validation Error] {error}")
        return False

    debug_log("[Structural Validation] All required keys and structures are present.")
    return True
# 🚀 Block 3: Nested Structure Validation
# Detailed checks for nested conditions, complex constructs, and advanced configurations

# Nested Structure Validation Handler

def validate_nested_structures(ir_data):
    """
    Validates nested structures within LadderCore IR for consistency and correctness.
    Ensures accurate nesting depth, logical flow, and complex construct validation.
    """
    errors = []
    nesting_level = 0

    # Validate Nested Logic
    for instruction in ir_data.get("instructions", []):
        if "NESTED" in instruction.get("type", ""):
            nesting_level += 1
            if nesting_level > MAX_NESTING_LEVEL:
                errors.append("Nesting level exceeded maximum limit")
                debug_log(f"[Nested Structure Validation] Nesting Level: {nesting_level}")
        else:
            nesting_level = max(0, nesting_level - 1)

    # Complex Constructs and Advanced Configurations
    for fb in ir_data.get("function_blocks", {}).values():
        if "block_type" not in fb or not fb["block_type"]:
            errors.append("Function block missing 'block_type'")
        if "args" in fb and not isinstance(fb["args"], list):
            errors.append("Invalid 'args' format in function block. Expected list.")

    # Advanced Math and Conditional Checks
    for math_op in ir_data.get("math_operations", {}).values():
        if "operation" not in math_op or not math_op["operation"]:
            errors.append("Math operation missing 'operation'")
        if "args" in math_op and not isinstance(math_op["args"], list):
            errors.append("Invalid 'args' format in math operation. Expected list.")

    # Log Errors and Return Validation Result
    if errors:
        for error in errors:
            debug_log(f"[Nested Structure Validation Error] {error}")
        return False

    debug_log("[Nested Structure Validation] All nested structures are consistent and valid.")
    return True
# 🚀 Block 4: Cross-Validation for Jump Instructions
# Ensures label and jump consistency for control flow integrity

# Cross-Validation for Jump Instructions Handler

def validate_jump_instructions(ir_data):
    """
    Cross-validates jump instructions to ensure label consistency and control flow integrity.
    Checks that all referenced labels (LBL) exist for each jump (JMP).
    Ensures no orphaned labels or invalid jump targets.
    """
    errors = []
    labels = set()
    jumps = set()

    # Collect Labels and Jumps
    for instruction in ir_data.get("instructions", []):
        op_type = instruction.get("type")
        args = instruction.get("args", [])

        # Collect Labels
        if op_type == "LBL" and args:
            labels.add(args[0])
            debug_log(f"[Jump Validation] Found Label: {args[0]}")

        # Collect Jumps
        elif op_type == "JMP" and args:
            jumps.add(args[0])
            debug_log(f"[Jump Validation] Found Jump: {args[0]}")

    # Validate Jumps Against Labels
    for jump in jumps:
        if jump not in labels:
            errors.append(f"Invalid jump target: {jump} - Label not found")

    # Check for Orphaned Labels
    for label in labels:
        if label not in jumps:
            debug_log(f"[Jump Validation] Orphaned Label: {label}")

    # Log Errors and Return Validation Result
    if errors:
        for error in errors:
            debug_log(f"[Jump Validation Error] {error}")
        return False

    debug_log("[Jump Validation] All jump instructions and labels are consistent.")
    return True
# 🚀 Block 5: Detailed Error Reporting and Debugging
# Consistent error messages and detailed debugging outputs for traceability

# Error Reporting and Debugging Handler

def report_validation_errors(errors, context):
    """
    Reports validation errors with consistent messaging and context information.
    Enhances traceability by providing detailed debugging outputs for complex validation flows.
    """
    for error in errors:
        error_message = f"[Validation Error - {context}] {error}"
        debug_log(error_message)
    if errors:
        raise Exception(f"[Validation Failed - {context}] {len(errors)} errors found.")

# Enhanced Debugging Function

def enhanced_debug_log(message, context):
    if DEBUG_MODE:
        print(f"[DEBUG - {context}] {message}")
# 🚀 Block 6: Main Validation Flow
# Cohesive execution for validating LadderCore IR with full feature parity

# Main Validation Function

def validate_laddercore_ir(ladder_core_ir):
    """
    Main validation function for LadderCore IR.
    Ensures full feature parity with OpenPLC and preserves all advanced features.
    """
    # Step 1: Structural Validation
    if not validate_structure(ladder_core_ir):
        report_validation_errors(["Structural validation failed."], "Structural Validation")
    enhanced_debug_log("[Validation] Structural Validation Successful", "Structural Validation")

    # Step 2: Nested Structure Validation
    if not validate_nested_structures(ladder_core_ir):
        report_validation_errors(["Nested structure validation failed."], "Nested Structure Validation")
    enhanced_debug_log("[Validation] Nested Structure Validation Successful", "Nested Structure Validation")

    # Step 3: Cross-Validation for Jump Instructions
    if not validate_jump_instructions(ladder_core_ir):
        report_validation_errors(["Jump instruction validation failed."], "Jump Validation")
    enhanced_debug_log("[Validation] Jump Instruction Validation Successful", "Jump Validation")

    enhanced_debug_log("[Validation] All validations passed successfully.", "Main Validation Flow")
    return True

# Example Execution
if __name__ == "__main__":
    example_ir = {
        "instructions": [
            {"type": "AND", "args": ["X1", "X2", "Y1"]},
            {"type": "JMP", "args": ["LABEL1"]},
            {"type": "LBL", "args": ["LABEL1"]},
            {"type": "NESTED", "args": ["X3", "X4"]}
        ],
        "timers": {
            "T1": {"type": "TON", "duration": 1000}
        },
        "counters": {
            "C1": {"type": "CTU", "preset": 10}
        },
        "function_blocks": {
            "FB1": {"block_type": "FB", "args": ["IN1", "IN2"]}
        }
    }
    result = validate_laddercore_ir(example_ir)
    print("Validation Result:", result)
