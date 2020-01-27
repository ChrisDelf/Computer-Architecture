"""CPU functionality."""

import sys
import re

LDI = 0b10000010
HLT = 1
PRN = 0b01000111
MUL  = 0b10100010


class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0  # program counter, address of the currently executing instruction.
        self.reg = [0] * 8
        self.sp = 7 # stack pointer, value
                    #at the top of the stack (most recently pushed),
                    # or at address F4 if the stack is empty.
        # self.branchtable = {}
        # self.branchtable[HLT] = self.handle_hlt
        # self.branchtable[LDI] = self.handle_ldi
        # self.branchtable[PRN] = self.handle_prn
        # self.branchtable[MUL] = self.handle_mul
        # self.running = True


    def load(self, filename):
        """Load a program into memory."""
        print("Loading")
        address = 0
        program = None
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        with open(filename) as f:
            program = f.readlines()
            # print(program)
        program = [re.sub("#.*$", "", x).strip() for x in program]
        program = [int(x, 2) for x in program if len(x) > 0]

        for instruction in program:

            self.ram[address] = instruction
            address += 1
    # def handle_hlt(self):
    #     self.running = False
    #     # self.pc += 1
    #
    # def handle_ldi(self, a, b):
    #     self.reg[a] = b
    #     # self.pc += 3
    #
    # def handle_prn(self, a):
    #     print(self.reg[a])
    #     # self.pc += 2
    #
    # def handle_mul(self, a, b):
    #     self.reg[a] = self.reg[a] * self.reg[b]
    #     # self.pc += 3
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print("SSFSSDDSDSFDS")
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
## RAM __________________
    def ram_read(self, mar):
       return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr


    def run(self):
        """Run the CPU."""

        cpu_on = True
        while self.running is True:
                command = self.ram[self.pc]
                # print(self.ram)
                if command == LDI: #Set the value of a register to an integer.
                    self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                    self.pc += 3

                elif command == HLT:
                    # print("exiting?")
                    cpu_on = False
                    self.pc += 1


                elif command == PRN: #PRN register pseudo-instruction
                                     #Print numeric value stored in the given register.
                                     #Print to the console the decimal integer value that is stored in the given register.
                    print(self.reg[self.ram[self.pc+1]])
                    self.pc += 1
                elif command == MUL:# This is an instruction handled by the ALU
                                     # Multiply the values in two registers
                                     # together and store the result in registerA.
                    # print("34234fsfsfswerewr")
                    self.reg[self.ram[self.pc+2]]
                    self.alu("MUL", self.ram[self.pc+1], self.ram[self.pc+2])
                    self.pc += 3
                elif command == PUSH:

                    reg = self.ram[self.pc + 1]
                    val = self.reg[reg]
                    self.reg[self.sp] -= 1
                    self.ram[self.reg[self.sp]] = val
                    self.pc += 2
                elif command == POP:
                    reg = self.ram[self.pc + 1]
                    val = self.ram[self.reg[self.sp]]
                    self.reg[reg] = val
                    self.reg[self.sp] += 1
                    self.pc += 2
                elif command == CALL:
                    reg = self.ram[self.pc + 1]
                    self.pc = self.reg[reg]
                else:
                    break


