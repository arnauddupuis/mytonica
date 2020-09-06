import random


class Note(object):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "A"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def random(cls):
        return cls()


class Chord(object):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "CEG"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def random(cls):
        return cls()


class Color(object):
    def __init__(self, r=0, g=0, b=0):
        super().__init__()
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other):
        if self.r == other.r and self.g == other.g and self.b == other.b:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    @classmethod
    def random(cls):
        return cls(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
