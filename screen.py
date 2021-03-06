#!/usr/bin/python

""" Class emulating screen """

__author__ = "Rosyid Haryadi"
__license__ = "GPLv3"

import pygame


class Screen:
    def __init__(self):
        self.screen_state = None
        self.padding = 20
        self.px_scale = 10

        self.surface = pygame.display.set_mode((
            (64 * self.px_scale) + (2 * self.padding),
            (32 * self.px_scale) + (2 * self.padding)
        ))

        self.clear()

    def draw_pixel(self, x, y, px_value):
        rgb = tuple([0x00 if px_value else 0xff for _ in range(3)])
        self.surface.fill(rgb,
                          (self.px_scale * x, self.px_scale * y, self.padding, self.padding)
                          )

        self.screen_state[y][x] = px_value

    def toggle_pixel(self, x, y):
        px_val = self.screen_state[y][x]
        self.draw_pixel(x, y, not px_val)
        self.screen_state[y][x] = not px_val

    def get_state(self):
        return self.screen_state

    def clear(self):
        self.surface.fill((0xff, 0xff, 0xff))
        self.screen_state = [[False] * 64] * 32

    def render(self):
        """ Actual rendering after pixels set. Called in main file c8.py """
        pygame.display.flip()
