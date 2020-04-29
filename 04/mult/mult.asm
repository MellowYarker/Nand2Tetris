// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
    // Set variables
    @i   // i = 0
    M=0
    @sum // sum = 0
    M=0
    
    //  We want to loop over the smaller number, since the addition operation 
    //  is less compuationally less expensive than a full loop.
    
    // If R0 >= R1, go to BIGGER.
    @R0
    D=M
    @R1
    D=D-M
    @BIGGER
    D;JGE

    // Otherwise go to SMALLER.
    @SMALLER
    0;JMP

 (LOOP)
    // If i < n
    @i
    D=M
    @n
    D = D-M
    @END
    D;JEQ

    @var
    D=M
    @sum
    M=M+D // sum = sum + var
    
    @i
    M=M+1 // Increment i.

    // Go back to start of loop iteration.
    @LOOP
    0;JMP

(BIGGER)
    // R0 was bigger than R1, so we loop R1 times.
    @R1
    D=M
    @n   // Our loop limit.
    M=D  // Here we set n = RAM[1].

    // We will add R0 to the sum on each loop iteration.
    @R0
    D=M
    @var
    M=D  // var = RAM[0], we will add var to itself n times.

    // Go to the loop to start adding.
    @LOOP
    0;JMP
   

(SMALLER)
    // RAM[0] < RAM[1], so we will add by R1, R0 times.
    // This is conceptually the same as BIGGER.
    @R0
    D=M
    @n
    M=D

    @R1
    D=M
    @var
    M=D

    @LOOP
    0;JMP


(END)
    @sum
    D=M // Store sum in data register.
    @R2
    M=D // set RAM[2] = sum
    
    @END
    0;JMP
