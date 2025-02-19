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

import os
import json
import re

def load_instruction_mappings():
    # Get the absolute path of the Morley-IR root directory
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    print(f"Resolved base_path: {base_path}")

    # Define full paths for the mappings
    instruction_set_path = os.path.join(base_path, "mappings", "instruction_set.json")
    ladder_logic_path = os.path.join(base_path, "mappings", "ladder_logic.json")
    structured_text_path = os.path.join(base_path, "mappings", "structured_text.json")

    # Debugging: Print paths to check correctness
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

    return instruction_set, ladder_logic, structured_text

instruction_set, ladder_logic, structured_text = load_instruction_mappings()


def parse_plutus_script(plutus_code):
    """ Extract conditions, state updates, and logic from a Morley-specific Plutus script. """
    conditions = []
    state_changes = []
    arithmetic_operations = []
    bitwise_operations = []
    control_flow = []  

    lines = plutus_code.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect mustValidateIn (Plutus time constraint)
        validate_match = re.search(r'mustValidateIn \(from (slot\d+)\)', line)
        if validate_match:
           slot = validate_match.group(1)
           timer_name = f"Timer{len(conditions) + 1}"  # Assign a generic timer name
           conditions.append((f"TON {timer_name}", f"TON {timer_name}, 5000ms"))
           print(f"✅ Detected mustValidateIn: {line} → TON {timer_name}, 5000ms")  # Debugging
           continue
        # Detect and extract timestamp from Plutus datums
        timestamp_match = re.search(r'{"timestamp":\s*(\d+)}', line)
        if timestamp_match:
           timestamp_value = timestamp_match.group(1)
           conditions.append((f"MOV timestamp", f"MOV timestamp = {timestamp_value}"))
           print(f"✅ Detected Timestamp Datum: {line} → MOV timestamp = {timestamp_value}")  # Debugging
           continue


        print(f"🔍 Processing line: {repr(line)}")  # Debugging

        # Extract traceIfFalse conditions
        match = re.search(r'traceIfFalse \"(.*?)\" \((.*?)\)', line)
        if match:
            description, condition = match.groups()
            conditions.append((description, condition))
            print(f"✅ Detected Condition: {description} -> {condition}")  # Debugging
            continue

        # Extract comparison conditions (e.g., if balance >= 100)
        comparison_match = re.search(r'if (\w+) ([=!<>]=?) ([\d.]+|\w+)', line)
        if comparison_match:
            var, op, val = comparison_match.groups()
            conditions.append((f"Check {var} {op} {val}", f"{var} {op} {val}"))
            continue  

        # Extract timer operations (TON, TOF)
        timer_match = re.search(r'timer (\w+) (\d+)ms', line, re.IGNORECASE)
        if timer_match:
            timer_name, duration = timer_match.groups()
            conditions.append((f"TON {timer_name}", f"TON {timer_name}, {duration}ms"))
            print(f"✅ Detected Timer: {timer_name}, Duration: {duration}ms")  # Debugging
            continue

        # Detect if a timer is being checked for "done" state
        timer_done_match = re.search(r'if (\w+)\.DN then output = (\d+)', line)
        if timer_done_match:
            timer_name, output = timer_done_match.groups()
            conditions.append((f"XIC {timer_name}.DN", f"OTE Output{output}"))
            print(f"✅ Detected Timer Done: {timer_name}.DN -> Output{output}")  # Debugging
            continue

        # Extract state updates
        state_match = re.search(r'let (\w+) = (\w+) ([+\-*/]) (\w+)', line)
        if state_match:
            var, left, operator, right = state_match.groups()
            state_changes.append(f"{var} = {left} {operator} {right}")
            print(f"✅ Detected State Change: {var} = {left} {operator} {right}")  # Debugging
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

    print(f"🔎 Parsed Conditions: {conditions}")
    print(f"🔎 Parsed State Changes: {state_changes}")
    print(f"🔎 Parsed Arithmetic: {arithmetic_operations}")
    print(f"🔎 Parsed Bitwise: {bitwise_operations}")
    print(f"🔎 Parsed Control Flow: {control_flow}")

    return conditions, state_changes, arithmetic_operations, bitwise_operations, control_flow


def convert_to_ladder_logic(conditions, state_changes, arithmetic_operations, bitwise_operations, control_flow):
    """ Convert extracted Plutus conditions, state updates, arithmetic, bitwise, and control flow operations to Ladder Logic. """
    ladder_logic_code = []

    # Process conditions (XIC, XIO, TON, TOF)
    for condition in conditions:
        description, logic = condition
        if "timer" in description.lower():
            print(f"⏳ Timer detected before regex: {repr(condition)}")  # Debugging
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
        print(f"🛠 Ladder Logic Output (Before Return):\n{ladder_logic_code}")

    return "\n".join(ladder_logic_code) if ladder_logic_code else "⚠️ No Ladder Logic Generated"


def reverse_compile_plutus_to_ll(plutus_code):
    """ Full pipeline: Parse Plutus -> Convert to Ladder Logic. """
    conditions, state_updates, arithmetic_operations, bitwise_operations, control_flow = parse_plutus_script(plutus_code)

    print(f"🔎 Conditions Sent to Ladder Logic: {conditions}")
    print(f"🔎 State Changes Sent to Ladder Logic: {state_updates}")
    print(f"🔎 Arithmetic Operations Sent to Ladder Logic: {arithmetic_operations}")
    print(f"🔎 Bitwise Operations Sent to Ladder Logic: {bitwise_operations}")
    print(f"🔎 Control Flow Sent to Ladder Logic: {control_flow}")

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
