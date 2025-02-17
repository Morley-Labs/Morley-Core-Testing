(* Structured Text Example *)

PROGRAM Main
VAR
    A : BOOL := FALSE;  (* Input Variable *)
    B : BOOL := FALSE;  (* Input Variable *)
    C : BOOL := FALSE;  (* Output Variable *)
    Timer1 : TON;       (* On-Delay Timer *)
END_VAR

(* Logical AND Operation *)
C := A AND B;

(* Timer Operation *)
Timer1(IN := C, PT := T#5S);

(* End of Program *)

