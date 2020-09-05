import random
from pygamelib.assets import graphics
from pygamelib.gfx import core
from pygamelib import board_items, constants
from blessed import Terminal
from game import media
import time
from copy import deepcopy

terminal = Terminal()


class Cell(board_items.BoardItemComplexComponent):
    def __init__(self, **kwargs):
        if "type" not in kwargs:
            kwargs["type"] = "cell"
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
            self.colors[0].r, self.colors[0].g, self.colors[0].b
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
                self.colors[1].r, self.colors[1].g, self.colors[1].b
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
        if "type" not in kwargs:
            kwargs["type"] = "organism"
        super().__init__(**kwargs)
        self.gen = 0
        if "gen" in kwargs and type(kwargs["gen"]) is int:
            self.gen = kwargs["gen"]
        self.lifespan = 5
        if "lifespan" in kwargs and type(kwargs["lifespan"]) is int:
            self.lifespan = kwargs["lifespan"]
        self.initial_lifespan = self.lifespan
        self.starting_position = [0, 0]
        if "starting_position" in kwargs and type(kwargs["starting_position"]) is int:
            self.starting_position = kwargs["starting_position"]
        self.timestamp = time.time()

    def reproduce(self, other=None):
        # We can all agree that it's a little sad
        if other is None:
            if self.lifespan >= 2:
                self.lifespan = int(self.lifespan / 2)
                o = deepcopy(self)
                o.initial_lifespan = o.lifespan
                return o
            return None
        else:
            new_width = random.randint(
                min([self.width, other.width]), max([self.width, other.width]),
            )
            new_height = random.randint(
                min([self.height, other.height]), max([self.height, other.height]),
            )
            # size: [width, height]
            # unicellular organisms have a chance to become multicellular
            # We'll treat each cell as a "gene"
            c = media.Color(0, 0, 0)
            mix = random.random()
            for elt in ["r", "g", "b"]:
                # Organisms can take either the genome of parent 1 or parent 2 or a
                # blending of them. They have 40% chance to take a gradient from one or
                # the other parent and 60% chance to be a mix (20% perfect mix, 20%
                # closer to parent 1 and 20% closer to parent 2).

                if mix <= 0.2:
                    c.__setattr__(elt, self.cells[0].colors[0].__getattribute__(elt))
                elif mix <= 0.4:
                    c.__setattr__(elt, other.cells[0].colors[0].__getattribute__(elt))
                else:
                    distance = 1
                    factor = 1
                    if mix <= 0.6:
                        # perfect mix
                        distance = 2
                    elif mix <= 0.8:
                        # closer to self
                        distance = 3
                    else:
                        # closer to other
                        factor = 2
                        distance = 3
                    c.__setattr__(
                        elt,
                        round(
                            (
                                self.cells[0].colors[0].__getattribute__(elt)
                                + other.cells[0].colors[0].__getattribute__(elt)
                            )
                            * (factor / distance)
                        ),
                    )
            new = Organism(
                size=[new_width, new_height], cells=[Cell(multi_color=False, color1=c)],
            )
            return new

    def mutate(self):
        pass


class GeneticMaterial(board_items.GenericActionableStructure):
    genetic_material_model = (
        graphics.GeometricShapes.CIRCLE_WITH_LOWER_HALF_BLACK
        + graphics.GeometricShapes.CIRCLE_WITH_UPPER_HALF_BLACK
    )

    def __init__(self, **kwargs):
        kwargs["perm"] = constants.NPC_AUTHORIZED
        super().__init__(**kwargs)
        self.color = media.Color.random()
        if "color" in kwargs and isinstance(kwargs["color"], media.Color):
            self.color = kwargs["color"]
        self.note = media.Note.random()
        if "note" in kwargs and isinstance(kwargs["note"], media.Note):
            self.note = kwargs["note"]
        self.chord = media.Chord.random()
        if "chord" in kwargs and isinstance(kwargs["chord"], media.Chord):
            self.chord = kwargs["chord"]
        self.directions = list()
        if "directions" in kwargs and type(kwargs["directions"]) is list:
            self.directions = kwargs["directions"]
        else:
            directions = [
                constants.UP,
                constants.DOWN,
                constants.LEFT,
                constants.RIGHT,
                constants.DLDOWN,
                constants.DLUP,
                constants.DRDOWN,
                constants.DRUP,
            ]
            for _ in range(0, random.randint(0, 5)):
                self.directions.append(random.choice(directions))
        if "sprixel" in kwargs:
            self.sprixel = kwargs["sprixel"]
        else:
            self.sprixel = core.Sprixel(
                GeneticMaterial.genetic_material_model,
                fg_color=terminal.color_rgb(self.color.r, self.color.g, self.color.b),
                is_bg_transparent=True,
            )
