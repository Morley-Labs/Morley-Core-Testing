DEBUG_MODE = True

import os
import json
import re
from collections import deque
from src.reverse_compiler.utils import *
from src.reverse_compiler.reverse_compiler import *
import sys

sys.path.append("./src")


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

    # Iterate over each condition and convert to ladder logic
    for condition in conditions:
        ladder_logic_lines = convert_to_ladder_logic(
            [condition],  # Pass each condition
            state_changes,
            state_updates,
            arithmetic_operations,
            bitwise_operations,
            control_flow,
            nested_logic,
            ladder_logic_lines,
            context,
        )
    print(
        "[DEBUG] ladder_logic_lines before flattening (Final Output):",
        ladder_logic_lines,
    )

    if ladder_logic_lines is None:
        print(
        "[ERROR] ladder_logic_lines is None at Final Output. Check overall mappings and conditions handling."
    )
        return "ERROR: ladder_logic_lines is None"
    else:
        nested_output = flatten_and_indent(ladder_logic_lines)

    final_output = "\n".join(nested_output)  # << This joins the lines correctly
    print("[DEBUG] Final Ladder Logic Output:\n", final_output)
    return final_output  # << Return the joined output

from collections import deque

MAX_NESTING_LEVEL = 10


def convert_to_ladder_logic(
    conditions,  # Add this as the first parameter
    state_changes,
    state_updates,
    arithmetic_operations,
    bitwise_operations,
    control_flow,
    nested_logic,
    ladder_logic_lines,
    context,
):

    """Convert extracted Plutus components to Ladder Logic."""
    ladder_logic_lines = ladder_logic_lines or []  # Ensure it's always a list

    print("[DEBUG] Conditions Passed to convert_to_ladder_logic:", conditions)
    print("[DEBUG] State Changes Passed to convert_to_ladder_logic:", state_changes)
    print(
        "[DEBUG] Arithmetic Operations Passed to convert_to_ladder_logic:",
        arithmetic_operations,
    )
    print("[DEBUG] Control Flow Passed to convert_to_ladder_logic:", control_flow)
    print(
        "[DEBUG] Mappings Available:",
        logical_mappings,
        arithmetic_mappings,
        control_flow_mappings,
    )

    # Handle Conditions
    for condition in conditions:
        # Split condition into tokens
        tokens = condition.split()  # Tokenize the condition properly
        print(f"[DEBUG] Tokens in Condition: {tokens}")

    # Initialize the mapped line
    mapped_line = "XIC "

    # Go through each token and map accordingly
    for token in tokens:
        if token in logical_mappings:
            mapped_value = logical_mappings[token]
            mapped_line += f"{mapped_value} "
        else:
            # Clean up traceIfFalse and add the condition as XIC input
            token = token.replace("traceIfFalse", "").replace('"', "").strip()
            mapped_line += f"{token} " if token not in ["traceIfFalse"] else ""

    # Add OTE at the end to indicate output (based on test expectations)
    if "traceIfFalse" in condition:
        mapped_line += "OTE Condition Failed"
    else:
        mapped_line += "OTE"

    mapped_line = mapped_line.strip()
    ladder_logic_lines.append(mapped_line)
    print(f"[DEBUG] Converted Condition: {mapped_line}")

    # Handle Comparison Operators
    for comparison in control_flow:
        # Split comparison into tokens
        comparison_tokens = comparison.split()
        print(f"[DEBUG] Tokens in Comparison: {comparison_tokens}")

    # Initialize the mapped line
    mapped_line = "XIC "

    # Tokenize the condition
    tokens = []

    # Go through each token and map accordingly
    for token in tokens:
        mapped_line += (
            f"{token} " if token not in ["=", "<", ">", "<=", ">="] else token + " "
        )

    # Add OTE at the end to indicate output (based on test expectations)
    mapped_line += "OTE Check Comparison"

    mapped_line = mapped_line.strip()
    ladder_logic_lines.append(mapped_line)
    print(f"[DEBUG] Mapped Comparison: {mapped_line}")

    # Handle State Updates
    if state_updates:
        print("[DEBUG] Found State Updates:", state_updates)
        for state_update in state_updates:
            print("[DEBUG] Checking State Update:", state_update)

        # Tokenize the state update
        tokens = state_update.split()
        print("[DEBUG] Tokens in State Update:", tokens)

        # Initialize the mapped line
        mapped_line = "MOV "

        # Tokenize the state update
        tokens = state_update.split()

        # Go through each token and map accordingly
        for token in tokens:
            if token != "let":
                mapped_line += f"{token} " if token != "let" else ""

        mapped_line = mapped_line.strip()

        # Check and append to ladder_logic_lines if valid
        if mapped_line:
            ladder_logic_lines.append(mapped_line)
            print(f"[DEBUG] Mapped State Update: {mapped_line}")
        else:
            print("[DEBUG] No State Updates Found.")

    # Handle Arithmetic Operations
    if arithmetic_operations:
        print("[DEBUG] Found Arithmetic Operations:", arithmetic_operations)
    for arithmetic_operation in arithmetic_operations:
        print("[DEBUG] Checking Arithmetic Operation:", arithmetic_operation)

        # Tokenize the operation
        arithmetic_tokens = arithmetic_operation.split()
        print("[DEBUG] Tokens in Arithmetic Operation:", arithmetic_tokens)

        # Initialize the mapped line
        mapped_line = ""
        skip_next = False  # To handle "=" and ignore it

        # Go through each token and map accordingly
        for i, token in enumerate(arithmetic_tokens):

            # Skip the next token if flagged
            if skip_next:
                skip_next = False
                continue

            # If "=" is found, skip it and continue to next token
            if token == "=":
                mapped_line += f"{tokens[i-1]} = "
                skip_next = True
                continue

            # Check if the token is in the arithmetic mappings
            if token in arithmetic_mappings:
                mapped_value = arithmetic_mappings[token]
                mapped_line += f"{mapped_value} "
            else:
                mapped_line += f"{token} " if token not in ["+"] else "ADD "

        # Prefix with ADD if "+" is present
        # Check and map arithmetic operations
        if "+" in tokens:
            mapped_line = "ADD " + " ".join(tokens[1:]).strip()

        # Check if the operation is in the arithmetic mappings
        for op, ll_op in arithmetic_mappings.items():
            if op in tokens:
                mapped_line = f"{ll_op} " + mapped_line.strip()

        # Strip any extra spaces
        mapped_line = mapped_line.strip()

        # Check and append to ladder_logic_lines if valid
        if mapped_line:
            ladder_logic_lines.append(mapped_line)
            print(f"[DEBUG] Mapped Arithmetic Operation: {mapped_line}")
        else:
            print("[DEBUG] No Arithmetic Operations Found.")

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
        nested_lines = handle_nested_logic(
            nested_logic, control_flow, nested, operations, context
        )
        ladder_logic_lines.extend(nested_lines)
        print(f"[DEBUG] Converted Nested Logic: NESTED LOGIC: {nested}")

    print("[DEBUG] Final ladder_logic_lines:", ladder_logic_lines)
    return ladder_logic_lines  # Always return the ladder_logic_lines list


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
