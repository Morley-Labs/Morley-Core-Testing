# Morley-IR Mappings

This directory contains **standardized mappings** between **Ladder Logic (LL), Structured Text (ST), and Morley-IR**.  
These mappings ensure **full feature parity with OpenPLC**.

## Mapping Files
- `ladder_logic.json` – Defines mappings for **Ladder Logic (LL)** instructions to Morley-IR.
- `structured_text.json` – Defines mappings for **Structured Text (ST)** operations to Morley-IR.
- `instruction_set.json` – Stores **shared instructions** used by both LL & ST.
- `plutus_ir.json` – Defines mappings from Morley-IR to **Plutus IR (for smart contracts).**  
  🔹 **Why this matters:** This allows industrial control logic to be **executed on the blockchain**, enabling use cases like **secure data logging, smart contract-based automation, and trustless machine interactions.**

## OpenPLC Feature Parity
All mappings now **match OpenPLC’s full instruction set**, including:
✅ **Timers & Counters (TON, TOF, CTU, CTD, TP, RES, RTO) – Including nested & multi-instance scenarios**  
✅ **Bitwise Operations (SHL, SHR, ROR, ROL, AND_BIT, OR_BIT, XOR_BIT, NOT_BIT) – Supporting variable-length shifts**  
✅ **Arithmetic & Logical Operators (ADD, SUB, MUL, DIV, MOD, SQRT, EXP, AND, OR, NOT, XOR) – Handling multi-step calculations**  
✅ **Jump & Subroutines (JMP, LBL, JSR, RET) – Ensuring correct execution flow across multiple subroutines**  
✅ **Selection Functions (MUX, LIMIT) – Handling dynamic value selection and range clamping**  

## **📌 Feature Set**
Below is a **complete list** of instructions that Morley-IR supports.

### **🔹 Logical Operations**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `AND`        | `XIC A XIC B OTE C`   | `C := A AND B;`        | `(A && B)`               |
| `OR`         | `XIC A OR XIC B OTE C` | `C := A OR B;`         | `(A || B)`               |
| `XOR`        | `XIC A XOR XIC B OTE C` | `C := A XOR B;`       | `A ⊕ B`                   |
| `NOT`        | `XIO A OTE B`         | `B := NOT A;`          | `!A`                      |

---

### **🔹 Comparison Operations**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `EQU` (Equal) | `XIC A EQU B OTE C`  | `C := A = B;`          | `A == B`                 |
| `NEQ` (Not Equal) | `XIC A NEQ B OTE C` | `C := A <> B;`       | `A /= B`                 |
| `LES` (Less Than) | `XIC A LES B OTE C` | `C := A < B;`        | `A < B`                   |
| `LEQ` (Less Than or Equal) | `XIC A LEQ B OTE C` | `C := A <= B;` | `A <= B`                 |
| `GRT` (Greater Than) | `XIC A GRT B OTE C` | `C := A > B;` | `A > B`                   |
| `GEQ` (Greater Than or Equal) | `XIC A GEQ B OTE C` | `C := A >= B;` | `A >= B` |

---

### **🔹 Arithmetic Operations**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `ADD` (Addition) | `ADD A B C` | `C := A + B;` | `A + B` |
| `SUB` (Subtraction) | `SUB A B C` | `C := A - B;` | `A - B` |
| `MUL` (Multiplication) | `MUL A B C` | `C := A * B;` | `A * B` |
| `DIV` (Division) | `DIV A B C` | `C := A / B;` | `A / B` |
| `MOD` (Modulo) | `MOD A B C` | `C := A MOD B;` | `A % B` |
| `SQRT` (Square Root) | `SQRT A B` | `B := SQRT(A);` | `sqrt(A)` |
| `EXP` (Exponential) | `EXP A B` | `B := EXP(A);` | `exp(A)` |

---

### **🔹 Bitwise Operations**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `AND_BIT` | `AND_BIT A B C` | `C := A AND B;` | `A & B` |
| `OR_BIT` | `OR_BIT A B C` | `C := A OR B;` | `A | B` |
| `XOR_BIT` | `XOR_BIT A B C` | `C := A XOR B;` | `A ⊕ B` |
| `NOT_BIT` | `NOT_BIT A B` | `B := NOT A;` | `~A` |
| `SHL` (Shift Left) | `SHL A B 2` | `B := A SHL 2;` | `A << 2` |
| `SHR` (Shift Right) | `SHR A B 2` | `B := A SHR 2;` | `A >> 2` |
| `ROR` (Rotate Right) | `ROR A B 1` | `B := A ROR 1;` | `Rotate Right` |
| `ROL` (Rotate Left) | `ROL A B 1` | `B := A ROL 1;` | `Rotate Left` |

---

### **🔹 Timers & Counters**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `TON` (On-Delay Timer) | `TON T1 500ms` | `T1 := TON(500);` | `T1 >= 500` |
| `TOF` (Off-Delay Timer) | `TOF T2 200ms` | `T2 := TOF(200);` | `T2 <= 200` |
| `TP` (Pulse Timer) | `TP T3 100ms` | `T3 := TP(100);` | `T3 == 100` |
| `CTU` (Count Up) | `CTU C1 10` | `C1 := CTU(10);` | `C1 >= 10` |
| `CTD` (Count Down) | `CTD C2 5` | `C2 := CTD(5);` | `C2 <= 5` |
| `CTUD` (Count Up/Down) | `CTUD C3 15` | `C3 := CTUD(15);` | `C3 +/- 15` |

---

### **🔹 Selection Functions**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `MUX` (Multiplexer) | `MUX X Y SEL Z` | `Z := MUX(SEL, X, Y);` | `if SEL then X else Y` |
| `LIMIT` (Clamp Value) | `LIMIT MIN X MAX Y` | `Y := LIMIT(X, MIN, MAX);` | `if X < MIN then MIN else if X > MAX then MAX else X` |

---

### **🔹 Jump & Subroutine Handling**
| **Instruction** | **Ladder Logic (LL)** | **Structured Text (ST)** | **Plutus IR Equivalent** |
|---------------|----------------------|------------------------|--------------------------|
| `JMP` (Jump to Label) | `JMP LBL1` | `GOTO LBL1;` | `Jump LBL1` |
| `LBL` (Label) | `LBL1:` | `LBL1:` | `Label LBL1` |
| `JSR` (Jump to Subroutine) | `JSR SUB1` | `CALL SUB1;` | `Call SUB1` |
| `RET` (Return) | `RET` | `RETURN;` | `Return` |

## Example Usage
### **Converting Ladder Logic to Morley-IR**
To convert a **Normally Open Contact (XIC)** to Morley-IR:
```json
{
  "XIC": { "symbol": "XIC", "ir_representation": "LL_XIC" }
}
```

To convert a **Timer On-Delay (TON)** instruction:
```json
{
  "TON": { "symbol": "TON", "ir_representation": "LL_TON" }
}
```

### **Converting Structured Text to Morley-IR**
To convert a **Structured Text AND operation** to Morley-IR:
```json
{
  "AND": { "symbol": "AND", "ir_representation": "ST_AND" }
}
```

To convert a **Structured Text Timer On-Delay (TON)**:
```json
{
  "TON": { "symbol": "TON", "ir_representation": "ST_TON" }
}
```
### **🔹 Reverse Compiling Plutus IR to Ladder Logic**
When **converting a Plutus Smart Contract Condition** back into **Ladder Logic**, the process works as follows:

#### **Plutus IR Condition (Smart Contract Logic)**
```json
{
  "traceIfFalse": { "description": "Check Balance", "condition": "balance >= 100" }
}

Becomes the Equivalent Ladder Logic (LL) Instruction
XIC balance >= 100 OTE Check_Balance

✅ This means:

If balance >= 100 (a smart contract condition)
It will activate (OTE) the output coil labeled Check_Balance

🔹 Another Example: Reverse Compilation of Arithmetic Logic
Plutus IR Arithmetic Operation
{
  "let": { "result": "A + B" }
}
Becomes Ladder Logic (LL)
MOV result = A + B

✅ This means:

The addition operation A + B is converted back into MOV (Move), which is the standard way Ladder Logic represents arithmetic assignments.