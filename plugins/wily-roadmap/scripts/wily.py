#!/usr/bin/env python3
"""Entry shim for Wily v3.

The implementation lives in the sibling `wily/` package. This file remains
because command docs and launchers invoke `scripts/wily.py` by path.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wily.cli.__main__ import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
