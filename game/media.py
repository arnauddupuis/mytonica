import random
import numpy as np
import simpleaudio as sa


class Note(object):
    base_line = {
        "C": 261.63,
        "C#": 277.18,
        "D": 293.66,
        "D#": 311.13,
        "E": 329.63,
        "F": 349.23,
        "F#": 369.99,
        "G": 392,
        "G#": 415.3,
        "A": 440,
        "A#": 466.16,
        "B": 493.88,
    }
    sample_rate = 44100
    T = 0.1

    def __init__(self, name="A"):
        super().__init__()
        self.name = name
        self.media_buffer = None
        self.generate_audio()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    def generate_audio(self):
        # code from SimpleAudio example

        # get timesteps for each sample, T is note duration in seconds
        t = np.linspace(0, Note.T, int(Note.T * Note.sample_rate), False)

        # generate sine wave notes
        note = np.sin(Note.base_line[self.name] * t * 2 * np.pi)
        self.raw = note
        # concatenate notes
        self.audio = np.hstack((note))
        # normalize to 16-bit range
        self.audio *= 32767 / np.max(np.abs(self.audio))
        # convert to 16-bit data
        self.audio = self.audio.astype(np.int16)

    @classmethod
    def random(cls):
        return cls(random.choice(list(Note.base_line.keys())))

    def play(self):
        if self.media_buffer is None or not self.media_buffer.is_playing():
            self.media_buffer = sa.play_buffer(self.audio, 1, 2, Note.sample_rate)


class Chord(object):
    base_line = {
        "CEG": ["C", "E", "G"],
        "DFA": ["D", "F", "A"],
        "EGB": ["E", "G", "B"],
        "FAC": ["F", "A", "C"],
        "GBD": ["G", "B", "D"],
        "ACE": ["A", "C", "E"],
        "BDF": ["B", "D", "F"],
    }

    def __init__(self, name="CEG"):
        super().__init__()
        self.name = name
        self.media_buffer = None
        self.generate_audio()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    @classmethod
    def random(cls):
        return cls(random.choice(list(Chord.base_line.keys())))

    def generate_audio(self):
        n1 = Note(Chord.base_line[self.name][0])
        n2 = Note(Chord.base_line[self.name][1])
        n3 = Note(Chord.base_line[self.name][2])
        self.audio = np.hstack((n1.raw, n2.raw, n3.raw))
        # normalize to 16-bit range
        self.audio *= 32767 / np.max(np.abs(self.audio))
        # convert to 16-bit data
        self.audio = self.audio.astype(np.int16)

    def play(self):
        if self.media_buffer is None or not self.media_buffer.is_playing():
            self.media_buffer = sa.play_buffer(self.audio, 1, 2, Note.sample_rate)


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
