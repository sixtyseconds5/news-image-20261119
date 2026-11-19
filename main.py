#!/usr/bin/env python3
"""Copy entry.png into the make.fun output directory.

Standard library only. The output directory comes from the
MAKEFUN_OUTPUT_DIR environment variable (default /output) and is
created if it does not exist yet. Exits with an error message if
entry.png is missing from this script's own directory.
"""

import os
import shutil
import sys
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: entry.png not found in {here}", file=sys.stderr)
        return 1
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")
    print(f"copied entry.png to {output_dir / 'entry.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
