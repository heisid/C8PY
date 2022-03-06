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

main()
