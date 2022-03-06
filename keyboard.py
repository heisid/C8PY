#!/usr/bin/env python

''' Class representing CHIP-8 hexadecimal keyboard '''

__author__  = "Rosyid Haryadi"
__license__ = "GPLv3"


import pygame

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
                pygame.K_1: 0x1,
                pygame.K_2: 0x2,
                pygame.K_3: 0x3,
                pygame.K_4: 0x4,
                pygame.K_q: 0xc,
                pygame.K_w: 0x5,
                pygame.K_e: 0x6,
                pygame.K_r: 0xd,
                pygame.K_a: 0x7,
                pygame.K_s: 0x8,
                pygame.K_d: 0x9,
                pygame.K_f: 0xe,
                pygame.K_z: 0xa,
                pygame.K_x: 0x0,
                pygame.K_c: 0xc,
                pygame.K_v: 0xf
                }

        ''' Current keyboard status (event_type, key) '''
        self.kb_status = (None, None)


    def set_keymap(self, keymap):
        ''' For custom keymap '''
        pass


    def set_event(self, event):
        self.kb_status(event.type, event.key)

    
    def get_key_value(self):
        ''' Return None when keyboard event has no value in dict '''
        return KEYBOARD_MAP.get(self.kb_status[1])
