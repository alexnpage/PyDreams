#!/usr/bin/env python

"""
soft.py: Module for decompressing SoftLib archives
"""

import sys
import struct
from enum import Enum


class Compression(Enum):
    NONE = 0
    LZW = 1
    LZH = 2


class SoftLibFile:
    """
    Represents a SoftLib archive and its contents.

    The header formats are based upon commit 4348b47 of the Keen Dreams source.
    https://github.com/keendreams/keen
    """

    class SoftLibHeader:
        fmt = '<4sHH'
        len = 8  # bytes

        def __init__(self, header):
            self.id = header[0].decode('ascii')  # 4-char string
            self.version = header[1]  # unsigned short
            self.file_count = header[2]  # unsigned short

    class FileEntryHeader:
        fmt = '<16sIIIh'
        len = 30  # bytes

        def __init__(self, header):
            self.filename = header[0].decode('ascii').rstrip('\0')  # 16-char string, null-padded
            self.offset = header[1]  # unsigned int
            self.chunk_length = header[2]  # unsigned int
            self.original_length = header[3]  # unsigned int
            self.compression = Compression(header[4])  # short

    class ChunkHeader:
        fmt = '<4sIh'
        len = 10  # bytes

        def __init__(self, header):
            self.id = header[0].decode('ascii')  # 4-char string
            self.original_length = header[1]  # unsigned int
            self.compression = Compression(header[2])  # short

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'rb')

        self.library_header, self.file_entry_headers, self.chunk_headers = self._read_lib()

    def __del__(self):
        self.file.close()

    def __str__(self):
        report = "Library:\n" \
            "   ID: " + self.library_header.id + "\n" \
            "   Version: " + str(self.library_header.version) + "\n" \
            "   Files: " + str(self.library_header.file_count) + "\n\n"

        for x, header in enumerate(self.file_entry_headers):
            report += "File " + str(x+1) + ":\n" \
                "   Filename: " + header.filename + "\n" \
                "   Offset: " + format(header.offset, '#x') + "\n" \
                "   Chunk Length: " + format(header.chunk_length, '#x') + "\n" \
                "   Original Length: " + format(header.original_length, '#x') + "\n" \
                "   Compression Method: " + str(header.compression).split('.')[1] + "\n\n"

        for x, chunk in enumerate(self.chunk_headers):
            report += "Chunk " + str(x+1) + ":\n" \
                "   ID: " + chunk.id + "\n" \
                "   Original Length: " + format(chunk.original_length, '#x') + "\n" \
                "   Compression Method: " + str(chunk.compression).split('.')[1] + "\n\n"

        return report

    def _read_lib(self):

        # Unpack library header
        library_header = self.SoftLibHeader(struct.unpack(self.SoftLibHeader.fmt, self.file.read(self.SoftLibHeader.len)))

        # Verify it is an SLIB file
        if library_header.id != 'SLIB':
            print("ERROR: " + self.filename + " is not a valid SLIB file.")
            self.file.close()
            sys.exit(1)

        # Check lib header version number
        if library_header.version > 2:
            print("ERROR: Unsupported SLIB file version.")
            self.file.close()
            sys.exit(1)

        # Unpack file entry headers
        file_entry_headers = []
        for x in range(0, library_header.file_count):
            file_entry_headers.append(
                self.FileEntryHeader(struct.unpack(self.FileEntryHeader.fmt, self.file.read(self.FileEntryHeader.len)))
            )

        chunk_headers = []
        header_size = self.SoftLibHeader.len + len(file_entry_headers) * self.FileEntryHeader.len
        for header in file_entry_headers:
            self.file.seek(header.offset + header_size)
            chunk_headers.append(self.ChunkHeader(struct.unpack(self.ChunkHeader.fmt, self.file.read(self.ChunkHeader.len))))

        return library_header, file_entry_headers, chunk_headers

if __name__ == '__main__':
    print(SoftLibFile(sys.argv[1]))