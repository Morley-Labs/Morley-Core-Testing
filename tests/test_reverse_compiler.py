import unittest
from src.reverse_compiler.reverse_compiler import reverse_compile_plutus_to_ll

class TestReverseCompiler(unittest.TestCase):
    
    def test_basic_conditions(self):
        """
        Test basic Plutus traceIfFalse conditions conversion.
        """
        plutus_script = '''
        traceIfFalse "Condition 1 failed" (X1 && X2)
        traceIfFalse "Condition 2 failed" (Y1 || Y2)
        '''
        
        expected_output = (
            "No Ladder Logic Generated\n"
            "Condition 1 failed: X1 && X2\n"
            "Condition 2 failed: Y1 || Y2"
        )

        self.assertEqual(reverse_compile_plutus_to_ll(plutus_script), expected_output)

    def test_state_updates(self):
        """
        Test state update translation from Plutus to Ladder Logic.
        """
        plutus_script = '''
        let counter = counter + 1
        '''
        
        expected_output = (
            "No Ladder Logic Generated\n"
            "MOV counter = counter + 1"
        )

        self.assertEqual(reverse_compile_plutus_to_ll(plutus_script), expected_output)

    def test_comparison_operators(self):
        """
        Test comparison operators mapping.
        """
        plutus_script = '''
        if balance >= 100
        '''
        
        expected_output = (
            "No Ladder Logic Generated\n"
            "Check balance >= 100: balance >= 100"
        )

        self.assertEqual(reverse_compile_plutus_to_ll(plutus_script), expected_output)

    def test_arithmetic_operations(self):
        """
        Test arithmetic operations conversion.
        """
        plutus_script = '''
        let result = A + B
        '''
        
        expected_output = (
            "No Ladder Logic Generated\n"
            "MOV result = A + B"
        )

        self.assertEqual(reverse_compile_plutus_to_ll(plutus_script), expected_output)

if __name__ == "__main__":
    unittest.main()
