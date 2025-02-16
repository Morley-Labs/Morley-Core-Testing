# Morley-IR

Morley-IR is an **Intermediate Representation (IR) library** designed to standardize and structure **industrial automation languages** (e.g., Ladder Logic, Structured Text) for use in blockchain-based automation. It serves as a **universal translation layer**, ensuring that industrial logic can be accurately represented before being used in blockchain applications.

## Overview
As industries integrate **blockchain-based automation**, there is a need for a **standardized IR** to translate traditional automation logic into structured data formats. Morley-IR provides:

- ✅ **Formal IR definitions** for **Ladder Logic (LL)** and **Structured Text (ST)**.
- ✅ **Mappings between industrial programming elements and IR components**.
- ✅ **Validation and integrity checks** for ensuring correct IR structure.

### **🛠 Key Features**
🔹 **Ladder Logic → Morley-IR Conversion** – Ensures accurate translation of **rungs, coils, timers, and counters**.  
🔹 **Structured Text → Morley-IR Mapping** – Standardized representation of **logical conditions, loops, and arithmetic**.  
🔹 **IR Schema Validation** – Checks that all IR structures conform to defined specifications.  
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
│── src/                 # Core IR structure definitions
│── mappings/            # Ladder Logic & Structured Text to IR mappings
│── examples/            # Example IR representations
│── tests/               # Unit tests for IR validation
│── ll_parser.py         # Parses Ladder Logic into IR
│── validator_ir_transform.py  # Validates IR integrity
│── README.md            # Documentation
```

## Usage
### **Convert Ladder Logic into IR**
```sh
python ll_parser.py input.ll
```

### **Validate IR Structure**
```sh
python validator_ir_transform.py input.ir
```

---

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
