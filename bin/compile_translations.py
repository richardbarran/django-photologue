#!/usr/bin/env python
"""Validate and compile Photologue's translations with GNU gettext."""

import subprocess
import tempfile
from pathlib import Path


def main():
    locale_dir = Path(__file__).resolve().parents[1] / "photologue" / "locale"
    for source in sorted(locale_dir.glob("*/LC_MESSAGES/django.po")):
        # Replace a committed catalogue only after compilation succeeds.
        with tempfile.TemporaryDirectory(dir=source.parent) as directory:
            output = Path(directory) / "django.mo"
            subprocess.run(
                ["msgfmt", "--check-format", "-o", str(output), str(source)],
                check=True,
            )
            output.replace(source.with_suffix(".mo"))


if __name__ == "__main__":
    main()
