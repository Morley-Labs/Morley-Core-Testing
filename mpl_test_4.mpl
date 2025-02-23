VAR
    inputA: INT = 50;
    inputB: INT = 20;
    result: INT;
    isValid: BOOL;
END_VAR

-- Arithmetic Operation
result := inputA + inputB;

-- Conditional Logic and State Update
IF result > 100 THEN
    isValid := TRUE;
    result := result - 50;
ELSE
    isValid := FALSE;
    result := result + 30;
ENDIF;

-- Blockchain Validation
traceIfFalse("Result is not valid", isValid);