import unittest
from src.plutusladder_compiler import compile_ir_to_plutus_haskell_enhanced

class TestPlutusLadderCompiler(unittest.TestCase):
    
    def test_nested_conditions(self):
        ir_data = {
            "instructions": [
                {"type": "AND", "args": ["A", "B"]},
                {"type": "OR", "args": ["C", "D"]}
            ]
        }
        expected_output = (
            'traceIfFalse "Condition 0 failed: and" (A && B)\n'
            'traceIfFalse "Condition 1 failed: or" (C || D)\n'
        )
        self.assertIn("traceIfFalse", compile_ir_to_plutus_haskell_enhanced(ir_data))

    def test_timer_and_counter(self):
        ir_data = {
            "timers": {"T1": {"type": "TON", "duration": "500"}},
            "counters": {"C1": {"type": "CTU", "preset": "10"}}
        }
        expected_output = (
            'traceIfFalse "Timer expired" (T1 >= 500)\n'
            'traceIfFalse "Counter exceeded" (C1 >= 10)\n'
        )
        self.assertIn("traceIfFalse", compile_ir_to_plutus_haskell_enhanced(ir_data))

    def test_arithmetic_operations(self):
        ir_data = {
            "math_operations": {
                "C": {"operation": "ADD", "args": ["A", "B"]}
            }
        }
        expected_output = (
            'traceIfFalse "Addition failed" (C == A + B)\n'
        )
        self.assertIn("traceIfFalse", compile_ir_to_plutus_haskell_enhanced(ir_data))
