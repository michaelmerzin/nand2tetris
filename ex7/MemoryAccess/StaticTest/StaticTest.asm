// push constant 111
@111
D=A;
@SP
A=M;
M=D;
@SP
M=M+1;
// push constant 333
@333
D=A;
@SP
A=M;
M=D;
@SP
M=M+1;
// push constant 888
@888
D=A;
@SP
A=M;
M=D;
@SP
M=M+1;
// pop static 8
@SP
M=M-1;
@SP
A=M;
D=M;
@sp_value
M=D;
@sp_value
D=M;
@Foo.8
M=D;
// pop static 3
@SP
M=M-1;
@SP
A=M;
D=M;
@sp_value
M=D;
@sp_value
D=M;
@Foo.3
M=D;
// pop static 1
@SP
M=M-1;
@SP
A=M;
D=M;
@sp_value
M=D;
@sp_value
D=M;
@Foo.1
M=D;
// push static 3
@Foo.3
D=M;
@address_value
M=D;
@address_value
D=M;
@SP
A=M;
M=D;
@SP
M=M+1;
// push static 1
@Foo.1
D=M;
@address_value
M=D;
@address_value
D=M;
@SP
A=M;
M=D;
@SP
M=M+1;
// sub ///////////////////////
@SP
M=M-1;
@SP
A=M;
D=M;
@y
M=D;
@SP
M=M-1;
@SP
A=M;
D=M;
@x
M=D;
@x
D=M;
@y
D=D-M;
@SP
A=M;
M=D;
@SP
M=M+1;
// push static 8
@Foo.8
D=M;
@address_value
M=D;
@address_value
D=M;
@SP
A=M;
M=D;
@SP
M=M+1;
// add ///////////////////////
@SP
M=M-1;
@SP
A=M;
D=M;
@y
M=D;
@SP
M=M-1;
@SP
A=M;
D=M;
@x
M=D;
@x
D=M;
@y
D=D+M;
@SP
A=M;
M=D;
@SP
M=M+1;