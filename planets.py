#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Jan 24 22:53:14 2018
# (c) Alexander Veledzimovich

"""
Sun, Asteroids, Planets for 0_spacewar.py
"""

__version__ = 0.1

from random import random, randrange


import pygame
from pygame.sprite import Sprite

from effects import Dots
from functions import Functions as Func


class Sun(Sprite):
    sun = None

    def __init__(self, set_si, DISPLAY):
        super().__init__()
        self.set_si = set_si
        self.DISPLAY = DISPLAY

        self.x, self.y = self.set_si.SCRWID, self.set_si.SCRHEI
        self.angle = 0
        self.size = self.set_si.SUNRAD * 2

        self.original = pygame.Surface((self.size + self.set_si.SUNRAD,
                                        self.size + self.set_si.SUNRAD))
        self.original = self.original.convert_alpha()
        self.original.fill(self.set_si.EMPTY)
        self.original_rect = self.original.get_rect()
        self.original_rect.center = self.x, self.y

        self.anim_rect = self.original_rect
        self.anim_image = self.original.copy()

        # draw a circle
        self.image = pygame.Surface((self.size, self.size))
        self.image = self.image.convert_alpha()
        self.image.fill(self.set_si.EMPTY)
        pygame.draw.circle(self.image, self.set_si.GAMECLR,
                           (self.set_si.SUNRAD, self.set_si.SUNRAD),
                           self.set_si.SUNRAD, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

        # use masks for collision
        self.mask = pygame.mask.from_surface(self.image)

        Sun.sun = self

    def draw(self):
        # clear old screen for new animation
        self.original.fill(self.set_si.EMPTY)
        for i in range(6):
            self.points = Func.random_polygon(self.set_si.SUNRAD,
                                              ((self.size +
                                                self.size // 2) // 2,
                                               (self.size +
                                                self.size // 2) // 2))
            pygame.draw.polygon(self.original, self.set_si.GAMECLR,
                                self.points, 1)

        self.DISPLAY.blit(self.anim_image, self.anim_rect)
        self.DISPLAY.blit(self.image, self.rect)

    def update(self, game_obj):

        # gravitation
        for i in game_obj:

            dist = Func.count_distance((self.x, self.y), i.rect.center)
            if dist and dist < self.set_si.SUNGRAVRAD:

                gravx = (self.x - i.rect.centerx) / dist
                gravy = (self.y - i.rect.centery) / dist

                actual_grav = ((self.set_si.SUNGRAVRAD -
                                dist) * self.set_si.SUNGRAV)

                i.delx += gravx * actual_grav
                i.dely += gravy * actual_grav

        # rotate sun
        self.angle -= self.set_si.SUNDT

        self.anim_image, self.anim_rect = Func.rotate_image(self.original,
                                                            self.anim_image,
                                                            self.anim_rect,
                                                            self.angle)


class Asteroids(Sprite):

    @staticmethod
    def create(set_si, DISPLAY, game_obj, exclude_obj=False, init=False):
        if init:
            for i in range(set_si.INITASTER):
                init = Func.random_screen_position(set_si.WID,
                                                   set_si.HEI, exclude_obj)
                size = set_si.ASTSIZE[randrange(len(set_si.ASTSIZE))]

                Asteroids(set_si, DISPLAY, game_obj, size, init)
        else:
            if randrange(set_si.ASTMAKE) == 0:
                size = set_si.ASTSIZE[randrange(len(set_si.ASTSIZE))]
                Asteroids(set_si, DISPLAY, game_obj, size, init)

    objects = pygame.sprite.Group()

    def __init__(self, set_si, DISPLAY, game_obj, size, init_coords):
        super().__init__()
        self.set_si = set_si
        self.DISPLAY = DISPLAY

        self.size = size
        self.game_obj = game_obj

        wid = self.size + self.size // 2
        hei = self.size + self.size // 2
        # center
        self.x, self.y = wid // 2, hei // 2

        self.points = Func.random_polygon(size // 2, (self.x, self.y))

        self.original = pygame.Surface((wid, hei))
        self.original = self.original.convert_alpha()

        self.original.fill(self.set_si.EMPTY)
        pygame.draw.polygon(self.original, self.set_si.GAMECLR,
                            self.points, 0)

        self.image = self.original.copy()
        # make a mask for perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

        self.name = 'asteroid'
        self.angle = self.set_si.INITANGLE[self.name]
        self.speed = randrange(*self.set_si.ASTDT)
        self.indestructable = self.set_si.TIMETOBORN
        self.visible = False

        self.rect = self.image.get_rect()
        self.rect.center = self.position(init_coords, size)

        # all forces
        # rotate
        self.delrot = self.speed
        # init speed
        self.delx = random() * self.speed
        self.dely = random() * self.speed

        self.cenx = float(self.rect.centerx)
        self.ceny = float(self.rect.centery)

        self.objects.add(self)
        self.game_obj.append(self)

    def position(self, init_coords, size):
        if init_coords:
            return init_coords
        else:
            half_wid = size // 2
            half_hei = size // 2

            left = (randrange(-self.set_si.WID, -half_wid),
                    randrange(half_hei, self.set_si.HEI - half_hei))
            right = (randrange(self.set_si.WID + half_wid,
                               self.set_si.WID * 2),
                     randrange(half_hei, self.set_si.HEI - half_hei))

            top = (randrange(half_wid, self.set_si.WID - half_wid),
                   randrange(-self.set_si.HEI, -half_hei))
            bottom = (randrange(half_wid, self.set_si.WID - half_wid),
                      randrange(self.set_si.HEI + half_hei,
                                self.set_si.HEI * 2))
            side = [left, right, top, bottom]
            return side[randrange(4)]

    def draw(self):
        self.DISPLAY.blit(self.image, self.rect)

    def update(self):
        if self.indestructable:
            self.indestructable -= 1

        self.cenx += self.delx
        self.ceny += self.dely

        self.rect.center = (self.cenx, self.ceny)

        self.angle += self.delrot

        self.image, self.rect = Func.rotate_image(self.original,
                                                  self.image,
                                                  self.rect,
                                                  self.angle)
        # recalculate mask
        self.mask = pygame.mask.from_surface(self.image)

        # invisible if out of circle screen
        dist = Func.count_distance((self.set_si.SCRWID, self.set_si.SCRHEI),
                                   self.rect.center)

        if dist > self.set_si.SCRRADIUS:
            self.visible = False
        else:
            self.visible = True

        if ((self.cenx < -self.set_si.WID or
                self.cenx > self.set_si.WID * 2) or
            (self.ceny < -self.set_si.HEI or
                self.ceny > self.set_si.HEI * 2)):
            self.game_obj.remove(self)
            self.objects.remove(self)

    def boom(self):
        Dots.create(self.set_si, self.DISPLAY, self.set_si.ASTBOOM,
                    self.rect.center, self.rect.width, self.set_si.GAMECLR)

    def destroy(self):
        if self.size >= 8:
            size = self.size // 2
            for i in range(size // 2):
                Asteroids(self.set_si,
                          self.DISPLAY, self.game_obj, size,
                          self.rect.center)
        else:
            self.boom()
        self.game_obj.remove(self)


if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
