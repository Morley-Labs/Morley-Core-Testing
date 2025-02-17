# Morley Reverse Compiler: Plutus to Ladder Logic

This module is responsible for **reverse-compiling Plutus scripts back into Ladder Logic (LL)**, allowing verification and debugging of smart contracts in their original PLC-based format.

## **Functionality**

🔹 **Parses Morley Plutus scripts** – Extracts logic conditions, state updates, arithmetic operations, and control flow.
🔹 **Converts Plutus logic to Ladder Logic IR** – Translates blockchain-based execution conditions into industrial automation logic.
🔹 **Outputs standard Ladder Logic (.ll) files** – Ensures compatibility with traditional PLC systems.
🔹 **Supports all Ladder Logic constructs** – Matches OpenPLC's full instruction set for seamless conversion.

## **Core Components**

### **🔹 reverse_compiler.py**
Handles the main logic for converting **Plutus Core scripts** into **Ladder Logic instructions**.

### **🔹 utils.py**
Provides utility functions for **loading and saving scripts**, ensuring smooth processing of Plutus and Ladder Logic files.

## **Usage**

To convert a Plutus script back into Ladder Logic, use:
```sh
python reverse_compiler.py input.plutus > output.ll
```

## **Next Steps**
Expand test coverage to include **complex nested Plutus conditions**.

