import unittest
import json
from src.plutusladder_compiler import compile_ir_to_plutus_haskell_enhanced
from src.reverse_compiler.reverse_compiler import reverse_compile_plutus_to_ll
from src.ir_converter import ladder_logic_to_ir, structured_text_to_ir, ir_to_ladder_logic, ir_to_structured_text

class TestMorleyCompilationFlow(unittest.TestCase):
    
    def setUp(self):
        """Load test data before each test."""
        with open("../mappings/ladder_logic.json", "r") as file:
            self.ladder_logic_data = json.load(file)
        with open("../mappings/structured_text.json", "r") as file:
            self.structured_text_data = json.load(file)

    def test_ladder_logic_to_plutus_and_back(self):
        """Test Ladder Logic → IR → Plutus → Reverse Compile → Ladder Logic."""
        ladder_logic_input = {
            "instructions": [
                {"type": "XIC", "args": ["A"]},
                {"type": "OTE", "args": ["B"]}
            ]
        }
        
        ir_data = ladder_logic_to_ir(ladder_logic_input)
        plutus_code = compile_ir_to_plutus_haskell_enhanced(ir_data)
        reversed_ladder_logic = reverse_compile_plutus_to_ll(plutus_code)
        
        self.assertEqual(ladder_logic_input, reversed_ladder_logic, "Ladder Logic forward & reverse compilation failed!")
    
    def test_structured_text_to_plutus_and_back(self):
        """Test Structured Text → IR → Plutus → Reverse Compile → Structured Text."""
        structured_text_input = {
            "instructions": [
                {"type": "IF", "condition": "A > B"},
                {"type": "ASSIGN", "var": "X", "value": "C + D"}
            ]
        }
        
        ir_data = structured_text_to_ir(structured_text_input)
        plutus_code = compile_ir_to_plutus_haskell_enhanced(ir_data)
        reversed_structured_text = reverse_compile_plutus_to_ll(plutus_code)
        
        self.assertEqual(structured_text_input, reversed_structured_text, "Structured Text forward & reverse compilation failed!")
    
    def test_plutus_to_ladder_logic_and_back(self):
        """Test Plutus → IR → Ladder Logic → IR → Plutus."""
        plutus_code = 'traceIfFalse "Condition failed" (A && B)'
        
        ir_data = reverse_compile_plutus_to_ll(plutus_code)
        ladder_logic_data = ir_to_ladder_logic(ir_data)
        compiled_plutus = compile_ir_to_plutus_haskell_enhanced(ladder_logic_to_ir(ladder_logic_data))
        
        self.assertEqual(plutus_code, compiled_plutus, "Plutus to Ladder Logic and back failed!")
    
    def test_plutus_to_structured_text_and_back(self):
        """Test Plutus → IR → Structured Text → IR → Plutus."""
        plutus_code = 'traceIfFalse "Check failed" (X == Y)'
        
        ir_data = reverse_compile_plutus_to_ll(plutus_code)
        structured_text_data = ir_to_structured_text(ir_data)
        compiled_plutus = compile_ir_to_plutus_haskell_enhanced(structured_text_to_ir(structured_text_data))
        
        self.assertEqual(plutus_code, compiled_plutus, "Plutus to Structured Text and back failed!")

if __name__ == "__main__":
    unittest.main()
