import json
import unittest

# Load the Ladder Logic mappings
import os

# Use the absolute path for the mappings file
ladder_logic_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mappings/ladder_logic.json"))

with open(ladder_logic_path, "r") as file:
    ladder_logic = json.load(file)


# Reference list of OpenPLC-supported instructions
openplc_reference = {
    "contacts": ["XIC", "XIO"],
    "coils": ["OTE", "OTL", "OTU"],
    "timers": ["TON", "TOF", "RTO"],
    "counters": ["CTU", "CTD", "RES"],
    "arithmetic": ["ADD", "SUB", "MUL", "DIV", "MOD"],
    "logical_operations": ["AND", "OR", "XOR", "NOT"],
    "comparison_operators": ["EQU", "NEQ", "LES", "GRT", "LEQ", "GEQ"],
    "bitwise_operations": ["AND_BIT", "OR_BIT", "XOR_BIT", "NOT_BIT"],
    "move_operations": ["MOV", "SWAP", "INT_TO_REAL", "REAL_TO_INT"],
    "jump_subroutine": ["JMP", "LBL", "JSR", "RET"],
    "floating_point_math": ["SIN", "COS", "TAN", "LOG", "EXP", "SQRT"]
}

class TestLadderLogicMappings(unittest.TestCase):
    
    def test_json_structure(self):
        """Ensure ladder_logic.json has the correct structure."""
        required_sections = openplc_reference.keys()
        for section in required_sections:
            self.assertIn(section, ladder_logic, f"Missing section: {section}")

    def test_ir_mappings_exist(self):
        """Ensure each Ladder Logic instruction has an IR representation."""
        for category, instructions in openplc_reference.items():
            for instruction in instructions:
                self.assertIn(
                    instruction,
                    [entry["symbol"] for entry in ladder_logic.get(category, {}).values()],
                    f"Missing IR mapping for {instruction} in {category}"
                )

    def test_no_duplicate_entries(self):
        """Ensure no duplicate mappings exist."""
        seen = set()
        for category in ladder_logic:
            for instruction in ladder_logic[category].values():
                ir_repr = instruction["ir_representation"]
                self.assertNotIn(ir_repr, seen, f"Duplicate IR mapping: {ir_repr}")
                seen.add(ir_repr)

if __name__ == "__main__":
    unittest.main()
