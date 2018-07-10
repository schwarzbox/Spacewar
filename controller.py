#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Jan 24 22:53:14 2018
# (c) Alexander Veledzimovich

"""
UserInput for 0_spacewar.py
"""

__version__ = 0.1

from sys import exit as sys_exit

import pygame
from pygame.locals import *


class UserInput():
    """
    Controller
    """
    def menu_input():
        for e in pygame.event.get():
            if e.type == QUIT:
                UserInput.make_exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or (e.key == K_q and e.mod == 1024):
                    UserInput.make_exit()
                return False

        return True

    def game_input(Needle, Wedge, ship_info):
        for e in pygame.event.get():
            if e.type == QUIT:
                UserInput.make_exit()

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or (e.key == K_q and e.mod == 1024):
                    UserInput.make_exit()
                # exit game loop
                if (e.key == K_r and e.mod == 1024):
                    return False

                if Needle.ship.sprite:
                    if e.key == K_w:
                        Needle.ship.sprite.power = True
                    if e.key == K_a:
                        Needle.ship.sprite.left = True
                    if e.key == K_d:
                        Needle.ship.sprite.right = True
                    if e.key == K_s:
                        Needle.ship.sprite.launch_torpeda(ship_info)
                    if e.key == K_e:
                        Needle.ship.sprite.hyper_jump(ship_info)

                if Wedge.ship.sprite:
                    if e.key == K_i:
                        Wedge.ship.sprite.power = True
                    if e.key == K_j:
                        Wedge.ship.sprite.left = True
                    if e.key == K_l:
                        Wedge.ship.sprite.right = True
                    if e.key == K_k:
                        Wedge.ship.sprite.launch_torpeda(ship_info)
                    if e.key == K_o:
                        Wedge.ship.sprite.hyper_jump(ship_info)

            if e.type == KEYUP:
                if Needle.ship.sprite:
                    if e.key == K_w:
                        Needle.ship.sprite.power = False
                    if e.key == K_a:
                        Needle.ship.sprite.left = False
                    if e.key == K_d:
                        Needle.ship.sprite.right = False
                if Wedge.ship.sprite:
                    if e.key == K_i:
                        Wedge.ship.sprite.power = False
                    if e.key == K_j:
                        Wedge.ship.sprite.left = False
                    if e.key == K_l:
                        Wedge.ship.sprite.right = False

        return True

    def make_exit():
        pygame.quit()
        sys_exit()


if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
