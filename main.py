#!/usr/bin/env python3
"""six-word-story: write one complete story in exactly six words to /output/entry.txt.

The story is two three-word beats: an acceptance, then its reversal.
"She said yes" opens a whole relationship; "He said goodbye" closes it.
What she said yes to, and why he left, are left for the reader to fill in.

Standard library only, no network. Deterministic: the same bytes on every run.
"""

import os
import sys

# The story is built from two clauses, one per beat, so each beat can be
# checked on its own: the yes that promises a future, then the goodbye
# that takes it away.
CLAUSES = (
    "She said yes.",
    "He said goodbye.",
)

LINE = " ".join(CLAUSES)

MIN_LEN = 1
MAX_LEN = 60
WORD_COUNT = 6


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} code points, must be {MIN_LEN}-{MAX_LEN}")
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if len(text.split()) != WORD_COUNT:
        found.append(f"entry has {len(text.split())} words, must be exactly {WORD_COUNT}")
    if not stripped.endswith("."):
        found.append("entry must end as one sentence")
    return found


def main() -> int:
    if len(CLAUSES) != 2:
        print("line must be built from exactly two clauses", file=sys.stderr)
        return 1
    if any(len(clause.split()) != WORD_COUNT // 2 for clause in CLAUSES):
        print("each clause must be exactly three words", file=sys.stderr)
        return 1
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output is a root-owned
    # directory, so a failed chmod must never fail the run.
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    written = open(path, "rb").read()
    if written != text.encode("utf-8"):
        print("wrote back bytes do not match entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
