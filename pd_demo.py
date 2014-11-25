#!/usr/bin/env python

"""
pd_demo.py: Initializes the demo and handles the demo loop
"""

import sys

import sdl2
import sdl2.ext as sdl


class PDDemo():
    def __init__(self):
        # Constants
        window_size = (640, 400)  # TODO: Make these variable
        self.game_size = (320, 200)

        # Init window
        sdl.init()
        self.window = sdl.Window("PyDreams 0.1", size=window_size)
        self.window.show()

        # Running?
        self.running = True

        # TODO: Init/load sounds

    def loop(self):
        # Demo loop
        while self.running:
            # Events
            for event in sdl.get_events():
                if event.type == sdl2.SDL_QUIT:
                    self.running = False
                    break

                if event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.running = False
                    break

            sdl.fill(self.window.get_surface(), sdl.Color(0, 0, 0))
            self.window.refresh()
        sys.exit(0)