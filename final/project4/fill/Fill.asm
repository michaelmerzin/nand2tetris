// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INF_LOOP)
@KBD
D = M; // D = KBD

@WHITE_COLOR
D; JEQ // cond-jump

@color
M = -1; //color = black
@COLOR_PICKED
0; JMP

(WHITE_COLOR)
@color
M = 0; // color = white

(COLOR_PICKED)

//start loop
@i
M = 0; // i = 0
@8192
D = A;
@end_loop
M = D; // *end_loop = 8192

(LOOP)
@end_loop
D = M; // D = 8192

@i
D = D - M; // D = 8192 - i

@INF_LOOP
D; JLE // 8192 - i <= 0, finish loop

//body loop
@i
D = M; // D = i
@SCREEN
D = D + A; // address = screen + i
@address
M = D;

@color
D = M; // D = color
@address
A = M;  // A = adress
M = D; // RAM[adress] = color

//end loop
@i
M = M + 1; // i = i + 1
@LOOP
0;JMP 


@INF_LOOP
0;JMP