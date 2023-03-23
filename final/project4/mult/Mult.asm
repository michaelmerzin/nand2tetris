
// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.


@R1
D = M;
@R3
M = D; //R3 = R1

@R2
M = 0;// R2 = 0

(LOOP)
@R3
D = M // D = R3
@EXIT
D; JLE // R3 == 0, finish loop

@R0
D = M; // D = R0

@R2
M = M + D; // R2 = R2 + R0

@R3
M = M - 1; // R3 = R3 - 1

@LOOP
0;JMP // next step

(EXIT)
@EXIT
0;JMP // end function
