# Morley-IR

Morley-IR is an **Intermediate Representation (IR) library** designed to standardize and structure **industrial automation languages** (e.g., Ladder Logic, Structured Text) for use in blockchain-based automation. It serves as a **universal translation layer**, ensuring that industrial logic can be accurately represented before being used in blockchain applications.

## Overview
As industries integrate **blockchain-based automation**, there is a need for a **standardized IR** to translate traditional automation logic into structured data formats. Morley-IR provides:

- **Formal IR definitions** for **Ladder Logic (LL)** and **Structured Text (ST)**.
- **Validated mappings** between industrial programming elements and IR components.
- **Unit tests to ensure correctness** of IR structures and mappings.

### **Key Features**
🔹 **Ladder Logic → Morley-IR Conversion** – Fully implemented and validated translation of **rungs, coils, timers, and counters**.  
🔹 **Structured Text → Morley-IR Mapping** – Standardized representation of **logical conditions, loops, and arithmetic**.  
🔹 **IR Schema Validation** – Ensures all IR structures conform to defined specifications, with tests verifying correctness.  
🔹 **Compatible with Morley Compiler** – IR output is designed to be used in **separate compilation processes**.  

## Installation
Clone the repository:
```sh
git clone https://github.com/Morley-Labs/Morley-IR.git
cd Morley-IR
```

Ensure **Python 3.8+** is installed, then install dependencies:
```sh
pip install -r requirements.txt
```

## Project Structure
```
Morley-IR/
│── src/                 # Core IR processing scripts (in progress)
│── mappings/            # Fully implemented Ladder Logic & Structured Text mappings
│── examples/            # Sample IR representations (to be added)
│── tests/               # Unit tests ensuring correctness of mappings and transformations
│── README.md            # Documentation
```

## Usage
# Convert Ladder Logic (.ll) into Morley-IR
```
python src/ll_parser.py input.ll
```
# Compile Morley-IR into Plutus Haskell
```
python src/plutusladder_compiler.py input.ir
```
# Reverse Compile Plutus back into Ladder Logic
```
python src/reverse_compiler/reverse_compiler.py input.plutus
```
### **Validate IR Structure**
```sh
python src/validator_ir_transform.py input.ir
```
# Example Workflow
```
python src/ll_parser.py examples/basic_example.ll > output.ir
```
```
python src/plutusladder_compiler.py output.ir > output.plutus
```
```
python src/reverse_compiler/reverse_compiler.py output.plutus > output_reversed.ll
```
---

## Next Steps
🔹 **Finalizing IR Processing Scripts** – Implement transformation logic inside `src/`.
🔹 **Creating Example Files** – Populate `examples/` with IR outputs for reference.

## Contributing
We welcome contributions! To get started:
1. **Fork the repo**.
2. **Create a new branch**:  
   ```sh
   git checkout -b feature-xyz
   ```
3. **Commit changes**:
   ```sh
   git commit -m "Added XYZ feature"
   ```
4. **Push and open a Pull Request**.

---

## License
This project is licensed under the **Apache 2.0 License**.

## Contact
For questions, discussions, or collaborations:
- **Website**: [MorleyLang.org](https://MorleyLang.org)
- **Twitter/X**: [@MorleyCardano](https://x.com/MorleyCardano)
- **Email**: admin@MorleyLang.org

