#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261119 bounty.

Copies the poster (entry.png, sitting next to this file) into the
output directory named by MAKEFUN_OUTPUT_DIR, defaulting to /output.
Standard library only, no network access, no side effects beyond
that single copy.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"


def locate_source() -> str:
    """Absolute path of the poster shipped with this entry."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def run() -> int:
    source = locate_source()
    if not os.path.isfile(source):
        print(f"error: {source} is missing -- run gen_poster.py first",
              file=sys.stderr)
        return 1

    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT)
    os.makedirs(target_dir, exist_ok=True)
    destination = os.path.join(target_dir, SOURCE_NAME)
    shutil.copyfile(source, destination)
    print(f"copied {source} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
