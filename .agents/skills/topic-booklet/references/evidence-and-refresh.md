# Evidence and refresh policy

## Evidence hierarchy

Apply the repository's `AGENTS.md` definitions. In booklet work:

| Grade | Use |
|---|---|
| A | Support stable factual claims when version and scope are explicit |
| B | Support factual claims with an explicit “not locally reproduced” boundary |
| C | Supply narrative or an independent observation only after A/B cross-checking |
| D | Discover questions; never support a published factual conclusion |

Do not quote ASR transcripts as authoritative statements or promote transcript-only numbers.

## Source responsibilities

- Upstream release/tag/commit/source/test/PR/documentation: final version-specific technical authority.
- Roadmap or Issue: dynamic intent and work-state signal.
- Version Monitor: release discovery and preliminary triage.
- Local experiments: evidence for the recorded target workload only.
- Public talks and third-party benchmarks: explanatory or comparative evidence within their disclosed method.

Floating `main` is acceptable for navigation during research. Bind stable conclusions to a release tag or exact commit.

## Claim requirements

Every factual claim must expose:

- claim ID;
- claim class;
- Source ID;
- evidence grade;
- version or capture date;
- model/hardware/topology where relevant;
- invalid generalization or counterexample;
- verification gap.

Keep engineering judgments distinct from the evidence grade of their factual basis.

## Capability state model

Never compress capability state into a single boolean. At minimum record:

```yaml
roadmap_status: checked | unchecked | discussion-required
release_status: unverified | verified | not-in-target
local_test_status: not-run | passed | failed | partial
```

Interpretation:

- `checked` means observed in the upstream roadmap.
- `verified` means the merge commit and first containing release/tag were established and the target tag was inspected.
- `passed` means this repository contains a reproducible test for the stated workload.

One state never implies another.

## Refresh order

After upstream drift:

1. Read the accepted snapshot and change log.
2. Inspect the roadmap diff and comments.
3. Find linked PRs, merge commits, tests, and the first containing release.
4. Use Version Monitor to locate release-note candidates.
5. Verify against the authoritative vLLM tag.
6. Update `capability-matrix.yml`.
7. Update claims and source cards only when evidence warrants it.
8. Refresh the booklet dynamic appendix.
9. Modify the stable body only for stable claim changes.
10. Mark or refresh affected Brief, handoff, figures, and slides.

Accepting a tracking snapshot means the change was triaged, not that every capability was released or tested.

## Benchmark gate

Record:

```text
version × model × hardware × precision × parallelism
× prompt/output distribution × concurrency × arrival rate
× cache state × frontend process count × metrics
```

State missing metrics. Include frontend-bound and GPU-bound controls before making production performance recommendations.

## Publication and rights

Keep raw third-party material separate from derived synthesis. If redistribution rights are unclear, flag the material before public publication or repository licensing.
