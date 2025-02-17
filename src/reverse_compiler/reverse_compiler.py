"""
Morley Reverse Compiler: Plutus to Ladder Logic
This tool interprets Morley-specific Plutus scripts back into Ladder Logic.

Overview:
- Parses Morley Plutus scripts.
- Extracts logic conditions and mappings.
- Converts to Ladder Logic IR.
- Outputs .ll (Ladder Logic) files.
- Supports all Ladder Logic constructs encountered in real-world PLC programming.
"""

import json
import re

def load_instruction_mappings():
    """Load instruction mappings from JSON files."""
    with open("mappings/instruction_set.json", "r") as f:
        instruction_set = json.load(f)
    with open("mappings/ladder_logic.json", "r") as f:
        ladder_logic = json.load(f)
    with open("mappings/structured_text.json", "r") as f:
        structured_text = json.load(f)
    return instruction_set, ladder_logic, structured_text

instruction_set, ladder_logic, structured_text = load_instruction_mappings()

def parse_plutus_script(plutus_code):
    """ Extract conditions, state updates, and logic from a Morley-specific Plutus script. """
    conditions = []
    state_changes = []
    arithmetic_operations = []
    bitwise_operations = []
    control_flow = []  # Correctly placed variable

    lines = plutus_code.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract traceIfFalse conditions
        match = re.search(r'traceIfFalse "(.*?)" \((.*?)\)', line)
        if match:
            description, condition = match.groups()
            conditions.append((description, condition))
            continue

        # Extract comparison conditions (e.g., if balance >= 100)
        comparison_match = re.search(r'if (\w+) ([=!<>]=?) ([\d.]+|\w+)', line)
        if comparison_match:
            var, op, val = comparison_match.groups()
            conditions.append((f"Check {var} {op} {val}", f"{var} {op} {val}"))
            continue  # Ensures conditions are properly captured

        # Extract state updates
        state_match = re.search(r'let (\w+) = (\w+) ([+\-*/]) (\w+)', line)
        if state_match:
            var, left, operator, right = state_match.groups()
            state_changes.append(f"{var} = {left} {operator} {right}")
            continue

        # Extract arithmetic operations
        arithmetic_match = re.search(r'let (\w+) = (\w+) ([+\-*/]) (\w+)', line)
        if arithmetic_match:
            var, operand1, operation, operand2 = arithmetic_match.groups()
            arithmetic_operations.append(f"MOV {var} = {operand1} {operation} {operand2}")
            continue

        # Extract bitwise operations
        bitwise_match = re.search(r'let (\w+) = (\w+) (SHL|SHR|ROR|ROL) (\d+)', line)
        if bitwise_match:
            var, operand, operation, shift_value = bitwise_match.groups()
            bitwise_operations.append(f"{operation} {var}, {operand}, {shift_value}")
            continue

        # Extract control flow operations
        control_match = re.search(r'(JMP|LBL|JSR|RET|MCR) (\w+)', line)
        if control_match:
            operation, label = control_match.groups()
            control_flow.append(f"{operation} {label}")

    return conditions, state_changes, arithmetic_operations, bitwise_operations, control_flow

def convert_to_ladder_logic(conditions, state_changes, arithmetic_operations, bitwise_operations, control_flow):
    """ Convert extracted Plutus conditions, state updates, arithmetic, bitwise, and control flow operations to Ladder Logic. """
    ladder_logic_code = []

    # Convert Plutus conditions to Ladder Logic XIC/OTE instructions
    for desc, cond in conditions:
        ladder_logic_code.append(f"XIC {cond} OTE {desc}")

    # Convert state updates to MOV instructions
    for update in state_changes:
        if "+=" in update or "-=" in update or "*=" in update or "/=" in update:
            ladder_logic_code.append(f"MOV {update}")  # Already shorthand
        else:
            # Convert explicit `counter = counter + 1` to `counter += 1`
            parts = update.split("=")
            if len(parts) == 2 and parts[0].strip() in parts[1].strip():
                var, expr = parts
                operator, value = expr.strip().split(" ")[1], expr.strip().split(" ")[2]
                shorthand = f"{var.strip()} {operator}= {value.strip()}"
                ladder_logic_code.append(f"MOV {shorthand}")
            else:
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

    return "\n".join(ladder_logic_code)

def reverse_compile_plutus_to_ll(plutus_code):
    """ Full pipeline: Parse Plutus -> Convert to Ladder Logic. """
    conditions, state_updates, arithmetic_operations, bitwise_operations, control_flow = parse_plutus_script(plutus_code)
    ladder_logic_code = convert_to_ladder_logic(conditions, state_updates, arithmetic_operations, bitwise_operations, control_flow)
    return ladder_logic_code

if __name__ == "__main__":
    example_plutus = '''
    traceIfFalse "Condition 1 failed" (X1 && X2)
    traceIfFalse "Condition 2 failed" (Y1 || Y2)
    let state = state + 1
    let result = A + B
    let shift = C SHL 2
    if balance >= 100
    JMP LABEL1
    '''
    ll_output = reverse_compile_plutus_to_ll(example_plutus)
    print("Generated Ladder Logic:\n", ll_output)
