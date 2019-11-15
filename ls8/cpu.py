"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

        self.branchtable = {}
        self.branch_operations()
        # Initialize stack pointer
        self.stack_pointer = 0xF3
        
        # Flags register
        # 0b00000LGE.
        # L = Less than
        # G = Greater
        # E = Equals
        self.FL = 0b00000000


    def load(self, program):
        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        # print(f"self.ram is loaded with instructions, it currently looks like: {self.ram}")


    #############
    # BRANCH OP #
    #############
    # * `LDI`: load "immediate", store a value in a register, or "set this register to this value".
    def LDI(self, a, b):

        self.reg[a] = b
        self.pc += 3

    # "PRN". `PRN`: a pseudo-instruction that prints the numeric value stored in a register.
    def PRN(self, a, b):
        print(self.reg[a])
        self.pc += 2
    
    ##### ALU OPERATIONS #####
    def ADD(self, op_a, op_b):
        self.alu("ADD", op_a, op_b)
        self.pc += 3
    # Multiply value a with b at location of reg[a]
    def MUL(self, a, b):
        self.alu("MUL", a, b)
        self.pc += 3

    ##### STACK OPERATIONS #####
    def STACK_POP(self, a, b):
        stack_value = self.ram[self.stack_pointer]
        self.reg[a] = stack_value
        # We cannot move past the top of the stack, so once we reach 0xFF, we shouldn't increase the pointer
        if self.stack_pointer != 0xFF:
            self.stack_pointer += 1
        self.pc += 2

    def STACK_PUSH(self, a, b):
        # Move stack pointer down
        self.stack_pointer -= 1
        # get value from register
        val = self.reg[a]
        # Insert value onto stack
        self.ram_write(self.stack_pointer, val)
        self.pc += 2

    def CALL(self, a, b):
        # store return address (self.pc + 2) in stack (return address is the next instruction address)
        self.stack_pointer -= 1
        return_address = self.pc + 2
        self.ram_write(self.stack_pointer, return_address)

        # then move the pc to the subroutine address
        self.pc = self.reg[a]


    def RET(self, a, b):
        # pop return value from the stack and store it in self.pc
        stack_value = self.ram[self.stack_pointer]
        # so next cycle will go from there
        self.pc = stack_value

    # Populate branchtable
    def branch_operations(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN

        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b10100000] = self.ADD

        self.branchtable[0b01000110] = self.STACK_POP
        self.branchtable[0b01000101] = self.STACK_PUSH

        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET



    # Returns the value found at the address in memory
    def ram_read(self, address):
        return self.ram[address]



    def ram_write(self, address, data):
        self.ram[address] = data



    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            
        else:
            raise Exception("Unsupported ALU operation")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()



    def run(self):
        """Run the CPU."""
        # We're extracting the instructions from RAM it seems

        active = True
        # Initialize Instruction Register

        while active:
            # Store address of data
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # print(f"IR: {IR}")
            # print(f"A: {operand_a}")
            # print(f"B: {operand_b}")

            # `HLT`: halt the CPU and exit the emulator.
            if IR == 0b00000001:
                print("Closing run loop")
                active = False
                break

            elif IR not in self.branchtable:
                print(f"Invalid instruction {IR}")
                sys.exit(1)

            else:
                self.branchtable[IR](operand_a, operand_b)

