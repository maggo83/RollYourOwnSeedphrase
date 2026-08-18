#!/usr/bin/env python3
"""Run the complete build and test suite with the pinned test-only reference dependency."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(arguments: list[str]) -> None:
    subprocess.run(arguments, cwd=ROOT, check=True)


def main() -> int:
    try:
        run([sys.executable, "build-guides.py", "all"])
        run([sys.executable, "-m", "unittest", "discover", "-s", "offline-package/tests", "-p", "test_*.py", "-v"])
        run(["node", "offline-package/tests/test_core.js"])
        run(["node", "--check", "guide-src/script.js"])
        run(["node", "--check", "offline-package/src/sha256.js"])
        run(["node", "--check", "offline-package/src/bits-words.js"])
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        return 1
    print("all offline-package verification checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
