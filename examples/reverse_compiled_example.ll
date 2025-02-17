(* Reverse Compiled Ladder Logic Example *)

(* This Ladder Logic was reverse compiled from a Plutus script *)

VAR
    X1 : BOOL;
    X2 : BOOL;
    Y1 : BOOL;
    Timer1 : TON;
END_VAR

(* Logical AND Operation *)
LD X1  (* Load X1 *)
AND X2 (* AND with X2 *)
ST Y1  (* Store result in Y1 *)

(* Timer Operation *)
TON Timer1 (IN := Y1, PT := T#5S);

(* End of Program *)

