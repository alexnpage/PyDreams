#!/usr/bin/env python

"""
soft.py: Module for decompressing SoftLib archives
"""

import sys
import io
import struct
from collections import namedtuple

SoftLibHdr = namedtuple('SoftLibHdr', 'version filecount')
FileEntryHdr = namedtuple('FileEntryHdr', 'filename offset chunklen original_length compression')
ChunkHeader = namedtuple('ChunkHeader', 'header_id original_length compression')

def load_lib_shape(libname, filename):
    pass


def load_lib_file(libname, filename):
    file = open(libname, "rb")

    # Verify it is a SLIB file
    if file.read(4) != b'SLIB':
        print(libname + " is not a SLIB file.")
        file.close()
        sys.exit(1)

    # Check lib header version number
    library_header = SoftLibHdr._make(struct.unpack('<hh', file.read(4)))
    if library_header.version > 2:
        print("Unsupported SLIB file version.")
        file.close()
        sys.exit(1)

    # Manage file entry headers
    file_entry_header = 0
    file_found = False
    for x in range(0, library_header.filecount):
        file_entry_header = FileEntryHdr._make(struct.unpack('<16sIIIh', file.read(30)))
        if file_entry_header.filename.decode('ascii').rstrip('\0') == filename:
            file_found = True
            break

    chunk_header = 0
    if file_found:
        # Seek to file position
        file.seek(file_entry_header.offset, io.SEEK_CUR)

        # Read chunk header and verify id
        chunk_header = ChunkHeader._make(struct.unpack('<4shh', file.read(8)))
        if chunk_header.header_id != b'CUNK':
            print(filename + " - BAD header_id!")
            file.close()
            sys.exit(1)

        # Calculate data length without header
        chunk_len = file_entry_header.chunklen - 8

        # Extract file data
        if chunk_header.compression == 1:  # LZW
            pass
        if chunk_header.compression == 2:  # LZH
            pass
        if chunk_header.compression == 0:  # None
            pass

    print(library_header)
    print(file_entry_header)
    print(chunk_header)

    file.close()

if __name__ == '__main__':
    load_lib_file("KDREAMS.CMP", "TITLESCR.LBM")