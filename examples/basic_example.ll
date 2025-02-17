(* Basic Ladder Logic Example *)

(* Define Inputs and Outputs *)
VAR
    X1 : BOOL; (* Input Contact *)
    X2 : BOOL; (* Input Contact *)
    Y1 : BOOL; (* Output Coil *)
END_VAR

(* Simple AND Logic *)
LD X1  (* Load X1 *)
AND X2 (* AND with X2 *)
ST Y1  (* Store result in Y1 *)

(* End of Program *)

