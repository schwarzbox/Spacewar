#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Jan 24 22:53:14 2018
# (c) Alexander Veledzimovich

"""
Setting for 0_spacewar.py
"""

__version__ = 0.1


class Setting():
    """
    Constants
    """

    def __init__(self):
        self.FPS = 30

        self.WID = 1024
        self.HEI = 768
        self.SCRWID = self.WID // 2
        self.SCRHEI = self.HEI // 2
        self.DIST = 30
        self.SCRRADIUS = self.SCRHEI - self.DIST
        self.SCRBORDERSIZE = 20

        self.BLACKBLUE = (0, 0, 35, 255)
        self.GRAY = (128, 128, 128, 128)
        self.WHITE = (255, 240, 240)
        self.DARKCYAN = (0, 130, 155, 255)
        self.LIGHTCYAN = (50, 110, 160, 255)

        self.EMPTY = (255, 255, 255, 0)

        self.APPNAME = 'Spacewar!'
        self.TITLEFNT = ('pdp1.ttf', 80)
        self.LABFNT = ('pdp1.ttf', 20)
        self.BGCLR = self.BLACKBLUE
        self.TXTCLR = self.DARKCYAN
        self.GAMECLR = self.DARKCYAN
        self.PDPCLR = self.LIGHTCYAN

        self.FINALPAUSE = self.FPS * 3

        self.SHIPPOS = {'needle': (self.SCRWID - self.SCRRADIUS + self.DIST,
                                   self.SCRHEI),
                        'wedge': (self.SCRWID + self.SCRRADIUS - self.DIST,
                                  self.SCRHEI)}

        self.INITANGLE = {'needle': 1, 'wedge': 179, 'asteroid': 1}
        self.FUEL = 256
        self.SPEED_DT = 0.2
        self.ROTATE_DT = 0.1
        self.MAXSPEED = 6
        self.MAXROTSPEED = 3
        self.HYPERJUMP = 3
        self.SHIPBOOM = 64

        self.NUMTORPEDOS = 9
        self.TORPEDASPEED = 0.6
        self.TORPEDAMAXSPEED = 10
        self.TORPEDADIST = 80

        self.SUNRAD = 32
        self.SUNGRAV = 0.0008
        self.SUNGRAVRAD = 256
        self.SUNDT = 1

        self.STARS = 64
        self.STARCLR = self.GRAY
        self.STARSIZE = [2, 4]

        self.INITASTER = 48
        self.TIMETOBORN = 14
        self.ASTDT = (-3, 4)
        self.ASTSIZE = [4, 6, 8, 10, 12, 16, 18]
        self.ASTMAKE = 16
        self.ASTBOOM = 24

        self.DOTSDT = (-1, 2)

    def init_dynamic_settings(self):
        pass

    def reset_dynamic_settings(self):
        pass


if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
