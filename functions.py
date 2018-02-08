#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sun Jan 28 12:42:38 2018
# (c) Alexander Veledzimovich


"""
Collision and additional function for 0_spacewar.py
"""

__version__ = 0.1

from math import cos, sin
from random import randrange

import pygame


class Functions():
    """
    Container for functions
    """

    def random_screen_position(WID, HEI, exclude_obj=False):
        if exclude_obj:
            # except given object
            obj_x, obj_y = exclude_obj.rect.center
            save_dist = max(exclude_obj.rect.size)
            x_min = randrange(save_dist)
            y_min = save_dist - x_min

            x_dist = randrange(x_min, WID - x_min)
            y_dist = randrange(y_min, HEI - y_min)

            x = (obj_x + x_dist) % WID
            y = (obj_y + y_dist) % HEI
        else:
            x = randrange(WID)
            y = randrange(HEI)
        return x, y

    def find_all_dots(rad):
        pixels = set()
        for grad in range(0, 360):
            for i in range(rad):
                x = int(i * cos(grad))
                y = int(i * sin(grad))

                pixels.add((x, y))
        return pixels

    def make_image(matrix, empty, color, size=1):
        size_matr_x = len(matrix)
        size_matr_y = len(matrix[0])

        icon = pygame.Surface((size_matr_x, size_matr_y))
        icon = icon.convert_alpha()
        icon.fill(empty)
        for i in range(size_matr_x):
            for j in range(size_matr_y):
                if matrix[i][j]:
                    icon.set_at((i, j), color)
        icon = pygame.transform.scale(icon,
                                      (int(size_matr_x // size),
                                       int(size_matr_y // size)))
        return icon

    def random_polygon(rad, center):
        half_rad = rad // 2
        x, y = center
        points = [(randrange(x, x + half_rad),
                   randrange(y - rad - half_rad, y - rad)),
                  (randrange(x + rad, x + rad + half_rad),
                   randrange(y - rad, y - half_rad)),
                  (randrange(x + rad, x + rad + half_rad),
                   randrange(y + half_rad, y + rad)),
                  (randrange(x, x + half_rad),
                   randrange(y + rad, y + rad + half_rad)),
                  (randrange(x - rad, x - half_rad),
                   randrange(y + rad, y + rad + half_rad)),
                  (randrange(x - rad - half_rad, x - rad),
                   randrange(y, y + half_rad)),
                  (randrange(x - rad - half_rad, x - rad),
                   randrange(y - half_rad, y)),
                  (randrange(x - rad, x - half_rad),
                   randrange(y - rad - half_rad, y - rad))]
        return points

    def count_distance(coords_obj1, coords_obj2):
        x1, y1 = coords_obj1
        x2, y2 = coords_obj2
        dist = ((x1 - x2)**2 + (y1 - y2)**2)**(1 / 2)
        return dist

    def rotate_image(original, image, rect, angle):
        old_center = rect.center
        rotate_img = pygame.transform.rotozoom(original, angle, 1)

        image = rotate_img
        rect = image.get_rect()
        rect.center = old_center
        return image, rect

    def collision_insamegroup(coll_ast_ast, Asteroids):
        kill = set()
        for aster in coll_ast_ast:
            for ast in coll_ast_ast[aster]:
                if ast != aster:
                    kill.add(ast)
        for i in kill:
            if not i.indestructable and i.visible:
                Asteroids.objects.remove(i)
                i.destroy()

    def inertion_after_collision(obj1, obj2):
        modx1 = -obj1.delx // 2
        modx2 = -obj2.delx // 2

        mody1 = -obj1.dely // 2
        mody2 = -obj2.dely // 2

        if obj1.delx == 0:
            modx1 = obj2.delx // 1.3
        if obj2.delx == 0:
            modx2 = obj1.delx // 1.3

        if obj1.dely == 0:
            mody1 = obj2.dely // 1.3
        if obj2.dely == 0:
            mody2 = obj1.dely // 1.3

        obj1.delx = modx1
        obj1.dely = mody1
        obj2.delx = modx2
        obj2.dely = mody2

    def collision(Sun, Asteroids, Needle, Wedge, Torpeda):

        for i in (Asteroids.objects, Needle.ship,
                  Wedge.ship, Torpeda.objects):
            sun_coll = pygame.sprite.spritecollide(Sun.sun, i, True,
                                                   pygame.sprite.collide_mask)
            [j.destroy() for j in sun_coll]

        for i in (Needle.ship, Wedge.ship):
            ship_coll = pygame.sprite.groupcollide(i, Asteroids.objects,
                                                   False, True,
                                                   pygame.sprite.collide_mask)

            for ship in ship_coll:
                for i in ship_coll[ship]:
                    Functions.inertion_after_collision(ship, i)
                    i.destroy()

        coll_ast_ast = pygame.sprite.groupcollide(Asteroids.objects,
                                                  Asteroids.objects,
                                                  False, False,
                                                  pygame.sprite.collide_mask)

        Functions.collision_insamegroup(coll_ast_ast, Asteroids)

        # asteroids and torpedos
        for i in (Needle.ship, Wedge.ship, Asteroids.objects):
            coll_torp = pygame.sprite.groupcollide(Torpeda.objects,
                                                   i,
                                                   False, False,
                                                   pygame.sprite.collide_mask)

            for torp in coll_torp:
                for obj in coll_torp[torp]:
                    if obj.name != torp.owner:
                        Torpeda.objects.remove(torp)
                        i.remove(obj)
                        torp.destroy()
                        obj.destroy()
                        break

        # ship and ship
        ships_col = pygame.sprite.groupcollide(Needle.ship,
                                               Wedge.ship,
                                               False, False,
                                               pygame.sprite.collide_mask)
        for ship in ships_col:
            for i in ships_col[ship]:
                Functions.inertion_after_collision(ship, i)


if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
