import random
from pygamelib.assets import graphics
from pygamelib.gfx import core
from pygamelib import board_items
from blessed import Terminal
from game import media

terminal = Terminal()

from copy import deepcopy


class Cell(board_items.BoardItemComplexComponent):
    def __init__(self, **kwargs):
        board_items.BoardItemComplexComponent.__init__(self, **kwargs)
        if "multi_color" in kwargs and type(kwargs["multi_color"]) is bool:
            self.multi_color = kwargs["multi_color"]
        else:
            self.multi_color = random.choice([True, False])
        self.colors = list()
        self.sprixel = core.Sprixel("  ")
        if "color1" in kwargs and isinstance(kwargs["color1"], media.Color):
            self.colors.append(kwargs["color1"])
        else:
            self.colors.append(media.Color.random())
        self.sprixel.bg_color = terminal.on_color_rgb(
            self.colors[0].r, self.colors[0].v, self.colors[0].b
        )
        if self.multi_color:
            self.__blocks = list()
            for n in dir(graphics.Blocks):
                if n.startswith("__"):
                    continue
                self.__blocks.append(graphics.Blocks.__dict__[n])
            if "color2" in kwargs and isinstance(kwargs["color2"], media.Color):
                self.colors.append(kwargs["color2"])
            else:
                self.colors.append(self.colors.append(media.Color.random()))
            self.sprixel.model = random.choice(self.__blocks) * 2
            self.sprixel.fg_color = terminal.color_rgb(
                self.colors[1].r, self.colors[1].v, self.colors[1].b
            )

    def set_color(self, color):
        if isinstance(color, media.Color):
            self.colors[0] = color


class Organism(board_items.ComplexNPC):
    mutation_rate = 0.1

    def __init__(self, **kwargs):
        self.cells = list()
        if "cells" in kwargs and type(kwargs["cells"]) is list:
            self.cells = kwargs["cells"]
            spr = list()
            if type(self.cells[0]) is list:
                for r in self.cells:
                    nl = list()
                    for c in r:
                        nl.append(c.sprixel)
                    spr.append(nl)
                kwargs["sprite"] = core.Sprite(sprixels=spr)
            elif isinstance(self.cells[0], Cell):
                spr = list()
                for c in self.cells:
                    spr.append(c.sprixel)
                kwargs["sprite"] = core.Sprite(sprixels=[spr])
        super().__init__(**kwargs)
        self.gen = 0
        if "gen" in kwargs and type(kwargs["gen"]) is int:
            self.gen = kwargs["gen"]
        self.lifespan = 20
        if "lifespan" in kwargs and type(kwargs["lifespan"]) is int:
            self.lifespan = kwargs["lifespan"]

    def reproduce(self, other=None):
        # We can all agree that it's a little sad
        if other is None and self.lifespan >= 2:
            self.lifespan = int(self.lifespan / 2)
            return deepcopy(self)
        else:
            (min_width, max_width) = (
                min([self.width, other.width]),
                max([self.width, other.width]),
            )
            (min_height, max_height) = (
                min([self.height, other.height]),
                max([self.height, other.height]),
            )

    def mutate(self):
        pass
