# Restoration - Block 1: Imports and Configuration
import os
import json
import re
from collections import deque

# Centralized Mappings for Reverse Compiler
logical_mappings = {"&&": "AND", "||": "OR"}

arithmetic_mappings = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}

comparison_mappings = {
    ">=": "GEQ",
    "<=": "LEQ",
    "==": "EQU",
    "!=": "NEQ",
    ">": "GRT",
    "<": "LES",
}

state_update_mappings = {"+=": "ADD", "-=": "SUB", "*=": "MUL", "/=": "DIV"}

bitwise_mappings = {"&": "AND_BIT", "|": "OR_BIT", "^": "XOR_BIT", "~": "NOT_BIT"}

# Supported operations for full OpenPLC feature parity, including nested logic
operations = {
    "logical_operations": ["AND", "OR", "XOR", "NOT"],
    "comparison_operations": ["EQU", "NEQ", "LES", "LEQ", "GRT", "GEQ"],
    "arithmetic_operations": ["ADD", "SUB", "MUL", "DIV", "MOD", "SQRT", "EXP", "MOV"],
    "bitwise_operations": [
        "AND_BIT",
        "OR_BIT",
        "XOR_BIT",
        "NOT_BIT",
        "SHL",
        "SHR",
        "ROR",
        "ROL",
    ],
    "timers_counters": ["TON", "TOF", "TP", "CTU", "CTD", "CTUD", "RTO", "RES"],
    "selection_functions": ["MUX", "LIMIT"],
    "jump_subroutine": ["JMP", "LBL", "JSR", "RET"],
    "function_blocks": ["SR", "RS", "SFB", "FB", "FC"],
    "coils_outputs": ["OTE", "OTL", "OTU"],
    "advanced_math": ["LN", "LOG", "SIN", "COS", "TAN", "ASIN", "ACOS", "ATAN"],
    "nested_logic": ["NAND", "NOR", "XNOR"],  # Added support for nested logic
}

# Configuration for advanced time logic, nested logic, and debugging
DEBUG_MODE = True  # Set to False for production
MAX_NESTING_LEVEL = 10  # Maximum nesting depth for complex logical operations
# Restoration - Block 2: Mappings Loader


def load_instruction_mappings():
    """Load instruction mappings for Ladder Logic, Structured Text, and Instruction Set"""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    instruction_set_path = os.path.join(base_path, "mappings", "instruction_set.json")
    ladder_logic_path = os.path.join(base_path, "mappings", "ladder_logic.json")
    structured_text_path = os.path.join(base_path, "mappings", "structured_text.json")

    # Debugging: Print paths to check correctness
    if DEBUG_MODE:
        print(f"Loading instruction set from: {instruction_set_path}")
        print(f"Loading ladder logic from: {ladder_logic_path}")
        print(f"Loading structured text from: {structured_text_path}")

    # Load the JSON files
    with open(instruction_set_path, "r", encoding="utf-8") as f:
        instruction_set = json.load(f)
    with open(ladder_logic_path, "r", encoding="utf-8") as f:
        ladder_logic = json.load(f)
    with open(structured_text_path, "r", encoding="utf-8") as f:
        structured_text = json.load(f)

    # Validate nested logic mappings
    if "nested_logic" not in instruction_set:
        raise ValueError("Nested logic mappings are missing in instruction_set.json")

    return instruction_set, ladder_logic, structured_text


# Initialize mappings
instruction_set, ladder_logic, structured_text = load_instruction_mappings()
# Restoration - Block 3: Parsing Logic

# Comparison Operator Mappings (Global Scope)
comparison_mappings = {
    ">=": "GEQ",
    "<=": "LEQ",
    "==": "EQU",
    "!=": "NEQ",
    ">": "GRT",
    "<": "LES",
}
control_flow_mappings = {
    "if": "IF",
    "else": "ELSE",
    "endif": "ENDIF",
    "while": "WHILE",
    "endwhile": "ENDWHILE",
    "for": "FOR",
    "endfor": "ENDFOR",
}


def map_comparison_operator(expression):
    """Maps comparison operators using centralized mappings"""
    for op, ladder_op in comparison_mappings.items():
        if op in expression:
            parts = expression.split(op)
            left_operand = parts[0].strip()
            right_operand = parts[1].strip()
            return f"XIC {left_operand} {ladder_op} {right_operand} OTE"
    return expression


def map_operations(expression, mappings):
    """Utility to map operations using predefined mappings"""
    for key, value in mappings.items():
        expression = expression.replace(key, value)
    return expression


def parse_plutus_script(plutus_code):
    """Extract conditions, state updates, nested logic, and advanced math from a Morley-specific Plutus script."""
    conditions = []
    state_changes = []
    arithmetic_operations = []
    bitwise_operations = []
    control_flow = []
    ladder_logic_lines = []
    nested_stack = deque(maxlen=MAX_NESTING_LEVEL)  # Support for nested logic

    lines = plutus_code.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match traceIfFalse for conditions
        condition_match = re.search(r'traceIfFalse "(.+?)" \((.+?)\)', line)
        if condition_match:
            message, condition = condition_match.groups()
            ladder_logic_lines.append(f"XIC {condition} OTE {message}")

        # Advanced Time Logic and Timestamp Anchoring
        if "mustValidateIn" in plutus_code:
            slot_match = re.search(r"mustValidateIn \(from slot(\d+)\)", plutus_code)
            if slot_match:
                slot_value = slot_match.group(1)
                if f"TON TimerX, {slot_value}ms" not in ladder_logic_lines:
                    ladder_logic_lines.append(f"TON TimerX, {slot_value}ms")

        # Verifiable Hash Handling
        if "Verifiable Hash" in plutus_code:
            hash_match = re.search(r"-- Verifiable Hash: (\w+)", plutus_code)
            if hash_match:
                hash_value = hash_match.group(1)
                if f"// Verifiable Hash: {hash_value}" not in ladder_logic_lines:
                    ladder_logic_lines.append(f"// Verifiable Hash: {hash_value}")

        # Advanced Math Operations
        if any(func in line for func in operations["advanced_math"]):
            math_match = re.search(
                r"(\w+) = (LN|LOG|SIN|COS|TAN|ASIN|ACOS|ATAN)\((\w+)\)", line
            )
            if math_match:
                output, func, operand = math_match.groups()
                ladder_logic_lines.append(f"MOV {output} = {func}({operand})")

        # Nested Logic Handling
        if any(nested in line for nested in operations["nested_logic"]):
            nested_stack.append(line)  # Push nested condition to stack
            ladder_logic_lines.append(f"NESTED LOGIC: {line}")  # Track in ladder logic
            control_flow.append(line)  # Track in control flow
            if DEBUG_MODE:
                print(f"Nested Logic Detected: {line}")

        # Tokenize and Initialize
        tokens = line.replace("(", "").replace(")", "").split()
        output = tokens[0]
        op1 = tokens[2] if len(tokens) > 2 else None
        op2 = tokens[4] if len(tokens) > 4 else None

        # Centralized and Ordered Mapping Flow
        for mapping in [
            logical_mappings,
            comparison_mappings,
            arithmetic_mappings,
            state_update_mappings,
            bitwise_mappings,
            control_flow_mappings
        ]:
            line = map_operations(line, mapping)
            tokens = line.replace("(", "").replace(")", "").split()  # Re-evaluate tokens

            # Track Mapped Operations
            if mapping == logical_mappings:
                conditions.append(line)
            elif mapping == comparison_mappings:
                conditions.append(line)  # Comparison ops are also conditions
            elif mapping == arithmetic_mappings:
                arithmetic_operations.append(line)
            elif mapping == state_update_mappings:
                state_changes.append(line)
            elif mapping == bitwise_mappings:
                bitwise_operations.append(line)
            elif mapping == control_flow_mappings:
                control_flow.append(line)

            # Append to Ladder Logic Lines
            ladder_logic_lines.append(
                f"XIC {op1} AND {op2} OTE {output}" if "AND" in line else
                f"XIC {op1} OR {op2} OTE {output}" if "OR" in line else
                f"XIC {op1} {op2} OTE {output}" if "XIC" in line else
                f"XIO {op1} OTE {output}"
            )

            # Apply Logical Mappings First
            if any(op in line for op in logical_mappings.keys()):
                line = map_operations(line, logical_mappings)
                tokens = line.replace("(", "").replace(")", "").split()  # Re-evaluate tokens
                op1 = tokens[2] if len(tokens) > 2 else None
                op2 = tokens[4] if len(tokens) > 4 else None
                conditions.append(line)
                ladder_logic_lines.append(
                f"XIC {op1} AND {op2} OTE {output}"
            if "AND" in line
            else (
                f"XIC {op1} OR {op2} OTE {output}"
            if "OR" in line
            else f"XIC {op1} OTE {output}"
            )
            )

            # Apply Comparison Mappings Next
            elif any(op in line for op in comparison_mappings.keys()):
                line = map_comparison_operator(line)
                tokens = line.replace("(", "").replace(")", "").split()  # Re-evaluate tokens
                op1 = tokens[2] if len(tokens) > 2 else None
                op2 = tokens[4] if len(tokens) > 4 else None
                conditions.append(line)
                ladder_logic_lines.append(f"XIC {op1} {op2} OTE {output}")

            # Apply Arithmetic Mappings
            elif any(op in line for op in arithmetic_mappings.keys()):
                line = map_operations(line, arithmetic_mappings)
                tokens = line.replace("(", "").replace(")", "").split()  # Re-evaluate tokens
                op1 = tokens[2] if len(tokens) > 2 else None
                op2 = tokens[4] if len(tokens) > 4 else None
                arithmetic_operations.append(line)
                ladder_logic_lines.append(
             f"ADD {output} = {op1} + {op2}"
            if "+" in line
            else (
            f"SUB {output} = {op1} - {op2}"
            if "-" in line
            else (
                f"MUL {output} = {op1} * {op2}"
                if "*" in line
                else f"DIV {output} = {op1} / {op2}"
            )
        )
    )

            # Apply State Update Mappings
            elif any(op in line for op in state_update_mappings.keys()):
                line = map_operations(line, state_update_mappings)
                tokens = line.replace("(", "").replace(")", "").split()  # Re-evaluate tokens
                op1 = tokens[2] if len(tokens) > 2 else None
                state_changes.append(line)
                ladder_logic_lines.append(f"MOV {output} = {op1}")

            # Apply Bitwise and Control Flow Mappings
            elif any(op in line for op in bitwise_mappings.keys()):
                line = map_operations(line, bitwise_mappings)
                bitwise_operations.append(line)
                ladder_logic_lines.append(line)
            elif any(op in line for op in control_flow_mappings.keys()):
                line = map_operations(line, control_flow_mappings)
                control_flow.append(line)
                ladder_logic_lines.append(line)

        # Default to XIO if no operation type is identified
        else:
            ladder_logic_lines.append(f"XIO {op1} OTE {output}")

        # Process Nested Logic Stack
        while nested_stack:
            nested_condition = nested_stack.pop()  # Pop the most nested condition
            ladder_logic_lines.append(f"NESTED LOGIC: {nested_condition}")
            ladder_logic_lines.append(nested_condition)  # Add the condition itself
            control_flow.append(nested_condition)  # Track in control flow
            print("[DEBUG] Ladder Logic Output (Before Flatten):", ladder_logic_lines)

            line = map_operations(line, control_flow_mappings)
            control_flow.append(line)

        # Apply Comparison Mappings
        if any(op in line for op in comparison_mappings.keys()):
            line = map_comparison_operator(line)

        nested_list = list(nested_stack)
        return "\n".join(nested_list)


def convert_to_ladder_logic(
    conditions,
    state_changes,
    arithmetic_operations,
    bitwise_operations,
    control_flow,
    nested_logic,
):
    """Convert extracted Plutus conditions, state updates, arithmetic, bitwise, control flow operations, and nested logic to Ladder Logic."""
    ladder_logic_code = []

    # Process conditions (XIC, XIO, TON, TOF)
    for condition in conditions:
        description, logic = condition
        if "timer" in description.lower():
            ladder_logic_code.append(f"{description}: {logic}")

    # Convert state updates to MOV instructions
    for update in state_changes:
        ladder_logic_code.append(f"MOV {update}")

    # Convert arithmetic operations
    for operation in arithmetic_operations:
        ladder_logic_code.append(operation)

    # Convert bitwise operations
    for operation in bitwise_operations:
        ladder_logic_code.append(operation)

    # Convert control flow operations
    for operation in control_flow:
        ladder_logic_code.append(operation)

    # Convert nested logic
    for nested in nested_logic:
        ladder_logic_code.append(f"NESTED LOGIC: {nested}")

    return (
        "\n".join(ladder_logic_code)
        if ladder_logic_code
        else "No Ladder Logic Generated"
    )


# Restoration - Block 5: Main Function and Execution Flow


def reverse_compile_plutus_to_ll(plutus_code):
    """Full pipeline: Parse Plutus -> Convert to Ladder Logic with Nested Logic and Advanced Math."""
    (
        conditions,
        state_changes,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic,
    ) = parse_plutus_script(plutus_code)

    ladder_logic_code = convert_to_ladder_logic(
        conditions,
        state_changes,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic
    )

    (
        conditions,
        state_updates,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic,
    ) = ([], [], [], [], [], [])

    # Flatten output if it's a list
    flattened_output = (
        "".join(ladder_logic_code)
        if isinstance(ladder_logic_code, list)
        else ladder_logic_code
    )
    ladder_logic_code = (
        flattened_output
        + "\n"
        + convert_to_ladder_logic(
            conditions,
            state_updates,
            arithmetic_operations,
            bitwise_operations,
            control_flow,
            nested_logic,
        )
    )
    print("[DEBUG] Ladder Logic Output:", ladder_logic_code)
    return ladder_logic_code


# Main function to read Plutus file and convert to Ladder Logic
if __name__ == "__main__":
    example_plutus = """ 
    traceIfFalse "Condition 1 failed" (X1 && X2)
    traceIfFalse "Condition 2 failed" (Y1 || Y2)
    let state = state + 1
    let result = LN(X) + COS(Y)
    let nested = (A && B) || (C && (D || E))
    if balance >= 100
    JMP LABEL1
    """
    ll_output = reverse_compile_plutus_to_ll(example_plutus)
    print(f"Generated Ladder Logic:\n{ll_output}")
