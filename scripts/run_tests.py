#!/usr/bin/env python
"""Run the Photologue Django unit tests from the example project."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    example_project = repo_root / "example_project"
    manage_py = example_project / "manage.py"

    test_args = sys.argv[1:] or ["photologue"]
    command = [sys.executable, str(manage_py), "test", *test_args]

    return subprocess.call(command, cwd=str(example_project))


if __name__ == "__main__":
    raise SystemExit(main())
