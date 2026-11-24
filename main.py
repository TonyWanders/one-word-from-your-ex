#!/usr/bin/env python3
"""Write one word, the word an ex would use to describe you, to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The word is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 24 characters, not only white space. The file holds
exactly the word, with no trailing newline and nothing else.
"""

import os
import sys
from pathlib import Path

WORD = "forgettable"

MIN_CHARS = 1
MAX_CHARS = 24
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 24 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"word is {chars} characters, outside 1-24")
    if not text.strip():
        raise ValueError("word is only white space")
    if len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")
    return chars


def main() -> int:
    try:
        chars = validate(WORD)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(WORD, encoding="utf-8")
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
