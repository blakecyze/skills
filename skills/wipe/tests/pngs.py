"""Write solid-colour PNGs for tests, standard library only."""

import struct
import zlib
from pathlib import Path


def _chunk(tag, data):
    body = tag + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png(path, w, h, rgb):
    row = b"\x00" + bytes(rgb) * w
    raw = row * h
    data = (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw))
            + _chunk(b"IEND", b""))
    path = Path(path)
    path.write_bytes(data)
    return path
