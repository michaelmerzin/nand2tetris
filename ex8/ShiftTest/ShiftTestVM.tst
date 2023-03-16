// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.


load shifttest.vm,
output-file ShiftTest.cmp,
output-list RAM[0]%D2.6.2 RAM[256]%D2.6.2 RAM[257]%D2.6.2 RAM[258]%D2.6.2
 RAM[259]%D2.6.2 RAM[260]%D2.6.2 RAM[261]%D2.6.2 RAM[262]%D2.6.2 RAM[263]%D2.6.2
 RAM[264]%D2.6.2 RAM[265]%D2.6.2 RAM[266]%D2.6.2 RAM[267]%D2.6.2 RAM[268]%D2.6.2
 RAM[269]%D2.6.2 RAM[270]%D2.6.2 RAM[271]%D2.6.2 RAM[272]%D2.6.2;

set RAM[0] 256,  // initializes the stack pointer

repeat 44 {       
  vmstep;
}

output;          // the stack pointer and the stack base
