#!/usr/bin/env python

''' Class for emulating CHIP-8 CPU '''

__author__  = "Rosyid Haryadi"
__license__ = "GPLv3"


import random


class CPU:
    def __init__(self, ram=None, screen=None, keyboard=None):
        '''
        CPU initialization of devices instance that will be used
        program counter, index register, stack memory,
        timers, and general purpose registers
        '''

        ''' Connect to RAM '''
        self.ram = ram

        ''' Connect to screen '''
        self.screen = screen

        ''' Connect to keyboard '''
        self.keyboard = keyboard

        '''
        The first CHIP-8 interpreter (on the COSMAC VIP computer)
        was also located in RAM, from address 000 to 1FF.
        It would expect a CHIP-8 program to be loaded into memory after it,
        starting at address 200 (512 in decimal)
        '''
        self.pc = 0x200

        ''' Index register '''
        self.i = 0x0

        ''' Stack '''
        self.stack = list()

        ''' Timers '''
        self.delay_timer = 0
        self.sound_timer = 0

        ''' 16 of 8-bit General purpose registers '''
        self.v = [0x0] * 16

        self.font_loaded = False


    def run(self):
        ''' 
        Run CPU at one tick clock. Loop is managed by main file (c8.py) 
        font_load() only run once at the beginning
        '''
        if not self.font_loaded:
            self.font_load()
            self.font_loaded = True

        opcode = self.fetch()
        self.execute(opcode)


    def load_font(self):
        '''
        The CHIP-8 emulator should have a built-in font
        Each font character should be 4 pixels wide by 5 pixels tall.
        For some reason, it’s become popular to put it at 050–09F
        '''
        FONT = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
        ]

        start_font_addr = 0x050
        self.ram.bulk_write(start_font_addr, FONT)


    def fetch(self):
        '''
        Read the instruction that PC is currently pointing at from memory. 
        An instruction is two bytes.
        '''
        opcode = (self.ram[self.pc] << 8) | self.ram[self.pc + 1]
        self.pc += 2
        return opcode


    def execute(self, opcode):
        '''
        Choosing function to execute opcode based on its class (first two bits)
        '''
        opcode_type = 0xf000 & opcode
        OPCODE_TYPE_MAP = {
                0x0000: self.op_0,
                0x1000: self.op_1,
                0x2000: self.op_2,
                0X3000: self.op_3,
                0x4000: self.op_4,
                0x5000: self.op_5,
                0x6000: self.op_6,
                0x7000: self.op_7,
                0x8000: self.op_8,
                0x9000: self.op_9,
                0xa000: self.op_a,
                0xb000: self.op_b,
                0xc000: self.op_c,
                0xd000: self.op_d,
                0xe000: self.op_e,
                0xf000: self.op_f
                }
        
        '''
        Execute opcode with argument of the last 12 bits of the opcode
        because we don't need the first 4 bits anyway.
        op_x will return false if the code is invalid, true otherwise.
        so, check the validity, and raise exception if it's not.
        '''
        exe_status = OPCODE_TYPE_MAP[opcode_type](0x0fff & opcode)
        
        if not exe_status:
            print(f"Invalid opcode: {opcode} at {self.pc - 2}")
            sys.exit(1)


    def op_0(self, arg):
        if arg == 0x0e0:
            ''' 0x00e0: CLS: Clear screen '''
            self.screen.clear()

        elif arg == 0x0ee:
            ''' 0x00ee: RET: Return from subroutine '''
            self.pc = self.stack.pop()

        else:
            return False

        return True

    
    def op_1(self, arg):
        ''' 0x1nnn: JP nnn: Jump to address 0xnnn '''
        self.pc = arg

        return True


    def op_2(self, arg):
        ''' 0x2nnn: CALL nnn: Call subroutine at 0xnnn '''
        self.stack.append(self.pc)
        self.pc = arg

        return True


    def op_3(self, arg):
        ''' 0x3xnn: SE Vx, nn: Skip if Vx = nn '''
        idx = (0xf00 & arg) >> 8
        val = 0xff & arg

        if self.v[idx] == val:
            self.pc += 2

        return True


    def op_4(self, arg):
        ''' 0x4xnn: SNE Vx, nn: Skip if Vx != nn '''
        idx = (0xf00 & arg) >> 8
        val = 0xff & arg

        if self.v[idx] != val:
            self.pc += 2

        return True


    def op_5(self, arg):
        if (0x00f & arg) != 0:
            return False

        ''' 0x5xy0: SE Vx, Vy: Skip if Vx = Vy '''
        x_idx = (0xf00 & arg) >> 8
        y_idx = (0x0f0 & arg) >> 4

        if self.v[x_idx] == self.v[y_idx]:
            self.pc += 2

        return True


    def op_6(self, arg):
        ''' 0x6xnn: LD Vx, nn: Set register Vx to 0xnnn '''
        idx = (0xf00 & arg) >> 8
        val = 0x0ff & arg

        self.v[idx] = val

        return True

    
    def op_7(self, arg):
        ''' 0x7xnn: ADD Vx, nn: Add 0xnn to register Vx '''
        idx = (0xf00 & arg) >> 8
        val = 0x0ff & arg

        self.v[idx] = (val + self.v[idx]) & 0xff

        return True

 
    def op_8(self, arg):
        op_subclass = 0x00f & arg
        idx = (0xf00 & arg) >> 8
        idy = (0x0f0 & arg) >> 4

        if op_subclass == 0x0:
            ''' 0x8xy0: LD Vx, Vy: Vx is set to the value of Vy '''
            self.v[idx] = self.v[idy]

        elif op_subclass == 0x1:
            ''' 0x8xy1: OR Vx, Vy: Vx is set to bitwise OR of Vx and Vy '''
            self.v[idx] |= v[idy]

        elif op_subclass == 0x2:
            ''' 0x8xy2: AND Vx, Vy: Vx is set to bitwise AND of Vx and Vy '''
            self.v[idx] &= v[idy]

        elif op_subclass == 0x3:
            ''' 0x8xy2: XOR Vx, Vy: Vx is set to bitwise XOR of Vx and Vy '''
            self.v[idx] ^= v[idy]

        elif op_subclass == 0x4:
            '''
            0x8xy2: ADD Vx, Vy: Vx is set to the value of Vx + Vy
            if the result overflows, Vf (carry flag) is set to 1,
            otherwise Vf is set to 0
            '''
            res = self.v[idx] + self.v[idy]
            self.v[0xf] = res > 0xff
            self.v[idx] = 0xff & res # Clipping if overflow happens

        elif op_subclass == 0x5:
            ''' 0x8xy2: SUB Vx, Vy '''
        elif op_subclass == 0x6:
            ''' 0x8xy2: SHR Vx, Vy '''
        elif op_subclass == 0x7:
            ''' 0x8xy2: SUBN Vx, Vy '''
        elif op_subclass == 0xe:
            ''' 0x8xy2: SHL Vx, Vy '''

        else:
            return False

        return True


    def op_9(self, arg):
        if (0x00f & arg) != 0:
            return False

        ''' 0x9xy0: SNE Vx, Vy: Skip if Vx != Vy '''
        x_idx = (0xf00 & arg) >> 8
        y_idx = (0x0f0 & arg) >> 4

        if self.v[x_idx] != self.v[y_idx]:
            self.pc += 2

        return True


    def op_a(self, arg):
        ''' 0xannn: LD I, nnn: Set register I to 0xnnn '''
        self.i = arg

        return True


    def op_d(self, arg):
        ''' 
        0xdxyn: DRW Vx, Vy, n
        Take (x, y) coordinate from Vx, Vy
        and draw n byte sprite data, starting at address stored at I register
        I is not incremented.
        Coordinate will wrap if it's outside the screen,
        but actual n pixel drawing does not (but is clipped)
        Then set register Vf to 0
        if there's a pixel that is already "on", toggle it to "off"
        and set register Vf to 1. Ribet amat kampret.
        '''
        x = self.v[(0xf00 & arg) >> 8]
        y = self.v[(0x0f0 & arg) >> 4]
        n = 0x00f & arg

        x, y = x % 63, y % 31 # Wrapping

        self.v[0xf] = 0
        
        screen_state = self.screen.get_state()

        for row in range(0, n):
            sprite_byte = self.ram[self.i + row]

            for col in range(0, 0x8):
                ''' Extract col-th bit from sprite_byte '''
                sprite_bit = (sprite_byte >> 0x7 - col) & 0x1

                self.v[0xf] = screen_state[row + y][col + x] and sprite_bit

                if sprite_bit:
                    ''' there is clipping here, but I will handle it to screen '''
                    self.screen.toggle_pixel(column + x, row + y)

        return True


if __name__ == '__main__':
    import unittest
    from tests import TestCPU

    cpu_test_runner = unittest.TestLoader().loadTestsFromTestCase(TestCPU)
    unittest.TextTestRunner(verbosity=2).run(cpu_test_runner)
