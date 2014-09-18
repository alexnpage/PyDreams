#!/usr/bin/env python

"""
soft.py: Module for decompressing SoftLib archives
"""

import sys
import io
import struct
from collections import namedtuple

LibraryHeader = namedtuple('LibraryHeader', 'version filecount')

def load_lib_shape(libname, filename):
    pass


def load_lib_file(libname, filename):
    file = open(libname, "rb")

    # Verify it is a SLIB file
    if file.read(4) != b'SLIB':
        print(libname + " is not a SLIB file.")
        sys.exit(1)

    # Check lib header version number
    header = LibraryHeader._make(struct.unpack('<hh', file.read(4)))
    if header.version > 2:
        print("Unsupported SLIB file version.")
        sys.exit(1)

    print(header)

if __name__ == '__main__':
    load_lib_file("KDREAMS.CMP", "TITLESCR.LBM")