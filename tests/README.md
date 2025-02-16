# Morley-IR Tests

This directory contains unit tests to **validate the correctness of Ladder Logic (LL) and Structured Text (ST) mappings**  
against **Morley-IR and OpenPLC’s feature set**.

## Running Tests
To run all tests, navigate to the **Morley-IR root directory** and execute:
```sh
python -m unittest discover tests
```

To run **specific tests**, use:
```sh
python -m unittest tests/test_ladder_logic.py
python -m unittest tests/test_structured_text.py
python -m unittest tests/test_instruction_set.py
```

## What Do These Tests Cover?
- ✅ **test_ladder_logic.py** – Verifies Ladder Logic mappings to Morley-IR.
- ✅ **test_structured_text.py** – Ensures Structured Text mappings are correctly formatted.
- ✅ **test_instruction_set.py** – Checks consistency across LL & ST instruction sets.

## Adding New Tests
- New tests should be placed in the `tests/` directory.
- Use `unittest` as the testing framework.
- Ensure **all mappings have unique IR representations** to avoid duplicates.

---
🔹 **These tests ensure that Morley-IR remains fully aligned with OpenPLC’s instruction set.**
