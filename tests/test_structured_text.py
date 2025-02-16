import json
import os
import unittest

# Get the correct absolute path for structured_text.json
structured_text_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mappings/structured_text.json"))

# Load the Structured Text mappings
with open(structured_text_path, "r") as file:
    structured_text = json.load(file)

# Reference list of OpenPLC-supported Structured Text instructions
openplc_reference = {
    "logical_operators": ["AND", "OR", "NOT"],
    "comparison_operators": ["=", "<", ">", "<=", ">="],
    "timers": ["TON", "TOF"]
}

class TestStructuredTextMappings(unittest.TestCase):
    
    def test_json_structure(self):
        """Ensure structured_text.json has the correct structure."""
        required_sections = openplc_reference.keys()
        for section in required_sections:
            self.assertIn(section, structured_text, f"Missing section: {section}")

    def test_ir_mappings_exist(self):
        """Ensure each Structured Text instruction has an IR representation."""
        for category, instructions in openplc_reference.items():
            for instruction in instructions:
                self.assertIn(
                    instruction,
                    list(structured_text.get(category, {}).keys()),
                    f"Missing IR mapping for {instruction} in {category}"
                )

    def test_no_duplicate_entries(self):
        """Ensure no duplicate mappings exist."""
        seen = set()
        for category in structured_text:
            for instruction in structured_text[category].values():
                ir_repr = instruction.get("ir_representation")  # Prevent KeyError
                if ir_repr:  # Only check if ir_representation exists
                    self.assertNotIn(ir_repr, seen, f"Duplicate IR mapping: {ir_repr}")
                    seen.add(ir_repr)

if __name__ == "__main__":
    unittest.main()
