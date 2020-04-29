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
    // Quick note on the architecture here:
    //  we only change the pixels if the keyboard state has changed, i.e
    //  if no key has been pressed and the screen is already white, we
    //  shouldn't change anything.

    // This is what the CHECKBLACK & CHECKWHITE labels are for.
    // If we actually want to change the colour, the program enters the
    // BLACKSCREEN or WHITESCREEN blocks.

    // fill = 0: screens white.
    // fill = 1: screens black.
    @fill
    M=0 // by default, the screen is not filled. 
    
    // The 'iter' variable is the number of words (16-bit chunks) 
    // that are required to represent all pixels on the screen.
    @8192   // #rows * #words per row = 256 * 32
    D=A
    @iter
    M=D

    @w // Current 'word', used for the loops.
    M=0

(LOOP)
    // Our infinite loop where we watch the keyboard state.
    // If the key is pressed, check if the screen is already black.
    @KBD
    D=M
    @CHECKBLACK
    D;JNE       // If KBD != 0, a key has been pressed.
    
    @CHECKWHITE // Otherwise, check if the screen is white.
    0;JMP

(CHECKBLACK)
    // Check fill variable.
    @fill
    D=M
    @LOOP
    D;JNE   // If fill is 1, we don't need to change the screen, so go back to LOOP.
    
    // Otherwise, make the whole screen black.
    @fill
    M=1     // Set fill to 1, i.e screen is black.
    @BLACKSCREEN
    0;JMP

(BLACKSCREEN)
    // While w (word) < 8192 (last word), change the pixels in the current batch.
    @w
    D=M
    @iter
    D=D-M
    @CLEANUP    // If word = 8192, we're done, GOTO CLEANUP.
    D;JEQ

    // Otherwise, we need to modify the screen!
    @SCREEN
    D=A
    @w
    A=D+M   // The address that represents the current word 'w' as 16 pixels on the screen.
    M=-1    // Set the current word to -1: 111...111 in binary.

    @w
    M=M+1   // Increment w to the next word.

    @BLACKSCREEN
    0;JMP   // GOTO top of this loop.

(CHECKWHITE)
    // Check fill variable.
    @fill
    D=M
    @LOOP
    D;JEQ   // If fill is 0, go back to the main program LOOP.

    // Otherwise, make the whole screen white.
    @fill
    M=0     // Set fill to 0, i.e screen is white.
    @WHITESCREEN
    0;JMP

(WHITESCREEN)
    // While w (word) < 8192 (last word), change the pixels in the current batch.
    @w
    D=M
    @iter
    D=D-M
    @CLEANUP    // If word = 8192, we're done, GOTO CLEANUP.
    D;JEQ

    // Otherwise, we need to modify the screen.
    @SCREEN     // Base of screen address.
    D=A
    @w
    A=D+M   // The address that represents the current word 'w' as 16 pixels on the screen.
    M=0     // Set the current word to 0: 00...000 in binary.

    @w
    M=M+1   // Increment w to the next word.

    @WHITESCREEN
    0;JMP   // GOTO top of this loop.

(CLEANUP)
    @w      // Reset current word w to 0.
    M=0
    @LOOP   // Return to main program LOOP.
    0;JMP
