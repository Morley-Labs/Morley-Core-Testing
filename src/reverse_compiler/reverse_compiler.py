DEBUG_MODE = True

import os
import json
import re
from collections import deque
from src.reverse_compiler.utils import *
from src.reverse_compiler.reverse_compiler import *


def flatten_and_indent(ladder_logic_lines, level=0):
    """Maintain the hierarchical structure as a nested list."""
    indented_output = []
    indent = "    " * level  # 4 spaces per level

    for line in ladder_logic_lines:
        if isinstance(line, list):
            # Recursively handle nested lists with increased indent
            nested_output = flatten_and_indent(line, level + 1)
            indented_output.extend(nested_output)
        else:
            # Add the line with indentation for the current level
            indented_output.append(f"{indent}{line}")

    return indented_output


operations = {
    "logical_operations": ["AND", "OR", "XOR", "NOT"],
    "comparison_operations": ["EQU", "NEQ", "LES", "LEQ", "GRT", "GEQ"],
    "arithmetic_operations": [
        "ADD",
        "SUB",
        "MUL",
        "DIV",
        "MOD",
        "SQRT",
        "EXP",
        "MOV",
    ],
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
    "selection_functions": ["MUX", "LIMIT", "SEL", "MAX", "MIN"],
    "jump_subroutine": ["JMP", "LBL", "JSR", "RET"],
    "function_blocks": ["SR", "RS", "SFB", "FB", "FC"],
    "coils_outputs": ["OTE", "OTL", "OTU"],
    "advanced_math": [
        "LN",
        "LOG",
        "SIN",
        "COS",
        "TAN",
        "ASIN",
        "ACOS",
        "ATAN",
        "SINH",
        "COSH",
        "TANH",
        "POW",
        "SQRT",
        "EXP",
        "FADD",
        "FSUB",
        "FMUL",
        "FDIV",
        "FNEG",
        "FABS",
    ],
    "nested_logic": [
        "NAND",
        "NOR",
        "XNOR",
        "NESTED_AND",
        "NESTED_OR",
        "NESTED_NOT",
        "NESTED_XOR",
    ],
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python reverse_compiler.py <input_file>")
        print(f"[DEBUG] Arguments Received: {sys.argv}")
        return

    input_file = sys.argv[1]
    print(f"[DEBUG] Input File Path: {input_file}")
    print(f"[DEBUG] Does the file exist? {os.path.exists(input_file)}")

    plutus_code = load_plutus_script(input_file)
    print(f"[DEBUG] Plutus Code:\n{plutus_code}")

    # Determine context from file extension
    context = "LL"  # Default to Ladder Logic
    if input_file.endswith(".st"):
        context = "ST"
    elif input_file.endswith(".ir"):
        context = "IR"

    final_output = reverse_compile_plutus_to_ll(plutus_code, context)
    print("[DEBUG] Final Output from reverse_compile_plutus_to_ll():\n", final_output)
    return final_output  # This ensures the output is passed along


def flatten_mappings(mapping, prefix=None):
    """
    Flattens mappings while preserving prefix hierarchy and checking for both 'symbol' and 'ir_representation'.
    """
    flat_mapping = {}
    for key, value in mapping.items():
        if isinstance(value, dict):
            # Check for 'ir_representation' first, then 'symbol'
            ir_representation = value.get("ir_representation", None)
            symbol = value.get("symbol", None)

            # Preserve the prefix hierarchy
            if ir_representation:
                flat_mapping[key] = (
                    f"{prefix}_{ir_representation}" if prefix else ir_representation
                )
            elif symbol:
                flat_mapping[key] = f"{prefix}_{symbol}" if prefix else symbol
        elif isinstance(value, str):
            flat_mapping[key] = f"{prefix}_{value}" if prefix else value

    return flat_mapping


def load_instruction_mappings():
    """Load instruction mappings for Ladder Logic, Structured Text, and Instruction Set"""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    instruction_set_path = os.path.join(base_path, "mappings", "instruction_set.json")
    ladder_logic_path = os.path.join(base_path, "mappings", "ladder_logic.json")
    structured_text_path = os.path.join(base_path, "mappings", "structured_text.json")

    if DEBUG_MODE:
        print(f"Loading instruction set from: {instruction_set_path}")
        print(f"Loading ladder logic from: {ladder_logic_path}")
        print(f"Loading structured text from: {structured_text_path}")

    with open(instruction_set_path, "r", encoding="utf-8") as f:
        instruction_set = json.load(f)
    with open(ladder_logic_path, "r", encoding="utf-8") as f:
        ladder_logic = json.load(f)
    with open(structured_text_path, "r", encoding="utf-8") as f:
        structured_text = json.load(f)

    return instruction_set, ladder_logic, structured_text


instruction_set, ladder_logic, structured_text = load_instruction_mappings()

if "nested_logic" not in instruction_set:
    raise ValueError("Nested logic mappings are missing in instruction_set.json")

comparison_mappings = flatten_mappings(ladder_logic.get("comparison_operators", {}))

control_flow_mappings = {
    "if": "IF",
    "else": "ELSE",
    "endif": "ENDIF",
    "while": "WHILE",
    "endwhile": "ENDWHILE",
    "for": "FOR",
    "endfor": "ENDFOR",
}

logical_mappings = {"&&": "LL_AND", "||": "LL_OR"}

arithmetic_mappings = flatten_mappings(ladder_logic.get("arithmetic", {}), prefix="LL")

bitwise_mappings = flatten_mappings(
    ladder_logic.get("bitwise_operations", {}), prefix="LL"
)

state_update_mappings = {
    key: value
    for key, value in flatten_mappings(
        ladder_logic.get("state_updates", {}), prefix="LL"
    ).items()
    if key.endswith("_ASSIGN")
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


def map_operations(expression, mappings, prefix="LL"):
    """
    Utility to map operations using predefined mappings while preserving prefix hierarchy.
    """
    for key, value in mappings.items():
        # Check if the mapping value already has a prefix
        if not value.startswith(prefix):
            value = f"{prefix}_{value}"

        # Preserve the prefix while replacing operations
        expression = re.sub(rf"\b{re.escape(key)}\b", value, expression)

    return expression


def tokenize_line(line):
    print(f"[DEBUG] Line Before Tokenization: {line}")
    tokens = re.findall(
        r"[^\s\"']+|\"[^\"]*\"|'[^']*'",
        line,
    )
    print(f"[DEBUG] Tokens After Tokenization: {tokens}")
    return tokens


def handle_nested_logic(
    nested_logic, control_flow, plutus_code, operations, context, prefix="LL"
):
    """
    Recursively handle nested logic and maintain consistent prefixing.
    Dynamically maps to LL, ST, or IR representations.
    """
    ladder_logic_lines = []
    nesting_stack = []

    # Collect all nested logic lines
    while nested_logic:
        nested_condition = nested_logic.popleft()

        # Dynamically select the correct representation
        if context == "LL":
            mappings = ladder_logic.get("nested_logic", {})
        elif context == "ST":
            mappings = structured_text.get("nested_logic", {})
        elif context == "IR":
            mappings = instruction_set.get("nested_logic", {})
        else:
            raise ValueError(f"Unknown context: {context}")

        # Check for IF, ELSE, ENDIF
        if "if" in nested_condition:
            new_block = [mappings["IF"]["ir_representation"]]
            nesting_stack.append(new_block)
            ladder_logic_lines.append(new_block)  # Add as a new block
        elif "else" in nested_condition:
            if nesting_stack:
                current_block = nesting_stack[-1]
                current_block.append(mappings["ELSE"]["ir_representation"])
                new_else_block = []
                current_block.append(new_else_block)
                nesting_stack.append(new_else_block)
        elif "endif" in nested_condition:
            if nesting_stack:
                current_block = nesting_stack.pop()
                current_block.append(mappings["ENDIF"]["ir_representation"])

        print(f"[DEBUG] Ladder Logic Lines: {ladder_logic_lines}")
        print(f"[DEBUG] Nesting Stack: {nesting_stack}")

    # Close any remaining open blocks
    while nesting_stack:
        current_block = nesting_stack.pop()
        current_block.append(mappings["ENDIF"]["ir_representation"])

    return ladder_logic_lines


def parse_plutus_script(plutus_code, context="LL"):
    conditions = []
    state_changes = []
    state_updates = []
    arithmetic_operations = []
    bitwise_operations = []
    control_flow = []
    nested_logic = deque(maxlen=MAX_NESTING_LEVEL)
    ladder_logic_lines = []

    lines = plutus_code.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        print(f"[DEBUG] Processing Line: {line}")
        tokens = tokenize_line(line)
        print(f"[DEBUG] Tokens: {tokens}")

        # Handle Nested Logic
        if "if" in line or "else" in line or "endif" in line:
            nested_logic.append(line)
            ladder_logic_lines.extend(
                handle_nested_logic(
                    nested_logic,
                    control_flow,
                    plutus_code,
                    operations,
                    context,
                    prefix="LL",
                )
            )
            continue

        # Handle regular conditions
        if "traceIfFalse" in line:
            conditions.append(line)

        # Handle State Changes
        if ":=" in line or "state" in line:
            state_changes.append(line)

    print(f"[DEBUG] Final Parsed Components:")
    print(f"Conditions: {conditions}")
    print(f"State Changes: {state_changes}")
    print(f"Control Flow: {control_flow}")
    print(f"Nested Logic: {nested_logic}")
    print(f"Ladder Logic Lines: {ladder_logic_lines}")

    return (
        conditions,
        state_changes,
        state_updates,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic,
        ladder_logic_lines,
    )


def reverse_compile_plutus_to_ll(plutus_code, context="LL"):
    """Full pipeline: Parse Plutus -> Convert to Ladder Logic with Nested Logic and Advanced Math."""

    (
        conditions,
        state_changes,
        state_updates,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic,
        ladder_logic_lines,
    ) = parse_plutus_script(plutus_code, context)

    # Convert to Ladder Logic
    ladder_logic_lines = convert_to_ladder_logic(
        conditions,
        state_changes,
        state_updates,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic,
        ladder_logic_lines,
        context,  # Pass context here
    )

    nested_output = flatten_and_indent(ladder_logic_lines)
    final_output = "\n".join(nested_output)  # << This joins the lines correctly
    print("[DEBUG] Final Ladder Logic Output:\n", final_output)
    return final_output  # << Return the joined output

from collections import deque

MAX_NESTING_LEVEL = 10


def convert_to_ladder_logic(
    conditions,
    state_changes,
    state_updates,
    arithmetic_operations,
    bitwise_operations,
    control_flow,
    nested_logic,
    ladder_logic_lines,
    context,  # Accept context as a parameter
):
    """Convert extracted Plutus components to Ladder Logic."""
    ladder_logic_lines = []

    # Handle Conditions
    for condition in conditions:
        ladder_logic_lines.append(f"XIC {condition}")
        print(f"[DEBUG] Converted Condition: XIC {condition}")

    # Handle State Changes
    for state_change in state_changes:
        ladder_logic_lines.append(f"MOV {state_change}")
        print(f"[DEBUG] Converted State Change: MOV {state_change}")

    # Handle State Updates
    for state_update in state_updates:
        ladder_logic_lines.append(f"UPDATE {state_update}")
        print(f"[DEBUG] Converted State Update: UPDATE {state_update}")

    # Handle Arithmetic Operations
    for arithmetic_operation in arithmetic_operations:
        ladder_logic_lines.append(f"ARITH {arithmetic_operation}")
        print(f"[DEBUG] Converted Arithmetic Operation: ARITH {arithmetic_operation}")

    # Handle Bitwise Operations
    for bitwise_operation in bitwise_operations:
        ladder_logic_lines.append(f"BITWISE {bitwise_operation}")
        print(f"[DEBUG] Converted Bitwise Operation: BITWISE {bitwise_operation}")

    # Handle Control Flow
    for flow in control_flow:
        if flow.startswith("LL_IF"):
            ladder_logic_lines.append(flow)  # Start of an IF block
        elif flow.startswith("LL_ELSE"):
            ladder_logic_lines.append(flow)  # Start of an ELSE block
        elif flow.startswith("LL_ENDIF"):
            ladder_logic_lines.append(flow)  # End of the IF-ELSE block
        else:
            ladder_logic_lines.append(f"FLOW {flow}")
        print(f"[DEBUG] Converted Control Flow: {flow}")

    # Handle Nested Logic
    for nested in nested_logic:
        # Pass the context to the nested logic handler
        ladder_logic_lines.extend(
            handle_nested_logic(nested_logic, control_flow, nested, operations, context)
        )
        print(f"[DEBUG] Converted Nested Logic: NESTED LOGIC: {nested}")

        # Maintain the hierarchical structure and return as a nested list
        nested_output = flatten_and_indent(ladder_logic_lines)
        print("[DEBUG] Final Nested Output:\n", nested_output)

        # Join the output into a single string, preserving the structure
        final_output = nested_output
        print("[DEBUG] Final Ladder Logic Output:\n", final_output)
        return final_output  # Return the fully joined output


if __name__ == "__main__":
    # Run with input file from command line if provided
    if len(sys.argv) > 1:
        final_output = main()
        print(
            "[DEBUG] Final Output from main():\n", final_output
        )  # This ensures the final output is printed
    # Otherwise, run example Plutus test
    else:
        example_plutus = """
        traceIfFalse "Condition 1 failed" (X1 && X2)
        traceIfFalse "Condition 2 failed" (Y1 || Y2)
        let state = state + 1
        let result = LN(X) + COS(Y)
        let nested = (A && B) || (C && (D || E))
        if balance >= 100
        JMP LABEL1
        """
        final_output = reverse_compile_plutus_to_ll(example_plutus)
        print("[DEBUG] Final Output from Example Plutus:\n", final_output)
