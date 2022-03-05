class Keyboard:
    def __init__(self):
        '''
        Mapping pygame keycode into CHIP-8 keyboard layout
        CHIP-8 keyboard:
        1 2 3 C
        4 5 6 D
        7 8 9 E
        A 0 B F
        into this:
        1 2 3 4 <- num row above not numpad
        q w e r
        a s d f
        z x c v
        '''
        self.KEYBOARD_MAP = {
                'K_1': 0x1,
                'K_2': 0x2,
                'K_3': 0x3,
                'K_4': 0x4,
                'K_q': 0xc,
                'K_w': 0x5,
                'K_e': 0x6,
                'K_r': 0xd,
                'K_a': 0x7,
                'K_s': 0x8,
                'K_d': 0x9,
                'K_f': 0xe,
                'K_z': 0xa,
                'K_x': 0x0,
                'K_c': 0xc,
                'K_v': 0xf
                }

    def set_keymap(self, keymap):
        '''
        For custom keymap
        '''
        pass
