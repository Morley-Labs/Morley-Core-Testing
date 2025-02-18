Generated Ladder Logic:
 XIC X1
XIC X2
OTE Condition_1_failed
XIC Y1
OR Y2
OTE Condition_2_failed
XIC balance >= 100 OTE Check_balance_>=_100
MOV state = state + 1
MOV result = A + B
SHL shift, C, 2
JMP LABEL1
