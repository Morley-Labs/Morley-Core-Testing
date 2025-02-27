import sys
import os
import unittest
from src.plutusladder_compiler import (
    ll_to_plutus as compile_ir_to_plutus_haskell_enhanced,
)
from src.validator_ir_transform import ladder_logic_to_ir


class TestLLToPlutus(unittest.TestCase):

    def test_basic_logical_operation(self):
        """Test Ladder Logic → IR → Plutus (Basic Logical Operation)"""
        ladder_logic_input = {
            "instructions": [
                {"type": "XIC", "args": ["A"]},
                {"type": "OTE", "args": ["B"]},
            ]
        }

        ir_data = ladder_logic_to_ir(ladder_logic_input)
        plutus_code = compile_ir_to_plutus_haskell_enhanced(ir_data)

        print("[DEBUG] Generated Plutus Code (Basic):", plutus_code)

    def test_nested_logical_operation(self):
        """Test Ladder Logic → IR → Plutus (Nested Logical Operation)"""
        ladder_logic_input = {
            "instructions": [
                {"type": "XIC", "args": ["A"]},
                {"type": "AND", "args": ["B"]},
                {"type": "OR", "args": ["C"]},
                {"type": "OTE", "args": ["D"]},
            ]
        }

        ir_data = ladder_logic_to_ir(ladder_logic_input)
        plutus_code = compile_ir_to_plutus_haskell_enhanced(ir_data)

        print("[DEBUG] Generated Plutus Code (Nested):", plutus_code)

    def test_arithmetic_operation(self):
        """Test Ladder Logic → IR → Plutus (Arithmetic Operation)"""
        ladder_logic_input = {
            "instructions": [{"type": "ADD", "args": ["A", "B", "C"]}]
        }

        ir_data = ladder_logic_to_ir(ladder_logic_input)
        plutus_code = compile_ir_to_plutus_haskell_enhanced(ir_data)

        print("[DEBUG] Generated Plutus Code (Arithmetic):", plutus_code)


if __name__ == "__main__":
    unittest.main()
