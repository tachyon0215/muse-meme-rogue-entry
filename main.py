#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — entry program.

The meme image (entry.png, 1024x1024) is committed next to this file;
it was rendered during the build session by draw.py. The grading
sandbox ships a bare python:3.13 with no Pillow, so this program uses
only the standard library: it copies entry.png to the output dir.
"""

import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # the gate accepts at most 1 MiB


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_SIGNATURE):
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    # Read back and confirm the copy landed whole before claiming success.
    if os.path.getsize(dst) != len(data):
        print("copied entry.png is truncated", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
