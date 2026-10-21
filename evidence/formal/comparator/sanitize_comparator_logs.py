#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


ANSI = re.compile(r"\x1B(?:\[[0-?]*[ -/]*[@-~]|[@-_])")
PRIVATE_PATH = re.compile(r"(?:/home|/Users|/private/tmp|/tmp)/[^\s\]\[\"']+")
PRIVATE_IPV4 = re.compile(r"\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3}|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.(?:\d{1,3}\.)\d{1,3})\b")


def sanitize(source: Path, destination: Path) -> None:
    text = source.read_text(encoding="utf-8", errors="replace")
    text = ANSI.sub("", text).replace("\r", "\n")
    text = re.sub(r"(?m)^(Script started on [^\n]*?) \[COMMAND=.*\]$", r"\1 [COMMAND=<redacted>]", text)
    text = PRIVATE_PATH.sub("<PRIVATE_PATH>", text)
    text = PRIVATE_IPV4.sub("<PRIVATE_IP>", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create path-redacted Comparator transcripts for local review.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    arguments = parser.parse_args()
    sanitize(arguments.source, arguments.destination)


if __name__ == "__main__":
    main()
