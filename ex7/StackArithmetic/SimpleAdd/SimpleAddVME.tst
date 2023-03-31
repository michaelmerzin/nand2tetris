
load SimpleAdd.vm,
output-file SimpleAdd.out,
compare-to SimpleAdd.cmp,
output-list RAM[0]%D2.6.2 RAM[256]%D2.6.2;

set RAM[0] 256,  // initializes the stack pointer

repeat 3 {       // SimpleAdd.vm has 3 instructions
  vmstep;
}

output;          // the stack pointer and the stack base
