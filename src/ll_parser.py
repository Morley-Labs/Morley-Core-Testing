"""
LL-Parser: Converts Ladder Logic into full LadderCore IR format.
Ensures support for all OpenPLC components.
"""

import json

def parse_ladder_logic(ladder_code):
    """
    Parses Ladder Logic and converts it into LadderCore IR.
    """
    ir_representation = {
        "type": "LadderCore IR",
        "instructions": [],
        "timers": {},
        "counters": {},
        "math_operations": {},
        "comparators": {},
        "set_reset_latches": {},
        "jump_instructions": {},
        "function_blocks": {},
        "scan_cycle": []
    }

    for line in ladder_code.split("\n"):
        tokens = line.split()

        if not tokens:
            continue

        instruction = tokens[0].upper()
        args = tokens[1:]

        if instruction in ["INPUT", "OUTPUT", "AND", "OR", "NOT", "XOR"]:
            ir_representation["instructions"].append({"type": instruction, "args": args})

        elif instruction in ["TON", "TOF", "TP"] and len(args) > 1:
            ir_representation["timers"][args[0]] = {"type": instruction, "duration": args[1]}

        elif instruction in ["CTU", "CTD"] and len(args) > 1:
            ir_representation["counters"][args[0]] = {"type": instruction, "preset": args[1]}

        elif instruction in ["ADD", "SUB", "MUL", "DIV", "MOD", "MOV"] and len(args) > 1:
            ir_representation["math_operations"][args[0]] = {"operation": instruction, "args": args[1:]}

        elif instruction in [">", "<", "==", "!="] and len(args) > 1:
            ir_representation["comparators"][args[0]] = {"comparison": instruction, "args": args[1:]}

        elif instruction in ["SR", "RS"] and args:
            ir_representation["set_reset_latches"][args[0]] = {"latch_type": instruction}

        elif instruction in ["JMP", "CALL", "RET"] and args:
            ir_representation["jump_instructions"][args[0]] = {"jump_type": instruction}

        elif instruction == "FB" and args:
            ir_representation["function_blocks"][args[0]] = {"args": args[1:]}

        ir_representation["scan_cycle"].append(instruction)

    return json.dumps(ir_representation, indent=2)

if __name__ == "__main__":
    example_ladder = "INPUT X1\nAND X2\nOUTPUT Y1"
    print(parse_ladder_logic(example_ladder))
