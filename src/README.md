# Morley-IR Source Code

This directory contains the core **source code** for **Morley-IR**, responsible for transforming Ladder Logic (LL) and Structured Text (ST) into **Intermediate Representation (IR)** and compiling IR into **Plutus smart contracts**.

## **Modules Overview**

### **🔹 ll_parser.py**
Parses **Ladder Logic (.ll) files** and converts them into Morley-IR.

### **🔹 plutusladder_compiler.py**
Compiles Morley-IR into **Plutus Core smart contracts**, making Ladder Logic executable on Cardano.

### **🔹 validator_ir_transformer.py**
Validates and optimizes IR transformations before they are compiled.

### **🔹 reverse_compiler/**
A module that enables **reverse compilation**, converting Plutus Core scripts **back into Ladder Logic**, allowing verification and debugging.

