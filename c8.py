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

    while True:
        '''
        CPU runs instruction, updates RAM state
        takes keyboard event, and sends command to screen
        '''
        cpu.run()

        ''' Limit to 60 FPS '''
        clock.tick(60)

main()
