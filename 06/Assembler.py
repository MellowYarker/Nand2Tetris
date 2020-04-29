class Parser:
    def __init__(self, string):
        """ Initial instruction parsing.
            Class properties:
                self.data            (str):         the string instruction.
                self.instructionType (str):         either A (address), C (computation), or L (label).
                self.symbol          (str):         the symbol if the instruction was a label.
                self.dest            (-1 or str):   dest field or -1 if no dest.
                self.comp            (str):         comp field.
                self.jump            (-1 or str):   jump field or -1 if no jump.
                self.address         (str):         address if A-instruction.
        """
        self.data = string
        # remove inline comments from the data
        self.data = self.removeComments()

        # get the instruction type
        if self.data[0] == '@':
            self.instructionType = 'A'
            self.address = self.data[1:]
        elif self.data[0] == '(':
            self.instructionType = 'L'
            self.symbol = self.getSymbol()
        else:
            self.instructionType = 'C'
            self.dest = self.getDest() # dest field
            self.comp = self.getComp() # comp field
            self.jump = self.getJump() # jump field

    def removeComments(self):
        """ Removes any inline comments from the instruction string.
            Returns the string with any comments removed.
        """
        comment = self.data.find("//")
        if comment == -1:
            return self.data
        return self.data[:comment]


    def getSymbol(self):
        """ Returns the symbol within the label (self.data) """
        return self.data[1:-1]


    def getDest(self):
        """ Gets the dest part of the instruction.
            Returns -1 on failure or the dest string on success.
        """
        end = self.data.find('=')
        if end == -1:
            return -1
        return self.data[0:end]


    def getComp(self):
        """ Gets the comp part of the instruction.
            Returns -1 on failure or the comp string on success.
        """
        start = self.data.find('=')
        end = self.data.find(';')
        # if '=' is not found, we will find a ';'
        if start == -1:
            return self.data[:end]
        elif end == -1:
            return self.data[start + 1:]
        else:
            return self.data[start + 1:end]


    def getJump(self):
        """ Gets the jump instructions.
            Returns -1 on failure or the jump string on success.
        """
        start = self.data.find(';')
        if start == -1:
            return -1

        return self.data[start + 1:]

    def updateAddress(self, new):
        """ When resolving variables and labels, we need to translate
            the symbolic reference to the instruction number.
        """
        self.address = new


    def __str__(self):
        if self.instructionType == 'A':
            addr = str(self.address)
            return (f"Instruction: {self.data}\nType: {self.instructionType}\nAddress: {addr}\n")
        elif self.instructionType == 'L':
            return (f"Instruction: {self.data}\nType: {self.instructionType}\nSymbol: {self.symbol}\n")
        dest = str(self.dest)
        comp = str(self.comp)
        jump = str(self.jump)
        return (f"Instruction: {self.data}\nType: {self.instructionType}\nDest: {dest}\nComp: {comp}\nJump: {jump}\n")


class Convert:
    def __init__(self, parsed):
        self.instructionType = parsed.instructionType
        if self.instructionType == 'A':
            # turn the decimal address to a 15 bit binary one.
            binary = format(int(parsed.address), '016b')
            self.instruction = binary[1:]
        else:
            dest = self.convertDest(parsed.dest)
            comp = self.convertComp(parsed.comp)
            jump = self.convertJump(parsed.jump)
            self.instruction = '111'  + comp + dest + jump


    def convertDest(self, destField):
        """ Convert the symbolic dest field to its 3-bit field.
            Returns a 3-bit string on success or -1 on failure.
        """
        # dest is NULL
        if destField == -1:
            return "000"
        elif destField == "M":
            return "001"
        elif destField == "D":
            return "010"
        elif destField == "MD":
            return "011"
        elif destField == "A":
            return "100"
        elif destField == "AM":
            return "101"
        elif destField == "AD":
            return "110"
        elif destField == "AMD":
            return "111"
        # Something went wrong
        return -1


    def convertJump(self, jumpField):
        """ Convert the symbolic jump field to its 3-bit field.
            Returns a 3-bit string on success or -1 on failure.
        """
        # jump is NULL
        if jumpField == -1:
            return "000"
        elif jumpField == "JGT":
            return "001"
        elif jumpField == "JEQ":
            return "010"
        elif jumpField == "JGE":
            return "011"
        elif jumpField == "JLT":
            return "100"
        elif jumpField == "JNE":
            return "101"
        elif jumpField == "JLE":
            return "110"
        elif jumpField == "JMP":
            return "111"
        # Something went wrong
        return -1


    def convertComp(self, compField):
        """ Convert the symbolic comp field to its 7-bit field.
            Returns a 7-bit string acccccc on success or -1 on failure.
        """
        cbits = ""
        if compField == "0":
            cbits = "101010"
        elif compField == "1":
            cbits = "111111"
        elif compField == "-1":
            cbits = "111010"
        elif compField == "D":
            cbits = "001100"
        elif compField == "A" or compField == "M":
            cbits = "110000"
        elif compField == "!D":
            cbits = "001101"
        elif compField == "!A" or compField == "!M":
            cbits = "110001"
        elif compField == "-D":
            cbits = "001111"
        elif compField == "-A" or compField == "-M":
            cbits = "110011"
        elif compField == "D+1":
            cbits = "011111"
        elif compField == "A+1" or compField == "M+1":
            cbits = "110111"
        elif compField == "D-1":
            cbits = "001110"
        elif compField == "A-1" or compField == "M-1":
            cbits = "110010"
        elif compField == "D+A" or compField == "D+M":
            cbits = "000010"
        elif compField == "D-A" or compField == "D-M":
            cbits = "010011"
        elif compField == "A-D" or compField == "M-D":
            cbits = "000111"
        elif compField == "D&A" or compField == "D&M":
            cbits = "000000"
        elif compField == "D|A" or compField == "D|M":
            cbits = "010101"

        # now add the 'a' bit
        if  (   compField == "0" or
                compField == "1" or
                compField == "-1" or
                compField == "D" or
                compField == "A" or
                compField == "!D" or
                compField == "!A" or
                compField == "-D" or
                compField == "-A" or
                compField == "D+1" or
                compField == "A+1" or
                compField == "D-1" or
                compField == "A-1" or
                compField == "D+A" or
                compField == "D-A" or
                compField == "A-D" or
                compField == "D&A" or
                compField == "D|A"    ):
            a = 0
        else:
            a = 1
        a = str(a)
        return a + cbits


if __name__ == "__main__":
    """ 1. Read the input file.
        2. On the first pass, remove all whitespace and comments. Find all labels and parse C-instructions.
        3. On the second pass, resolve all labels and variables by refering to the symbol table.
            We also convert from symbolic instructions to binary.
        4. Write the output to the input filename.hack
    """
    # The default symbol table, we will add to this if we encounter any variables or labels.
    symbolTable = { "R0": 0,
                    "R1": 1,
                    "R2": 2,
                    "R3": 3,
                    "R4": 4,
                    "R5": 5,
                    "R6": 6,
                    "R7": 7,
                    "R8": 8,
                    "R9": 9,
                    "R10": 10,
                    "R11": 11,
                    "R12": 12,
                    "R13": 13,
                    "R14": 14,
                    "R15": 15,
                    "SP": 0,
                    "LCL": 1,
                    "ARG": 2,
                    "THIS": 3,
                    "THAT": 4,
                    "SCREEN": 16384,
                    "KBD": 24576 }

    fname = input("Enter a filename: ")
    f = open(fname, "r")
    instructions = f.readlines()
    f.close()

    # Maintains program line count. Does not include comments or whitespace.
    validLineCounter = 0
    # Stores the index of the next variable. Variables are stored from RAM[16] onwards.
    VariableRAM = 16
    # We will store parsed instructions (Parser Objects) here.
    parsedList = list()

    # This is the first pass through the file. We remove whitespace and comments,
    # find and resolve symbols, and parse instructions.
    for instruction in instructions:
        instruction = instruction.replace(" ", "")
        instruction = instruction.rstrip()
        # skip if it's a comment
        if instruction.startswith("//") or len(instruction) == 0:
            continue

        current = Parser(instruction)
        # If this is a label, search or store it in the symbol table.
        if (current.instructionType == 'L'):
            # Symbol translates to current line number, line disappears in machine code.
            symbolTable[current.symbol] = validLineCounter
            continue

        parsedList.append(current)
        validLineCounter += 1

    out = fname[:-3] + "hack"
    fOut = open(out, "w")
    # This is the second pass. Here we resolve variable references, and convert symbolic
    # instructions to binary.
    for instruction in parsedList:
        # Resolve variable/label references
        if instruction.instructionType == 'A':
            # Work on it if it's symbolic
            if not(instruction.address.isdigit()):
                if not (instruction.address in symbolTable):
                    symbolTable[instruction.address] = VariableRAM
                    VariableRAM += 1
                # Swap the symbolic reference for the value in the symbol table.
                instruction.updateAddress(str(symbolTable[instruction.address]))

        converted = Convert(instruction).instruction
        fOut.write(converted)
        fOut.write('\n')

    fOut.close()

