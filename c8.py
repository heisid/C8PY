#!/usr/bin/env python

''' Main file to glue all components together '''

__author__  = "Rosyid Haryadi"
__license__ = "GPLv3"


import pygame
from cpu import CPU
from ram import RAM
from keyboard import Keyboard
from screen import Screen


def main():
    ram = RAM()
    screen = Screen()
    keyboard = Keyboard()

    cpu = CPU(ram=ram, screen=screen, keyboard=keyboard)

    clock = pygame.time.Clock()

    running = True
    while running:
        ''' Take global event '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.KEYDOWN) or (event.type == pygame.KEYUP):
                keyboard.set_event(event)

        '''
        CPU runs instruction, updates RAM state
        check keyboard input, and sends command to screen
        '''
        cpu.run()
        screen.render()

        ''' Limit to 60 FPS '''
        clock.tick(60)


def load_rom(file_name, ram):
    addr = 0x200
    with open(file_name, 'rb') as f:
        byte = f.read(1)
        while byte:
            ram[addr] = byte
            addr += 0x1


if __name__ == '__main__':
    main()
