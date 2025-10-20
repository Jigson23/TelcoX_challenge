# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
#!/usr/bin/env python3
"""Utility to add developer signature headers to project files."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

COMMENT_STYLES: Dict[str, Tuple[str, str]] = {
    ".py": ("#", "#"),
    ".sh": ("#", "#"),
    ".env": ("#", "#"),
    ".js": ("//", "//"),
    ".ts": ("//", "//"),
    ".tsx": ("//", "//"),
    ".jsx": ("//", "//"),
    ".java": ("//", "//"),
    ".kt": ("//", "//"),
    ".c": ("//", "//"),
    ".cpp": ("//", "//"),
    ".cs": ("//", "//"),
    ".go": ("//", "//"),
    ".rs": ("//", "//"),
    ".php": ("//", "//"),
    ".rb": ("#", "#"),
    ".swift": ("//", "//"),
    ".scala": ("//", "//"),
    ".sql": ("--", "--"),
    ".yaml": ("#", "#"),
    ".yml": ("#", "#"),
    ".json": ("//", "//"),
    ".md": ("<!--", "-->")
}

DEFAULT_NAME = "Ing. Jigson Contreras"
DEFAULT_EMAIL = "supercontreras-ji@hotmail.com"


def build_signature(prefix: str, suffix: str, name: str, email: str) -> List[str]:
    if prefix == "<!--" and suffix == "-->":
        return [f"<!-- Author: {name} -->", f"<!-- Email: {email} -->", ""]

    if suffix and suffix != prefix:
        return [
            f"{prefix} Author: {name} {suffix}",
            f"{prefix} Email: {email} {suffix}",
            "",
        ]

    return [f"{prefix} Author: {name}", f"{prefix} Email: {email}", ""]


def iter_target_files(root: Path, extensions: Iterable[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        yield path


def signature_present(content: str, name: str) -> bool:
    marker = f"Author: {name}"
    return marker in content.splitlines()[:5]


def add_signature_to_file(path: Path, prefix: str, suffix: str, name: str, email: str, dry_run: bool) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False

    if signature_present(text, name):
        return False

    signature_lines = build_signature(prefix, suffix, name, email)
    updated = "\n".join(signature_lines) + text

    if dry_run:
        return True

    path.write_text(updated, encoding="utf-8")
    return True


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add a developer signature header to supported files",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root path to scan (defaults to current directory)",
    )
    parser.add_argument("--name", default=DEFAULT_NAME, help="Developer name")
    parser.add_argument("--email", default=DEFAULT_EMAIL, help="Developer email")
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=sorted(COMMENT_STYLES.keys()),
        help="File extensions to update (default: all supported)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show how many files would change without modifying them",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    root = Path(args.path).resolve()
    extensions = tuple(ext if ext.startswith(".") else f".{ext}" for ext in args.extensions)

    processed = 0
    for file_path in iter_target_files(root, extensions):
        comment_style = COMMENT_STYLES.get(file_path.suffix.lower())
        if not comment_style:
            continue
        prefix, suffix = comment_style
        changed = add_signature_to_file(file_path, prefix, suffix, args.name, args.email, args.dry_run)
        if changed:
            processed += 1

    if args.dry_run:
        print(f"{processed} file(s) would be updated.")
    else:
        print(f"Signature added to {processed} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
