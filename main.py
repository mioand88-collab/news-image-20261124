#!/usr/bin/env python3
"""Entry point: copy the poster shipped in this repo to /output/entry.png.

The poster is entry.png at the repository root, rendered by
draw_poster.py. This program only copies it: it never removes /output
(the grader mounts that directory), it only creates it if missing.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # sanity: the copy must be a whole PNG of the expected size
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("entry.png copy is incomplete")


if __name__ == "__main__":
    main()
