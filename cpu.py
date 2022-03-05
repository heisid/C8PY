class CPU:
    def __init__(self):
        '''
        CPU initialization of
        program counter, index register, stack memory,
        timers, and general purpose registers
        '''
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


    def load_font(self, ram):
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
        ram.bulk_write(start_font_addr, FONT)


    def fetch(self, ram):
        '''
        Read the instruction that PC is currently pointing at from memory. 
        An instruction is two bytes.
        '''
        opcode = (ram[self.pc] << 8) | ram[self.pc + 1]
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
            pass # IMPLEMENT LATER

        elif arg = 0x0ee:
            ''' 0x00ee: RET: Return from subroutine '''
            self.pc = self.stack.pop()

        else:
            return False

        return True
