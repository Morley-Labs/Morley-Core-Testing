import json
import os
import unittest

# Get the correct absolute path for instruction_set.json
instruction_set_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mappings/instruction_set.json"))

# Load the Instruction Set mappings
with open(instruction_set_path, "r") as file:
    instruction_set = json.load(file)

# Reference list of OpenPLC-supported instruction types
openplc_reference = {
    "bitwise_operations": ["AND_BIT", "OR_BIT", "XOR_BIT", "NOT_BIT"],
    "arithmetic": ["ADD", "SUB", "MUL", "DIV", "MOD"],
    "logical_operations": ["AND", "OR", "XOR", "NOT"],
    "comparison_operators": ["EQU", "NEQ", "LES", "GRT", "LEQ", "GEQ"],
    "move_operations": ["MOV", "SWAP", "INT_TO_REAL", "REAL_TO_INT"]
}

class TestInstructionSetMappings(unittest.TestCase):
    
    def test_json_structure(self):
        """Ensure instruction_set.json has the correct structure."""
        required_sections = openplc_reference.keys()
        for section in required_sections:
            self.assertIn(section, instruction_set, f"Missing section: {section}")

    def test_ir_mappings_exist(self):
        """Ensure each instruction has an IR representation."""
        for category, instructions in openplc_reference.items():
            for instruction in instructions:
                self.assertIn(
                    instruction,
                    list(instruction_set.get(category, {}).keys()),
                    f"Missing IR mapping for {instruction} in {category}"
                )

    def test_no_duplicate_entries(self):
        """Ensure no duplicate mappings exist."""
        seen = set()
        for category in instruction_set:
            for instruction in instruction_set[category].values():
                ir_repr = instruction.get("ir_representation")  # Prevent KeyError
                if ir_repr:  # Only check if ir_representation exists
                    self.assertNotIn(ir_repr, seen, f"Duplicate IR mapping: {ir_repr}")
                    seen.add(ir_repr)

if __name__ == "__main__":
    unittest.main()
