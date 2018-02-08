#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Jan 24 22:53:14 2018
# (c) Alexander Veledzimovich

"""
SpaceShip, Torpeda, Needle(ship), Wedge(ship) for 0_spacewar.py
"""

__version__ = 0.1

from math import cos, pi, sin

import pygame
from pygame.sprite import Sprite

from effects import Dots
from functions import Functions as Func


class SpaceShip(Sprite):

    """
    Basic object class
    """

    def __init__(self, set_si, DISPLAY, game_obj, name=''):
        super().__init__()
        self.set_si = set_si
        self.DISPLAY = DISPLAY

        self.original = Func.make_image(list(zip(*self.matrix)),
                                        self.set_si.EMPTY,
                                        self.set_si.GAMECLR)

        self.name = name
        self.angle = self.set_si.INITANGLE[self.name]

        self.speed = self.set_si.SPEED_DT
        self.fuel = self.set_si.FUEL
        self.torpedos = self.set_si.NUMTORPEDOS
        self.hyper = self.set_si.HYPERJUMP

        self.image = self.original.copy()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.set_si.SHIPPOS.get(name, (0, 1))

        self.image, self.rect = Func.rotate_image(self.original,
                                                  self.image,
                                                  self.rect,
                                                  self.angle)
        # make a mask for perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

        self.game_obj = game_obj

        self.delx = 0
        self.dely = 0

        self.del_angle = 0
        self.cenx = float(self.rect.centerx)
        self.ceny = float(self.rect.centery)
        self.power = False
        self.right = False
        self.left = False

    def count_delta(self, MAXSPEED):
        cosx, siny = self.count_sin_cos()

        delx = self.delx + cosx * self.speed
        dely = self.dely + siny * self.speed

        # correct diagonal movement
        temp_speedx = MAXSPEED - (abs(delx * siny))
        temp_speedy = MAXSPEED - (abs(dely * cosx))

        if abs(self.delx + delx) < abs(temp_speedx):
            self.delx = delx
        if abs(self.dely + dely) < abs(temp_speedy):
            self.dely = dely

    def count_sin_cos(self):
        angle_rad = self.angle * pi / 180
        cosx = cos(angle_rad)
        siny = -sin(angle_rad)
        return cosx, siny

    def count_radius(self, radius):
        cosx, siny = self.count_sin_cos()
        len_x = cosx * radius
        len_y = siny * radius
        return len_x, len_y

    def run_engine(self, num_particle=6, space=3):
        # make a inversion on the bottom
        len_x, len_y = self.count_radius((self.rect.width // 2) + 2)
        x, y = self.rect.center
        cen_bot_x = x - len_x
        cen_bot_y = y - len_y
        midbot = (int(cen_bot_x), int(cen_bot_y))
        # particles
        Dots.create(self.set_si, self.DISPLAY,
                    num_particle, midbot, space, self.set_si.PDPCLR)

    def side_engine(self, left_right, num_particle=1, space=1):
        len_x, len_y = self.count_radius((self.rect.width // 2) - 4)
        x, y = self.rect.center

        cen_bot_x = x - len_x
        cen_bot_y = y - len_y

        if left_right == 'right':
            engine = (int(cen_bot_x - len_y), int(cen_bot_y + len_x))
        elif left_right == 'left':
            engine = (int(cen_bot_x + len_y), int(cen_bot_y - len_x))
        # particles
        Dots.create(self.set_si, self.DISPLAY,
                    num_particle, engine, space, self.set_si.PDPCLR)

    def launch_torpeda(self, ship_info):
        if self.torpedos:
            len_x, len_y = self.count_radius((self.rect.width // 2) + 2)
            x, y = self.rect.center
            cen_top_x = x + len_x
            cen_top_y = y + len_y
            midtop = (int(cen_top_x), int(cen_top_y))
            Torpeda(self.set_si, self.DISPLAY, self.game_obj,
                    *midtop, self.angle, self.delx, self.dely, self.name)
            self.torpedos -= 1
            ship_info.make_screen()

    def update(self, ship_info):
        self.cenx += self.delx
        self.ceny += self.dely

        if self.power and self.fuel:
            self.fuel -= 1
            self.count_delta(self.set_si.MAXSPEED)
            self.run_engine()
            ship_info.make_screen()

        # very hard inertion
        self.angle += self.del_angle
        if self.right:
            self.del_angle -= self.set_si.ROTATE_DT
            self.side_engine('right')
        if self.left:
            self.del_angle += self.set_si.ROTATE_DT
            self.side_engine('left')

        self.del_angle = min(max(self.del_angle,
                                 -self.set_si.MAXROTSPEED),
                             self.set_si.MAXROTSPEED)

        self.image, self.rect = Func.rotate_image(self.original,
                                                  self.image,
                                                  self.rect,
                                                  self.angle)
        # recalculate mask for collision
        self.mask = pygame.mask.from_surface(self.image)

        # calculate distance for circle screen
        dist = Func.count_distance((self.set_si.SCRWID, self.set_si.SCRHEI),
                                   self.rect.center)

        if dist > self.set_si.SCRRADIUS:
            dist_delx = -((self.cenx - self.set_si.SCRWID) / dist *
                          (self.set_si.SCRRADIUS - 3) * 2)
            dist_dely = -((self.ceny - self.set_si.SCRHEI) / dist *
                          (self.set_si.SCRRADIUS - 3) * 2)
            self.cenx += dist_delx
            self.ceny += dist_dely

        self.rect.center = (self.cenx, self.ceny)

    def boom(self):
        Dots.create(self.set_si, self.DISPLAY, self.set_si.SHIPBOOM,
                    self.rect.center, self.rect.width, self.set_si.WHITE)

    def destroy(self):
        self.boom()
        self.game_obj.remove(self)

    def hyper_jump(self, ship_info):
        if self.hyper:
            self.hyper -= 1
            x, y = Func.random_screen_position(self.set_si.WID,
                                               self.set_si.HEI)
            dist = Func.count_distance((self.set_si.SCRWID,
                                        self.set_si.SCRHEI), (x, y))

            if dist > self.set_si.SCRRADIUS:
                self.destroy()
                self.ship.remove(self)
            else:
                self.cenx = x
                self.ceny = y
            ship_info.make_screen()


class Torpeda(SpaceShip):

    objects = pygame.sprite.Group()
    matrix = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, set_si, DISPLAY, game_obj, x, y, angle,
                 delx, dely, owner):
        Sprite.__init__(self)
        self.set_si = set_si
        self.DISPLAY = DISPLAY

        self.angle = angle
        self.original = Func.make_image(list(zip(*self.matrix)),
                                        self.set_si.EMPTY,
                                        self.set_si.GAMECLR)
        self.image = self.original.copy()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.image, self.rect = Func.rotate_image(self.original,
                                                  self.image,
                                                  self.rect,
                                                  self.angle)
        # for perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        self.game_obj = game_obj
        # for safe shoot
        self.owner = owner
        self.speed = self.set_si.TORPEDASPEED
        self.delx = delx
        self.dely = dely
        self.count_delta(self.set_si.TORPEDAMAXSPEED)

        self.cenx = float(self.rect.centerx)
        self.ceny = float(self.rect.centery)

        self.boom_dist = self.set_si.TORPEDADIST

        self.objects.add(self)
        self.game_obj.append(self)

    def update(self):
        self.cenx += self.delx
        self.ceny += self.dely
        self.rect.center = (self.cenx, self.ceny)

        self.count_delta(self.set_si.TORPEDAMAXSPEED)
        self.run_engine(num_particle=4, space=4)

        self.boom_dist -= 1
        if self.boom_dist < 0:
            self.destroy()
            self.objects.remove(self)
            return

        dist = Func.count_distance((self.set_si.SCRWID, self.set_si.SCRHEI),
                                   self.rect.center)

        if dist > self.set_si.SCRRADIUS:
            self.game_obj.remove(self)
            self.objects.remove(self)


class Needle(SpaceShip):
    ship = pygame.sprite.GroupSingle()
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    ]

    def __init__(self, set_si, DISPLAY, game_obj, name):
        super().__init__(set_si, DISPLAY, game_obj, name)
        self.ship.add(self)
        self.game_obj.append(self)


class Wedge(SpaceShip):
    ship = pygame.sprite.GroupSingle()
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1,
            1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1,
            1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    ]

    def __init__(self, set_si, DISPLAY, game_obj, name):
        super().__init__(set_si, DISPLAY, game_obj, name)
        self.ship.add(self)
        self.game_obj.append(self)

if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
