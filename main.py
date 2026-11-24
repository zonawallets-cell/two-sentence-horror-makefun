"""Two-Sentence Horror — make.fun entry.

Writes one horror story of exactly two sentences to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Pure standard library only (os, re). The story is a fixed string:
a sleep-study report whose count is off by one — and the extra
breath belongs to something else in the room. 123 characters,
well inside the gate's 1-400 character limit.
"""

import os
import re

STORY = ("The sleep study said I stop breathing forty times a night. "
         "Last night it recorded forty-one, and one of them wasn't mine.")

MAX_CHARS = 400


def validate(text):
    """Enforce the competition gate: 1-400 UTF-8 chars, not only
    whitespace, and exactly two sentences. Raises ValueError on
    any violation."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d"
                         % (MAX_CHARS, len(text)))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    text.encode("utf-8")  # must be valid UTF-8
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    if len(sentences) != 2:
        raise ValueError("entry must be exactly two sentences, got %d"
                         % len(sentences))
    for s in sentences:
        if s[-1] not in ".!?":
            raise ValueError("sentence does not end with terminal "
                             "punctuation: %r" % s)
    return True


def main():
    validate(STORY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(STORY)
    # Read back and verify the file holds exactly the validated story:
    # the judge reads the file, not the string in memory. Re-validate
    # the text as read from disk, so a write that silently changed a
    # character (encoding, newline) fails here instead of at the gate.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != STORY:
        raise ValueError("entry.txt does not match the validated story")
    validate(written)
    print("wrote %d chars to %s (verified)" % (len(STORY), path))


if __name__ == "__main__":
    main()
