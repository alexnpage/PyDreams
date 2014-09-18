#!/usr/bin/env python

"""
pd_demo.py: Initializes the demo and handles the demo loop
"""

import sys

import sfml as sf


class PDDemo():
    def __init__(self):
        # Constants
        self.game_size = sf.Vector2(320, 200)  # TODO: Make this variable

        # Init window
        w, h = self.game_size
        self.window = sf.RenderWindow(sf.VideoMode(w, h), "PyDreams 0.1")
        self.window.vertical_synchronization = True

        # TODO: Init/load sounds

    def loop(self):
        # Demo loop
        while self.window.is_open:
            # Events
            for event in self.window.events:
                if type(event) is sf.CloseEvent:
                    self.window.close()

                if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.ESCAPE:
                    self.window.close()

            self.window.clear(sf.Color(0, 0, 0))
            self.window.display()
        sys.exit(0)