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
