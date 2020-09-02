import random


class Note(object):
    def __init__(self):
        super().__init__()


class Chord(object):
    def __init__(self):
        super().__init__()


class Color(object):
    def __init__(self, r=0, v=0, b=0):
        super().__init__()
        self.r = r
        self.v = v
        self.b = b

    def __eq__(self, other):
        if self.r == other.r and self.v == other.v and self.b == other.b:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    @classmethod
    def random(cls):
        return cls(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
