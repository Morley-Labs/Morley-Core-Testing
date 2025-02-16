# Morley-IR Mappings

This directory contains **standardized mappings** between **Ladder Logic (LL), Structured Text (ST), and Morley-IR**.  
These mappings ensure **full feature parity with OpenPLC**.

## Mapping Files
- `ladder_logic.json` – Defines mappings for **Ladder Logic** instructions to Morley-IR.
- `structured_text.json` – Defines mappings for **Structured Text** operations to Morley-IR.
- `instruction_set.json` – Stores **shared instructions** that exist in both LL & ST.

## OpenPLC Feature Parity
Each mapping file has been carefully **verified against OpenPLC** to ensure:
✅ **All Ladder Logic instructions match OpenPLC’s supported set**  
✅ **All Structured Text instructions match OpenPLC’s supported set**  
✅ **Each instruction maps correctly to an equivalent Morley-IR representation**

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
