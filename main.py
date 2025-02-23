from src.reverse_compiler.reverse_compiler import parse_plutus_script
from src.reverse_compiler.utils import load_plutus_script

# Test files to run
test_files = [
    "./tests/plutus_scripts/test_advanced_math.plutus",
    "./tests/plutus_scripts/test_complex_combination.plutus",
    "./tests/plutus_scripts/test_loops.plutus",
    "./tests/plutus_scripts/test_nested_if_else.plutus",
]

# Run the tests
for test_file in test_files:
    plutus_code = load_plutus_script(test_file)
    parsed_output = parse_plutus_script(plutus_code)
    print(f"\n--- {test_file} ---")
    print(parsed_output)
