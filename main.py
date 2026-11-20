#!/usr/bin/env python3
"""Deliver the 19 November 2026 news poster as the entry image.

The poster itself lives in this repository as entry.png, drawn at build
time by draw_poster.py. All this program does is place a copy of it in
the output directory the grader provides, so the run needs no network,
does no drawing, and always produces the same bytes.
"""

import hashlib
import os
import shutil
import sys

POSTER = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, POSTER)
    if not os.path.exists(src):
        print(f"missing {POSTER} next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, POSTER)
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dst_hash:
        print("copied file differs from source", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
