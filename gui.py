#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Jan 24 22:53:14 2018
# (c) Alexander Veledzimovich

"""
GUI, Button, Label, LabelImage, SimpleInfo, InfoBar, PDP for 0_spacewar.py
"""

__version__ = 0.1

import pygame.font
from functions import Functions as Func


class GUI():
    """
    GUI
    """

    def __init__(self, set_si, x, y, anchor, DISPLAY, font):
        self.set_si = set_si
        self.DISPLAY = DISPLAY
        self.set_blink_item = set_si.FPS

    def draw(self):
        if self.blink:
            self.make_blink_item(self.image, self.rect)
        else:
            self.DISPLAY.blit(self.image, self.rect)

    @property
    def blink_item(self):
        self.__blink_item -= 1
        return self.__blink_item

    @blink_item.setter
    def set_blink_item(self, frames):
        self.__blink_item = frames

    def wrap_blink_item(func):
        def wrap(self, *args, **kwargs):
            if self.blink_item > self.set_si.FPS // 2:
                func(self, *args, **kwargs)
            if not self.blink_item:
                self.set_blink_item = self.set_si.FPS
        return wrap

    def get_txt_size(self):
        return self.font.size(self.txt)

    @wrap_blink_item
    def make_blink_item(self, *args, **kwargs):
        self.DISPLAY.blit(*args, **kwargs)

    def make_txt(self, x, y, anch):
        self.image = self.font.render(self.txt, 1, self.fg, self.bg)
        self.rect = self.image.get_rect()
        self.rect = self.make_anchor(self.rect, x, y, anch)

    def make_anchor(self, rect, x, y, anchor):
        if anchor == 'center':
            rect.centerx = x
            rect.centery = y
        elif anchor == 'n':
            rect.midtop = (x, y)
        elif anchor == 's':
            rect.midbottom = (x, y)
        elif anchor == 'w':
            rect.midleft = (x, y)
        elif anchor == 'e':
            rect.midright = (x, y)
        elif anchor == 'nw':
            rect.topleft = (x, y)
        elif anchor == 'ne':
            rect.topright = (x, y)
        elif anchor == 'se':
            rect.bottomright = (x, y)
        elif anchor == 'sw':
            rect.bottomleft = (x, y)

        return rect


class Label(GUI):
    """
    GUI Label
    """

    def __init__(self, set_si, x, y, anchor, DISPLAY, font, txt,
                 blink=False, fg=(255, 255, 255), bg=None):
        super().__init__(set_si, x, y, anchor, DISPLAY, font)
        self.txt = txt
        self.bg = bg
        self.fg = fg

        self.font = pygame.font.Font(*font)
        self.width, self.height = self.get_txt_size()

        self.blink = blink
        self.make_txt(x, y, anchor)


class LabelImage(GUI):
    """
    GUI LabelImage
    """

    def __init__(self, set_si, x, y, anchor, DISPLAY, font, img_mat, border=2,
                 blink=False, fg=(255, 255, 255), bg=None):
        super().__init__(set_si, x, y, anchor, DISPLAY, font)

        self.bg = bg
        self.fg = fg
        self.border = border
        self.font = pygame.font.Font(*font)
        self.blink = blink

        self.img = Func.make_image(img_mat, self.set_si.EMPTY, self.fg)
        self.make_image(x, y, anchor)

    def make_image(self, x, y, anch):
        wid, hei = self.img.get_size()
        wid += self.border
        hei += self.border
        self.image = pygame.Surface((wid, hei))
        self.image = self.image.convert_alpha()
        if self.bg:
            self.image.fill(self.bg)
        else:
            self.image.fill(self.set_si.EMPTY)
        img_rect = self.img.get_rect()
        img_rect = self.make_anchor(img_rect, wid // 2, hei // 2, 'center')
        self.image.blit(self.img, img_rect)
        self.rect = self.image.get_rect()
        self.rect = self.make_anchor(self.rect, x, y, anch)


class SimpleInfo():
    """
    Firsts and last menu
    """

    def __init__(self, set_si, DISPLAY,
                 title_txt='', menu_items=[],
                 press_txt='PRESS ANY KEY TO START'):
        self.set_si = set_si
        self.DISPLAY = DISPLAY
        self.title_txt = title_txt
        self.title_fnt = self.set_si.TITLEFNT
        self.menu_items = menu_items
        self.press_txt = press_txt
        self.menu_fnt = self.set_si.LABFNT
        self.menu_labels = []

        self.make_labels()

    def make_labels(self):

        wid = self.set_si.SCRWID
        hei = self.set_si.SCRHEI
        from_center = 3
        menu_str_int = 1.5

        self.title = Label(self.set_si, wid,
                           hei - self.set_si.DIST * from_center,
                           'center', self.DISPLAY, self.title_fnt,
                           self.title_txt,
                           blink=False,
                           fg=self.set_si.TXTCLR)
        last_ = 0

        for i in range(len(self.menu_items)):

            if self.menu_items[i][0]:
                self.menu_labels.append(LabelImage(
                    self.set_si,
                    wid - self.set_si.DIST * 2.5,
                    hei + i * self.set_si.DIST * menu_str_int,
                    'center', self.DISPLAY,
                    self.menu_fnt, self.menu_items[i][0].matrix,
                    blink=False, fg=self.set_si.TXTCLR))

                align = 'w'
                place = wid - self.set_si.DIST * 1.5
            else:
                align = 'center'
                place = wid

            self.menu_labels.append(Label(self.set_si,
                                          place,
                                          hei + i * self.set_si.DIST * menu_str_int,
                                          align, self.DISPLAY, self.menu_fnt,
                                          self.menu_items[i][1],
                                          blink=False,
                                          fg=self.set_si.TXTCLR))

            last_ = i * self.set_si.DIST

        self.press = Label(self.set_si, wid,
                           hei + last_ + self.set_si.DIST * from_center,
                           'center', self.DISPLAY, self.menu_fnt,
                           self.press_txt,
                           blink=True,
                           fg=self.set_si.TXTCLR)

    def draw(self):

        self.title.draw()
        [i.draw() for i in self.menu_labels]
        self.press.draw()


class InfoBar():

    """
    Ship Fuel, Torpedos, Hyperspace labels and bars
    """

    def __init__(self, set_si, DISPLAY, Needle, Wedge, Torpeda, Star):
        self.set_si = set_si
        self.DISPLAY = DISPLAY
        self.needle = Needle
        self.wedge = Wedge
        self.torpeda = Torpeda
        self.star = Star

        self.info_bars = []
        self.info_labels = []

        self.menu_fnt = self.set_si.LABFNT

        self.lb_pos = self.set_si.SCRHEI - self.set_si.DIST

        self.make_labels()
        self.make_screen()

    def make_labels(self):

        fuel_matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        all_images = (fuel_matrix, self.torpeda.matrix, self.star.matrix)
        for i in range(len(all_images)):
            self.info_labels.append(LabelImage(
                self.set_si,
                self.set_si.DIST,
                self.lb_pos + self.set_si.DIST * i,
                'center', self.DISPLAY,
                self.menu_fnt, all_images[i],
                blink=False, fg=self.set_si.BGCLR))

            self.info_labels.append(LabelImage(
                self.set_si,
                self.set_si.WID - self.set_si.DIST,
                self.lb_pos + self.set_si.DIST * i,
                'center', self.DISPLAY,
                self.menu_fnt, all_images[i],
                blink=False, fg=self.set_si.BGCLR))

    def make_screen(self):
        self.info_bars = []
        if self.needle.ship:
            needle_txt = [str(self.needle.ship.sprite.fuel),
                          str(self.needle.ship.sprite.torpedos),
                          str(self.needle.ship.sprite.hyper)]
        else:
            needle_txt = ['0', '0', '0']

        for i in range(len(needle_txt)):
            self.info_bars.append(Label(
                self.set_si,
                self.set_si.DIST * 2,
                self.lb_pos + self.set_si.DIST * i,
                'center', self.DISPLAY,
                self.menu_fnt,
                needle_txt[i],
                blink=False,
                fg=self.set_si.BGCLR))

        if self.wedge.ship:
            wedge_txt = [str(self.wedge.ship.sprite.fuel),
                         str(self.wedge.ship.sprite.torpedos),
                         str(self.wedge.ship.sprite.hyper)]
        else:
            wedge_txt = ['0', '0', '0']

        for i in range(len(wedge_txt)):
            self.info_bars.append(Label(
                self.set_si,
                self.set_si.WID - self.set_si.DIST * 2,
                self.lb_pos + self.set_si.DIST * i,
                'center', self.DISPLAY,
                self.menu_fnt,
                wedge_txt[i],
                blink=False,
                fg=self.set_si.BGCLR))

    def draw(self):
        for i in self.info_bars:
            i.draw()
        for i in self.info_labels:
            i.draw()


class PDP():
    """
    PDP screen
    """

    def __init__(self, set_si, DISPLAY):
        self.set_si = set_si
        self.DISPLAY = DISPLAY

        self.image = pygame.Surface((self.set_si.WID, self.set_si.HEI))
        self.image.fill(self.set_si.STARCLR)

        pygame.draw.circle(self.image, self.set_si.BGCLR,
                           (self.set_si.SCRWID, self.set_si.SCRHEI),
                           self.set_si.SCRRADIUS, 0)

        size = self.set_si.SCRBORDERSIZE

        pygame.draw.circle(self.image, self.set_si.GAMECLR,
                           (self.set_si.SCRWID, self.set_si.SCRHEI),
                           self.set_si.SCRRADIUS + size, size)

        self.image.set_colorkey(set_si.STARCLR)


if __name__ == '__main__':
    print(__version__)
    print(__doc__)
    print(__file__)
