// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

@R14
D = M; 
@arr
M = D; // arr = R14 arr


@arr
D = M; 
@min_address
M = D // min_address = arr
@max_address
M = D // max_index = arr

//start loop
@i
M = 0; // i = 0

@R15
D = M; 
@end_loop
M = D; // end_loop = arr_length

(LOOP)
@end_loop
D = M; // D = arr_length

@i
D = D - M; // D = arr_length - i

@LOOP_FINISHED
D; JLE // arr_length - i <= 0, finish loop


//body loop
@i
D = M;
@arr
D = D + M; 
@cur_address
M = D; // current_address = arr + i


@cur_address
A = M 
D = M; // *cur_address (cur_value)
@max_address
A = M // M = *max_address
D = D - M; 
@MIN
D;JLE // cur_value - max_value > 0 


// cur_value > max_value //
@cur_address
D = M; // cur_address
@max_address
M = D // max_address = cur_address

(MIN)

@cur_address
A = M 
D = M; // *cur_address (cur_value)
@min_address
A = M // M = *min_address
D = D - M; 
@END_LOOP
D;JGE // cur_value - min_value > 0 


// cur_value < min_value //
@cur_address
D = M; 
@min_address
M = D // max_address = cur_address

(END_LOOP)
@i
M = M + 1; // i = i + 1
@LOOP
0;JMP 


(LOOP_FINISHED)
// swap //
@max_address
A = M; 
D = M // D = *max_address
@temp
M = D; // temp = max_value

@min_address
A = M;  
D = M // D = *min_address (min_value)
@max_address
A = M
M = D; //*max_address = min_value

@temp
D = M // D = temp
@min_address
A = M
M = D; //*min_address = temp (max_value)


(EXIT)
@EXIT
0;JMP // end function