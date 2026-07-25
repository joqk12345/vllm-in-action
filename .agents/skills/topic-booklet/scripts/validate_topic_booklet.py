#!/usr/bin/env python3
"""Validate a topic-booklet bundle using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CLAIM_DEF_RE = re.compile(r"^\s*-\s+id:\s*[\"']?([A-Z][A-Z0-9-]*-C\d+)")
CLAIM_REF_RE = re.compile(r"\b([A-Z][A-Z0-9-]*-C\d+)\b")
SOURCE_RE = re.compile(r"\b(SRC-[A-Za-z0-9-]+)\b")
SOURCE_DEF_RE = re.compile(r"^source_id:\s*[\"']?([^\"'\s]+)", re.MULTILINE)


def validate(topic_dir: Path) -> list[str]:
    errors: list[str] = []
    topic_id = topic_dir.name
    claims_path = topic_dir / "claims.yml"
    booklet_dir = topic_dir / "outputs/booklet"
    deliverables_path = topic_dir / "outputs/deliverables.yml"
    root = topic_dir.resolve().parents[2]

    required = [
        booklet_dir / "README.md",
        booklet_dir / f"{topic_id}-topic-booklet.md",
        booklet_dir / "seminar-guide.md",
        booklet_dir / "reading-list.md",
        booklet_dir / "capability-matrix.yml",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required booklet file: {path}")

    main_booklet = booklet_dir / f"{topic_id}-topic-booklet.md"
    if main_booklet.is_file():
        main_text = main_booklet.read_text(encoding="utf-8")
        required_sections = {
            "shared research questions": "共同研究问题",
            "minimal concept system": "最小概念系统",
            "cross-source claims": "跨来源命题",
            "source correction": "来源如何相互校正",
            "open questions": "未决问题",
            "tests or experiments": "实验",
            "production decision": "生产采用",
            "layered conclusions": "结论分层",
            "dynamic appendix": "动态附录",
            "seminar decision template": "研讨结论模板",
        }
        for label, marker in required_sections.items():
            if marker not in main_text:
                errors.append(f"main booklet missing section: {label}")

    if not claims_path.is_file():
        errors.append(f"missing claim spine: {claims_path}")
        claim_ids: set[str] = set()
    else:
        claims_text = claims_path.read_text(encoding="utf-8")
        claim_ids = {
            match.group(1)
            for line in claims_text.splitlines()
            if (match := CLAIM_DEF_RE.match(line))
        }
        if not claim_ids:
            errors.append(f"no claim IDs found in: {claims_path}")
        claim_blocks = re.split(r"(?=^\s*-\s+id:)", claims_text, flags=re.MULTILINE)
        for block in claim_blocks:
            match = re.search(r"^\s*-\s+id:\s*[\"']?([^\"'\s]+)", block)
            if not match:
                continue
            claim_id = match.group(1)
            if "verification_gap:" not in block:
                errors.append(f"claim missing verification_gap: {claim_id}")
            if (
                "counterexample:" not in block
                and "invalid_generalization:" not in block
            ):
                errors.append(
                    f"claim missing counterexample/invalid_generalization: {claim_id}"
                )

    source_cards = root / "book/evidence/source-ledger/cards"
    source_ids: set[str] = set()
    if not source_cards.is_dir():
        errors.append(f"missing source-card directory: {source_cards}")
    else:
        for card in source_cards.glob("*.md"):
            match = SOURCE_DEF_RE.search(card.read_text(encoding="utf-8"))
            if match:
                source_ids.add(match.group(1))

    booklet_text = ""
    for path in booklet_dir.glob("*") if booklet_dir.is_dir() else []:
        if path.suffix in {".md", ".yml", ".yaml"}:
            booklet_text += "\n" + path.read_text(encoding="utf-8")

    undefined_claims = sorted(set(CLAIM_REF_RE.findall(booklet_text)) - claim_ids)
    for claim_id in undefined_claims:
        errors.append(f"undefined claim referenced by booklet: {claim_id}")

    undefined_sources = sorted(set(SOURCE_RE.findall(booklet_text)) - source_ids)
    for source_id in undefined_sources:
        errors.append(f"missing source card for booklet reference: {source_id}")

    if deliverables_path.is_file():
        deliverables = deliverables_path.read_text(encoding="utf-8")
        for path in required:
            relative = path.relative_to(topic_dir / "outputs").as_posix()
            if relative not in deliverables:
                errors.append(f"deliverable path not registered: {relative}")
    else:
        errors.append(f"missing deliverables manifest: {deliverables_path}")

    matrix_path = booklet_dir / "capability-matrix.yml"
    if matrix_path.is_file():
        matrix = matrix_path.read_text(encoding="utf-8")
        for field in (
            "schema_version:",
            "topic:",
            "as_of:",
            "target_release:",
            "roadmap_status:",
            "release_status:",
            "local_test_status:",
            "source_ids:",
        ):
            if field not in matrix:
                errors.append(f"capability matrix missing field: {field}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("topic_dir", type=Path)
    args = parser.parse_args()

    errors = validate(args.topic_dir)
    if errors:
        print(f"Topic-booklet validation failed ({len(errors)} error(s)):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Topic-booklet validation passed: {args.topic_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
