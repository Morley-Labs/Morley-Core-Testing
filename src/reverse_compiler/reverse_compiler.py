import os
import json
import re
from collections import deque

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


DEBUG_MODE = True
MAX_NESTING_LEVEL = 10


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

def parse_plutus_script(plutus_code):
    """Extract conditions, state updates, nested logic, and advanced math from a Morley-specific Plutus script."""
    conditions = []
    state_changes = []
    arithmetic_operations = []
    bitwise_operations = []
    control_flow = []
    ladder_logic_lines = []
    nested_stack = deque(maxlen=MAX_NESTING_LEVEL)

    lines = plutus_code.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        print(f"[DEBUG] Line Before Tokenization: {line}")
        tokens = tokenize_line(line)
        print(f"[DEBUG] Tokens: {tokens}")
        output = tokens[0]
        op1 = tokens[2] if len(tokens) > 2 else None
        op2 = tokens[4] if len(tokens) > 4 else None

        print(f"[DEBUG] Output: {output}, Operand1: {op1}, Operand2: {op2}")

        condition_match = re.search(r'traceIfFalse "(.+?)" \((.+?)\)', line)
        if condition_match:
            print(f"[DEBUG] Output: {output}, Operand1: {op1}, Operand2: {op2}")
            if "if" in line or "else" in line or "while" in line or "for" in line:
                conditions.append(line)
            message, condition = condition_match.groups()
            ladder_logic_lines.append(f"XIC {condition} OTE {message}")
            return ladder_logic_lines

        if any(func in line for func in operations["advanced_math"]):
            math_match = re.search(
                r"(\w+) = (LN|LOG|SIN|COS|TAN|ASIN|ACOS|ATAN)\((\w+)\)", line
            )
            if math_match:
                output, func, operand = math_match.groups()
                ladder_logic_lines.append(
                    f"{func.upper()} {output} = {func}({operand})"
                )

            elif any(op in line for op in control_flow_mappings.keys()):
                print(f"[DEBUG] Output: {output}, Operand1: {op1}, Operand2: {op2}")
                line = map_operations(line, control_flow_mappings, prefix="LL")
                print(f"[DEBUG] Line Before Tokenization: {line}")

                tokens = tokenize_line(line)
                output = tokens[0] if len(tokens) > 0 else None
                op1 = tokens[2] if len(tokens) > 2 else None
                control_flow.append(line)
                ladder_logic_lines.append(f"{output} = {op1} CONTROL FLOW")

        else:
            ladder_logic_lines.append(f"XIO {op1} OTE {output}")

            ladder_logic_lines.append(
                f"XIC {op1} AND {op2} OTE {output}"
                if "AND" in line
                else (
                    f"XIC {op1} OR {op2} OTE {output}"
                    if "OR" in line
                    else (
                        f"XIC {op1} {op2} OTE {output}"
                        if "XIC" in line
                        else f"XIO {op1} OTE {output}"
                    )
                )
            )


def handle_nested_logic(nested_stack, prefix="LL"):
    """
    Recursively handle nested logic and maintain consistent prefixing.
    """
    ladder_logic_lines = []

    # Collect all nested logic lines
    while nested_stack:
        nested_condition = nested_stack.pop()
        nested_condition = map_operations(
            nested_condition, operations["nested_logic"], prefix=prefix
        )
        ladder_logic_lines.append(f"NESTED LOGIC: {nested_condition}")

        # Recursively handle further nesting
        if "NESTED_" in nested_condition:
            nested_logic_lines = handle_nested_logic(nested_stack, prefix="LL")
            ladder_logic_lines.extend(nested_logic_lines)

        # Return only after all recursion is complete
        return ladder_logic_lines

    if "mustValidateIn" in plutus_code:
        slot_match = re.search(r"mustValidateIn \(from slot(\d+)\)", plutus_code)
    if slot_match:
        slot_value = slot_match.group(1)
    if f"TON TimerX, {slot_value}ms" not in ladder_logic_lines:
        ladder_logic_lines.append(f"TON TimerX, {slot_value}ms")

    if "Verifiable Hash" in plutus_code:
        hash_match = re.search(r"-- Verifiable Hash: (\w+)", plutus_code)
        if hash_match:
            hash_value = hash_match.group(1)
            if f"// Verifiable Hash: {hash_value}" not in ladder_logic_lines:
                ladder_logic_lines.append(f"// Verifiable Hash: {hash_value}")

    if any(nested in line for nested in operations["nested_logic"]):
        nested_stack.append(line)
        ladder_logic_lines.append(f"NESTED LOGIC: {line}")
        control_flow.append(line)
        if DEBUG_MODE:
            print(f"Nested Logic Detected: {line}")

    mapping = None
    for mapping in [
        logical_mappings,
        state_update_mappings,
        arithmetic_mappings,
        bitwise_mappings,
        control_flow_mappings,
        comparison_mappings,
    ]:

        line = map_operations(line, mapping)
        tokens = tokenize_line(line)
        print(f"[DEBUG] Output: {output}, Operand1: {op1}, Operand2: {op2}")

        for op, template in mapping.items():
            if op in line:
                output = tokens[0] if len(tokens) > 0 else None
                op1 = tokens[2] if len(tokens) > 2 else None
                op2 = tokens[4] if len(tokens) > 4 else None
                ladder_logic_lines.append(
                    template.format(output=output, op1=op1, op2=op2)
                )
                return ladder_logic_lines

        for comp_op, ir_rep in comparison_mappings.items():
            if comp_op in line:
                left, right = line.split(comp_op)
                ladder_logic_lines.append(
                    f"XIC {left.strip()} {ir_rep} {right.strip()} OTE {output}"
                )

    nested_list = list(nested_stack)

    if not ladder_logic_lines:
        ladder_logic_lines.append("No Ladder Logic Generated")

    return (
        conditions,
        state_changes,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_list,
    )


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

    for condition in conditions:
        description = condition[0] if len(condition) > 0 else "Undefined"
        logic = condition[1] if len(condition) > 1 else "Undefined"
        if "timer" in description.lower():
            ladder_logic_code.append(f"{description}: {logic}")

    for update in state_changes:
        ladder_logic_code.append(f"MOV {update}")

    for operation in arithmetic_operations:
        ladder_logic_code.append(operation)

    for operation in bitwise_operations:
        ladder_logic_code.append(operation)

    for operation in control_flow:
        ladder_logic_code.append(operation)

    for nested in nested_logic:
        ladder_logic_code.append(f"NESTED LOGIC: {nested}")

    return (
        "\n".join(ladder_logic_code)
        if ladder_logic_code
        else "No Ladder Logic Generated"
    )


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
        nested_logic,
    )

    (
        conditions,
        state_updates,
        arithmetic_operations,
        bitwise_operations,
        control_flow,
        nested_logic,
    ) = ([], [], [], [], [], [])

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
    return ladder_logic_code


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
