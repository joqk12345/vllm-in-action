#!/usr/bin/env python3
"""Detect upstream drift for the Rust Frontend research topic.

This checker deliberately separates discovery from verification:

- vLLM Issue #44280 supplies the live roadmap signal.
- vllm-version-monitor supplies release-intelligence and workflow-health signals.
- vLLM releases remain the authoritative release source.

The command exits with 2 when the accepted snapshot has drifted, so it can be
used as a lightweight scheduled CI gate. Use --accept only after human review.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = (
    ROOT / "research/topics/rust-frontend/tracking/upstream-snapshot.json"
)
API_ROOT = "https://api.github.com"
ISSUE_URL = f"{API_ROOT}/repos/vllm-project/vllm/issues/44280"
LATEST_RELEASE_URL = f"{API_ROOT}/repos/vllm-project/vllm/releases/latest"
MONITOR_MANIFEST_URL = (
    f"{API_ROOT}/repos/joqk12345/vllm-version-monitor/contents/"
    "output/vllm/build_manifest.json"
)
MONITOR_RUNS_URL = (
    f"{API_ROOT}/repos/joqk12345/vllm-version-monitor/actions/workflows/"
    "vllm-monitor.yml/runs?status=success&per_page=1"
)
CHECKBOX_RE = re.compile(r"^- \[([ xX])\] (.+)$")


def fetch_json(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "vllm-in-action-rust-frontend-tracker",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def decode_content(payload: dict[str, Any]) -> Any:
    if payload.get("encoding") != "base64":
        raise ValueError("GitHub contents response is not base64 encoded")
    raw = base64.b64decode(payload["content"])
    return json.loads(raw)


def build_snapshot() -> dict[str, Any]:
    issue = fetch_json(ISSUE_URL)
    release = fetch_json(LATEST_RELEASE_URL)
    monitor_manifest_payload = fetch_json(MONITOR_MANIFEST_URL)
    monitor_manifest = decode_content(monitor_manifest_payload)
    monitor_runs = fetch_json(MONITOR_RUNS_URL)

    body = issue.get("body") or ""
    checked = 0
    unchecked = 0
    for line in body.splitlines():
        match = CHECKBOX_RE.match(line)
        if not match:
            continue
        if match.group(1).lower() == "x":
            checked += 1
        else:
            unchecked += 1

    runs = monitor_runs.get("workflow_runs", [])
    latest_run = runs[0] if runs else {}

    return {
        "schema_version": 1,
        "captured_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "roadmap": {
            "repository": "vllm-project/vllm",
            "issue": 44280,
            "url": issue["html_url"],
            "state": issue["state"],
            "updated_at": issue["updated_at"],
            "comments": issue["comments"],
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "checked_items": checked,
            "unchecked_items": unchecked,
        },
        "authoritative_release": {
            "tag": release["tag_name"],
            "published_at": release["published_at"],
            "url": release["html_url"],
        },
        "version_monitor": {
            "repository": "joqk12345/vllm-version-monitor",
            "manifest_commit": monitor_manifest_payload["sha"],
            "cutoff": monitor_manifest["cutoff"],
            "latest_stable": monitor_manifest["latest_stable"],
            "latest_successful_run_id": latest_run.get("id"),
            "latest_successful_run_at": latest_run.get("updated_at"),
            "latest_successful_run_url": latest_run.get("html_url"),
        },
    }


def compare(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    checks = [
        ("roadmap.state", "roadmap state"),
        ("roadmap.body_sha256", "roadmap body"),
        ("roadmap.comments", "roadmap comments"),
        ("roadmap.checked_items", "checked roadmap items"),
        ("roadmap.unchecked_items", "unchecked roadmap items"),
        ("authoritative_release.tag", "latest vLLM release"),
        ("version_monitor.latest_stable", "Version Monitor latest stable"),
        ("version_monitor.manifest_commit", "Version Monitor manifest"),
    ]
    changes = []
    for dotted, label in checks:
        left: Any = old
        right: Any = new
        for part in dotted.split("."):
            left = left.get(part)
            right = right.get(part)
        if left != right:
            changes.append(f"{label}: `{left}` → `{right}`")
    return changes


def render(snapshot: dict[str, Any], changes: list[str]) -> str:
    roadmap = snapshot["roadmap"]
    release = snapshot["authoritative_release"]
    monitor = snapshot["version_monitor"]
    lines = [
        "# Rust Frontend upstream tracking",
        "",
        f"- Roadmap: {roadmap['state']}, updated {roadmap['updated_at']}, "
        f"{roadmap['checked_items']} checked / "
        f"{roadmap['unchecked_items']} unchecked",
        f"- vLLM latest release: {release['tag']} ({release['published_at']})",
        f"- Version Monitor snapshot: {monitor['latest_stable']} "
        f"(cutoff {monitor['cutoff']})",
        f"- Version Monitor latest successful run: "
        f"{monitor['latest_successful_run_at'] or 'unavailable'}",
        "",
    ]
    if monitor["latest_stable"] != release["tag"]:
        lines.extend(
            [
                "⚠ Version Monitor committed snapshot differs from the "
                "authoritative vLLM latest release.",
                "",
            ]
        )
    if changes:
        lines.append("## Drift detected")
        lines.append("")
        lines.extend(f"- {change}" for change in changes)
        lines.extend(
            [
                "",
                "Review linked PRs, merge commits, release tags and tests before "
                "accepting any capability as a book fact.",
                "",
                "Review impact in this order:",
                "1. outputs/booklet/capability-matrix.yml",
                "2. feature-parity-roadmap.md and claims.yml",
                "3. topic booklet dynamic appendix and chapter handoff",
                "4. brief, figures and slides",
            ]
        )
    else:
        lines.extend(["No accepted tracking fields changed.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument(
        "--accept",
        action="store_true",
        help="replace the snapshot after completing human upstream review",
    )
    args = parser.parse_args()

    try:
        current = build_snapshot()
        accepted = json.loads(args.snapshot.read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError) as exc:
        print(f"tracking check failed: {exc}", file=sys.stderr)
        return 1

    changes = compare(accepted, current)
    print(render(current, changes))

    if args.accept:
        args.snapshot.write_text(
            json.dumps(current, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Accepted snapshot: {args.snapshot}")
        return 0
    return 2 if changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
