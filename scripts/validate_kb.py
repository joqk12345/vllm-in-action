#!/usr/bin/env python3
"""Validate the lightweight book knowledge-base contract without dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPINE = ROOT / "book/spine.yml"

REQUIRED_PATHS = [
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "book/STATUS.md",
    ROOT / "book/toc.yml",
    SPINE,
    ROOT / "book/chapter-briefs",
    ROOT / "book/chapters",
    ROOT / "book/evidence/source-ledger/cards",
    ROOT / "research/releases",
    ROOT / "research/watchlist.yml",
    ROOT / "templates/source-card.md",
    ROOT / "templates/experiment.md",
]

REQUIRED_BRIEF_KEYS = {
    "chapter_id",
    "part",
    "title",
    "status",
    "evidence_status",
}
ALLOWED_CHAPTER_STATUS = {"brief", "researching", "draft", "review", "ready"}
ALLOWED_SOURCE_STATUS = {"captured", "verified", "cited", "stale"}
ALLOWED_EVIDENCE_GRADES = {"A", "B", "C", "D"}


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening front matter delimiter")

    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip("\"'")
            data[match.group(1)] = value
    raise ValueError("missing closing front matter delimiter")


def spine_chapters() -> list[str]:
    text = SPINE.read_text(encoding="utf-8")
    return re.findall(r'^\s+- "(\d{2}-[^"]+)"\s*$', text, re.MULTILINE)


def spine_files() -> list[Path]:
    text = SPINE.read_text(encoding="utf-8")
    return [
        ROOT / match
        for match in re.findall(r"^\s+- file:\s*(\S+)\s*$", text, re.MULTILINE)
    ]


def validate() -> list[str]:
    errors: list[str] = []

    for path in REQUIRED_PATHS:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(ROOT)}")

    if errors or not SPINE.exists():
        return errors

    chapters = spine_chapters()
    if not chapters:
        errors.append("book/spine.yml contains no chapter slugs")
        return errors
    if len(chapters) != len(set(chapters)):
        errors.append("book/spine.yml contains duplicate chapter slugs")

    expected_briefs = {f"{slug}.md" for slug in chapters}
    actual_briefs = {
        path.name for path in (ROOT / "book/chapter-briefs").glob("*.md")
    }
    for name in sorted(expected_briefs - actual_briefs):
        errors.append(f"missing chapter brief: book/chapter-briefs/{name}")
    for name in sorted(actual_briefs - expected_briefs):
        errors.append(f"orphan chapter brief not present in spine: {name}")

    for slug in chapters:
        brief = ROOT / "book/chapter-briefs" / f"{slug}.md"
        if not brief.exists():
            continue
        try:
            metadata = parse_front_matter(brief)
        except ValueError as exc:
            errors.append(f"{brief.relative_to(ROOT)}: {exc}")
            continue
        missing = REQUIRED_BRIEF_KEYS - metadata.keys()
        if missing:
            errors.append(
                f"{brief.relative_to(ROOT)}: missing keys {', '.join(sorted(missing))}"
            )
        if metadata.get("chapter_id") != slug:
            errors.append(
                f"{brief.relative_to(ROOT)}: chapter_id must equal {slug!r}"
            )
        status = metadata.get("status")
        if status and status not in ALLOWED_CHAPTER_STATUS:
            errors.append(f"{brief.relative_to(ROOT)}: invalid status {status!r}")

    for declared in spine_files():
        if not declared.exists():
            errors.append(
                f"book/spine.yml references missing file: {declared.relative_to(ROOT)}"
            )

    cards_dir = ROOT / "book/evidence/source-ledger/cards"
    source_ids: set[str] = set()
    for card in sorted(cards_dir.glob("*.md")):
        try:
            metadata = parse_front_matter(card)
        except ValueError as exc:
            errors.append(f"{card.relative_to(ROOT)}: {exc}")
            continue
        source_id = metadata.get("source_id", "")
        if not re.fullmatch(r"SRC-[a-z0-9][a-z0-9-]*", source_id):
            errors.append(f"{card.relative_to(ROOT)}: invalid source_id {source_id!r}")
        if source_id and card.stem != source_id:
            errors.append(
                f"{card.relative_to(ROOT)}: filename must match source_id {source_id!r}"
            )
        if source_id in source_ids:
            errors.append(f"duplicate source_id: {source_id}")
        source_ids.add(source_id)
        status = metadata.get("status")
        if status not in ALLOWED_SOURCE_STATUS:
            errors.append(f"{card.relative_to(ROOT)}: invalid status {status!r}")
        grade = metadata.get("evidence_grade")
        if grade not in ALLOWED_EVIDENCE_GRADES:
            errors.append(
                f"{card.relative_to(ROOT)}: invalid evidence_grade {grade!r}"
            )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"Knowledge-base validation failed ({len(errors)} error(s)):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Knowledge-base validation passed: "
        f"{len(spine_chapters())} chapters, "
        f"{len(list((ROOT / 'book/evidence/source-ledger/cards').glob('*.md')))} "
        "source cards."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
