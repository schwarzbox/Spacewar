#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Jan 24 22:53:14 2018

"""
SPACE WAR
"""

__version__ = 1.0

# 1.0 (2018 - two players, no AI, random asteroids, particle system, gravity)

# 2.0 (2018 - add ship inertion after launch torpeda, add planet, simple AI)

#
#  0_spacewar.py
#
#  Copyright (c) 2018 Alexander Veledzimovich veledz@gmail.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms pip3of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import pygame

import gui

from controller import UserInput as UINP
from effects import Dots, Stars
from functions import Functions as Func
from planets import Asteroids, Sun
from setting import Setting
from ship import Needle, Torpeda, Wedge


# init Settings
set_si = Setting()


class Main(object):

    def __init__(self):
        pygame.init()

        WID = set_si.WID
        HEI = set_si.HEI

        self.CLOCK = pygame.time.Clock()
        self.DISPLAY = pygame.display.set_mode((WID,
                                                HEI), 0, 32)
        self.DISPLAY.convert_alpha()

        # set up icon
        icon_sq = pygame.Surface((128, 128)).convert_alpha()
        icon_sq.fill(set_si.EMPTY)
        gui.Label(set_si, icon_sq.get_size()[0] // 2,
                  icon_sq.get_size()[1] // 2, 'center', icon_sq,
                  set_si.TITLEFNT, 'SW', fg=set_si.BGCLR).draw()
        pygame.display.set_icon(icon_sq)

        self.caption = 'spacewar!'
        pygame.display.set_caption(self.caption)

        pygame.mouse.set_visible(True)
        self.game()

    def game(self):
        while True:
            self.start_screen()
            # game loop
            self.game_loop()
            # game over screen
            self.end_screen()

            pygame.display.update()
            self.CLOCK.tick(set_si.FPS)

    def reset(self):
        # collision objects
        game_obj = []
        Needle(set_si, self.DISPLAY, game_obj, 'needle')
        Wedge(set_si, self.DISPLAY, game_obj, 'wedge')
        Sun(set_si, self.DISPLAY)

        Asteroids.objects.empty()
        Torpeda.objects.empty()
        Dots.objects.empty()

        return game_obj

    def circle_screen(self, exclude_obj=False):
        pdp = gui.PDP(set_si, self.DISPLAY)
        Stars.create(set_si, pdp.image, exclude_obj)
        Stars.objects.draw(pdp.image)
        return pdp

    def start_screen(self):
        run_scr = True
        menu = gui.SimpleInfo(set_si, self.DISPLAY,
                              title_txt='SPACEWAR!',
                              menu_items=[(Needle, ' W. A. S. D. E'),
                                          (Wedge, ' I. J. K. L. O')])
        # make circle screen
        pdp = self.circle_screen()

        while run_scr:
            run_scr = UINP.menu_input()

            self.DISPLAY.fill(set_si.PDPCLR)
            self.DISPLAY.blit(pdp.image, (0, 0))

            menu.draw()

            pygame.display.update()
            self.CLOCK.tick(set_si.FPS)

    def game_loop(self):
        run_loop = True

        game_obj = self.reset()

        Asteroids.create(set_si, self.DISPLAY, game_obj,
                         exclude_obj=Sun.sun, init=True)

        # make labels and round screen
        ship_info = gui.InfoBar(set_si, self.DISPLAY, Needle, Wedge,
                                Torpeda, Stars)
        # make circle screen
        pdp = self.circle_screen(Sun.sun)

        final_pause = set_si.FINALPAUSE
        while run_loop:
            run_loop = UINP.game_input(Needle, Wedge, ship_info)

            self.DISPLAY.fill(set_si.PDPCLR)
            self.DISPLAY.blit(pdp.image, (0, 0))

            ship_info.draw()

            Asteroids.create(set_si, self.DISPLAY, game_obj)

            Dots.objects.draw(self.DISPLAY)
            Dots.objects.update()

            Sun.sun.draw()
            Sun.sun.update(game_obj)

            for i in Asteroids.objects:
                if i.visible:
                    i.draw()
            Asteroids.objects.update()

            Torpeda.objects.draw(self.DISPLAY)
            Torpeda.objects.update()

            Needle.ship.draw(self.DISPLAY)
            Needle.ship.update(ship_info)

            Wedge.ship.draw(self.DISPLAY)
            Wedge.ship.update(ship_info)

            # print(len(Asteroids.objects))
            Func.collision(Sun, Asteroids, Needle, Wedge, Torpeda)

            fps_info = 'fps ' + str(round(self.CLOCK.get_fps(), 2))
            pygame.display.set_caption(
                f'{self.caption} {__version__} {fps_info}')

            # create border
            size = set_si.SCRBORDERSIZE
            pygame.draw.circle(self.DISPLAY, set_si.GAMECLR,
                               (set_si.SCRWID, set_si.SCRHEI),
                               set_si.SCRRADIUS + size, size)

            if ((not Needle.ship or not Wedge.ship) or
                    (not Needle.ship.sprite.fuel and
                     not Wedge.ship.sprite.fuel) or
                    (not Needle.ship.sprite.torpedos and
                     not Wedge.ship.sprite.torpedos)):

                final_pause -= 1
            if not final_pause:
                return

            pygame.display.update()
            self.CLOCK.tick(set_si.FPS)

    def end_screen(self):
        win_message = [(False, 'ALL SHIPS LOST IN SPACE')]

        if (Needle.ship and Needle.ship.sprite.fuel and
                Needle.ship.sprite.torpedos):
            win_message = [(Needle, 'BEST IN SPACE'),
                           (Wedge, 'DUST IN SPACE')]

        elif (Wedge.ship and Wedge.ship.sprite.fuel and
              Wedge.ship.sprite.torpedos):
            win_message = [(Wedge, 'BEST IN SPACE'),
                           (Needle, 'DUST IN SPACE')]

        run_scr = True
        menu = gui.SimpleInfo(set_si, self.DISPLAY,
                              title_txt='GAME OVER',
                              menu_items=win_message)
        # make circle screen
        pdp = self.circle_screen()

        while run_scr:
            run_scr = UINP.menu_input()

            self.DISPLAY.fill(set_si.PDPCLR)
            self.DISPLAY.blit(pdp.image, (0, 0))
            menu.draw()

            pygame.display.update()
            self.CLOCK.tick(set_si.FPS)


if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
    Main()
