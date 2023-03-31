
load StaticTest.asm,
output-file StaticTest.out,
compare-to StaticTest.cmp,
output-list RAM[256]%D1.6.1;

set RAM[0] 256,    // initializes the stack pointer

repeat 200 {       // enough cycles to complete the execution
  ticktock;
}

output;            // the stack base
