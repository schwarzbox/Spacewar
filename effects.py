#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Fri Feb  2 01:15:49 2018
# (c) Alexander Veledzimovich


"""
Dots and Stars for 0_spacewar.py
"""

__version__ = 0.1

from random import random, randrange

import pygame
from pygame.sprite import Sprite

from functions import Functions as Func


class Dots(Sprite):
    """
    Create particles
    """
    objects = pygame.sprite.Group()

    @staticmethod
    def create(set_si, DISPLAY, value, coords, space, color):
        for i in range(value):
            Dots(set_si, DISPLAY, coords, space, color)

    def __init__(self, set_si, DISPLAY, coords, space,
                 color, minsize=2, maxsize=5):
        super().__init__()

        self.set_si = set_si
        self.DISPLAY = DISPLAY
        self.color = color

        size = randrange(minsize, maxsize)
        self.matrix = [[randrange(2) for i in range(size)]] * size

        self.image = Func.make_image(self.matrix, self.set_si.EMPTY,
                                     self.color, 1)

        self.rect = self.image.get_rect()

        # init pos
        self.rect.center = (randrange(coords[0] - space,
                                      coords[0] + space + 1),
                            randrange(coords[1] - space,
                                      coords[1] + space + 1))
        # move dots
        self.speedx = randrange(*self.set_si.DOTSDT)
        self.speedy = randrange(*self.set_si.DOTSDT)

        self.delx = random() * (self.speedx / 4)
        self.dely = random() * (self.speedy / 4)

        self.cenx = float(self.rect.centerx)
        self.ceny = float(self.rect.centery)

        self.timer = randrange(60, 256)

        self.objects.add(self)

    def update(self):
        self.cenx += self.delx
        self.ceny += self.dely

        self.rect.center = (self.cenx, self.ceny)

        color = (*self.color[:3], self.timer)
        # change transparency
        arr = pygame.PixelArray(self.image)
        arr.replace(self.color, color)
        del arr
        self.color = color

        self.timer -= 1
        if not self.timer:
            self.objects.remove(self)


class Stars(Sprite):
    """
    Stars in the background
    """
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]

    objects = pygame.sprite.Group()

    @staticmethod
    def create(set_si, DISPLAY, exclude_obj=False):
        Stars.objects.empty()

        for i in range(set_si.STARS):
            coords = Func.random_screen_position(set_si.WID,
                                                 set_si.HEI,
                                                 exclude_obj)
            Stars(set_si, DISPLAY, coords)

    def __init__(self, set_si, DISPLAY, coords):
        super().__init__()
        self.DISPLAY = DISPLAY
        self.set_si = set_si
        self.color = self.set_si.STARCLR
        size = randrange(*self.set_si.STARSIZE)
        self.image = Func.make_image(self.matrix, self.set_si.EMPTY,
                                     self.color, size)

        self.rect = self.image.get_rect()

        # init pos
        self.rect.center = coords
        self.objects.add(self)

if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
