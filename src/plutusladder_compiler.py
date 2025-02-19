"""
PlutusLadder Compiler (PLC) - Enhanced
Transforms LadderCore IR into valid Plutus Haskell and Plutus Core (PLC) with structured validation logic.
"""

import json

def compile_ir_to_plutus_haskell_enhanced(ir_data):
    """
    Converts LadderCore IR into a structured Plutus Haskell script with improved validation logic.
    """
    if not isinstance(ir_data, dict) or "instructions" not in ir_data:
        raise ValueError("Invalid IR input: Missing 'instructions' key")

    script_lines = []

    # Handle logical operations
    if "instructions" in ir_data:
        for i, instr in enumerate(ir_data["instructions"]):
            op_type = instr["type"].lower()
            args = " && ".join(instr["args"]) if op_type == "and" else " || ".join(instr["args"])
            script_lines.append(f'traceIfFalse "Condition {i} failed: {op_type}" ({args})')

    # Handle Timers
    if "timers" in ir_data:
        for timer_name, timer_data in ir_data["timers"].items():
            print(f"Compiling Timer: {timer_name}, Duration: {timer_data['duration']}ms → mustValidateIn (from slotX)")

            if timer_data["type"] == "TON":
                # Dynamically use `slotX` from IR if available
                slot_constraint = timer_data.get("slot", "slotX")
                script_lines.append(f'mustValidateIn (from {slot_constraint}) -- Timer {timer_name} enforced')

            elif timer_data["type"] == "TOF":
                script_lines.append(f'traceIfFalse "Timer {timer_name} off delay expired" ({timer_name} <= {timer_data["duration"]})')

    # Handle Counters
    if "counters" in ir_data:
        for counter_name, counter_data in ir_data["counters"].items():
            if counter_data["type"] == "CTU":
                script_lines.append(f'traceIfFalse "Counter {counter_name} exceeded" ({counter_name} >= {counter_data["preset"]})')
            elif counter_data["type"] == "CTD":
                script_lines.append(f'traceIfFalse "Counter {counter_name} decreased below preset" ({counter_name} <= {counter_data["preset"]})')

    # Ensure the script is not empty
    if not script_lines:
        raise ValueError("Invalid IR format: No valid logic generated")

    haskell_script = """{-# INLINABLE validate #-}
validate :: BuiltinData -> BuiltinData -> ScriptContext -> Bool
validate _ _ ctx =
    let txInfo = scriptContextTxInfo ctx
    in """

    grouped_conditions = []

    for i, instruction in enumerate(ir_data.get("instructions", [])):
        if isinstance(instruction, dict):
            inst_type = instruction["type"].lower()
            args = " && ".join(instruction["args"])  # Ensure valid format
            grouped_conditions.append(f'traceIfFalse "Condition {i} failed: {inst_type}" ({args})')

    if grouped_conditions:
        haskell_script += "    " + " &&\n    ".join(grouped_conditions) + """

script :: PlutusScript
script = mkValidatorScript $$(PlutusTx.compile [|| validate ||])
"""
    else:
        haskell_script += "    True  -- Default to always valid if no conditions\n"

    # Combine logic
    return "\n".join(script_lines) + "\n" + haskell_script


if __name__ == "__main__":
    # Example IR data (normally should be passed from ll_parser.py output)
    example_ir = {
        "instructions": [
            {"type": "INPUT", "args": ["X1"]}, 
            {"type": "AND", "args": ["X2"]}, 
            {"type": "OUTPUT", "args": ["Y1"]}
        ],
        "timers": {
            "Timer1": {"type": "TON", "duration": "5000", "slot": "slot123"}
        },
        "counters": {},
        "math_operations": {},
        "comparators": {},
        "set_reset_latches": {},
        "jump_instructions": {},
        "function_blocks": {}
    }

    try:
        haskell_code = compile_ir_to_plutus_haskell_enhanced(example_ir)
        print("\nGenerated Plutus Haskell Script:\n")
        print(haskell_code)
    except ValueError as e:
        print(f"Error: {e}")
