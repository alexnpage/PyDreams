#!/usr/bin/env python

"""
pydreams.py: The main script for PyDreams.
"""

import sys

import pd_demo

if __name__ == "__main__":

    # Handle arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "-v":
            print("\nPyDreams version 0.1")
            print("Keen Dreams Copyright 1991-1993 Softdisk Publishing.")
            print("Commander Keen is a trademark of Id Software.")
            sys.exit(0)

        if sys.argv[1].lower() == "-h":
            print("\nPyDreams version 0.1")
            print("Keen Dreams Copyright 1991-1993 Softdisk Publishing.\n")
            print("Type \"python pydreams.py\" from the command line to run.\n")
            print("python pydreams.py -v for version and compatibility information")
            print("python pydreams.py -h for this help information")
            sys.exit(0)

    # TODO: Consider the other arguments

    demo = pd_demo.PDDemo()
    demo.loop()  # This should cleanly quit when done

    print("wat how this happen")
    sys.exit(1)