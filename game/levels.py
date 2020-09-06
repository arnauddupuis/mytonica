class Level(object):
    data = {
        0: {
            "map": "maps/tutorial.json",
            "allowed_cells": 50,
            "difficulty": "easy",
            "winning_condition": 0,
            "number": 0,
            "state": 0,
        },
        1: {
            "map": "maps/lvl_01.json",
            "allowed_cells": 25,
            "difficulty": "easy",
            "winning_condition": 0,
            "number": 1,
            "state": 0,
        },
        2: {
            "map": "maps/lvl_02.json",
            "allowed_cells": 30,
            "difficulty": "easy",
            "winning_condition": 0,
            "number": 2,
            "state": 0,
        },
        3: {
            "map": "maps/lvl_03.json",
            "allowed_cells": 20,
            "difficulty": "normal",
            "winning_condition": 0,
            "number": 3,
            "state": 0,
        },
        4: {
            "map": "maps/lvl_04.json",
            "allowed_cells": 15,
            "difficulty": "normal",
            "winning_condition": 0,
            "number": 4,
            "state": 0,
        },
        5: {
            "map": "maps/lvl_02.json",
            "allowed_cells": 5,
            "difficulty": "hard",
            "winning_condition": 0,
            "number": 5,
            "state": 0,
        },
        6: {
            "map": "maps/lvl_03.json",
            "allowed_cells": 5,
            "difficulty": "hard",
            "winning_condition": 0,
            "number": 6,
            "state": 0,
        },
        7: {
            "map": "maps/lvl_04.json",
            "allowed_cells": 5,
            "difficulty": "hard",
            "winning_condition": 0,
            "number": 7,
            "state": 0,
        },
    }

    def __init__(self, lvl):
        super().__init__()
        if lvl in Level.data:
            self.map = Level.data[lvl]["map"]
            self.allowed_cells = Level.data[lvl]["allowed_cells"]
            self.difficulty = Level.data[lvl]["difficulty"]
            self.winning_condition = Level.data[lvl]["winning_condition"]
            self.number = Level.data[lvl]["number"]
            self.state = Level.data[lvl]["state"]
            self.board = None

    @staticmethod
    def max_level():
        return max(Level.data.keys())
