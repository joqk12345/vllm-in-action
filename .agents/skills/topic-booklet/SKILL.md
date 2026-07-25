---
name: topic-booklet
description: Systematically generate or refresh a Markdown topic-research booklet from an existing research/topics/<topic> directory. Use when Codex must synthesize multiple sources by shared questions, create a seminar guide and reading path, maintain a machine-readable capability matrix, integrate booklet deliverables, or refresh those outputs after upstream roadmap or release drift. Do not use for a single-source summary, direct chapter drafting, or slide/PDF generation.
---

# Topic Booklet

Transform an existing research topic into a question-driven booklet for technical seminars, decisions, and later chapter handoff.

## Required inputs

Require a target `research/topics/<topic>` directory. Accept optional audience, seminar duration, target release/commit, and priority questions.

If the topic is uniquely implied, proceed without asking. Stop only when the topic is missing, ambiguous, or lacks material whose absence would materially change the result.

Do not depend on an external Inbox.

## Read before editing

1. Read the repository `AGENTS.md` completely.
2. Read `research/topics/README.md` and `templates/topic-booklet.md`.
3. Read the target topic's README, `claims.yml`, vocabulary, research notes, tracking records, existing outputs, and referenced source cards.
4. Inspect Git status and preserve unrelated or user-authored changes.
5. Read [references/evidence-and-refresh.md](references/evidence-and-refresh.md).
6. Read [references/output-contract.md](references/output-contract.md) before creating or restructuring booklet files.

## Workflow

### 1. Establish the research frame

- Define 3–7 shared research questions.
- Reuse or refine the topic's smallest systematic nouns/verbs.
- Use `claims.yml` as the claim spine.
- Record target version, model, hardware, topology, verification date, assumptions, and open questions.

Do not organize the booklet as sequential summaries of individual sources.

### 2. Synthesize across sources

For each research question:

- extract propositions from multiple sources;
- state what each source can and cannot prove;
- align version and workload boundaries;
- identify conflicts, time gaps, counterexamples, and invalid generalizations;
- classify conclusions as upstream fact, benchmark observation, engineering judgment, hypothesis, or stale conclusion.

Convert unresolved questions into upstream checks, capability tests, experiments, canary conditions, or rollback drills.

### 3. Build or refresh the booklet bundle

Maintain these files under `research/topics/<topic>/outputs/booklet/`:

- `README.md`
- `<topic>-topic-booklet.md`
- `seminar-guide.md`
- `reading-list.md`
- `capability-matrix.yml`

Follow the exact responsibilities in [references/output-contract.md](references/output-contract.md).

When refreshing, update the capability matrix first. Rewrite the stable booklet body only when stable claims changed; keep checkbox counts, release numbers, parser lists, and similar volatile facts in the dynamic appendix.

### 4. Integrate the output

- Register every booklet file in `outputs/deliverables.yml`.
- Separate artifact completion from research maturity.
- Add links from the topic README and outputs README.
- If tracking exists, make the capability matrix the first review point after drift.
- Check Brief, chapter handoff, figures, and slides for downstream staleness.
- Mark unsynchronized artifacts `research_status: needs-refresh` with a concrete reason.

Do not edit formal book chapters unless the user explicitly requests chapter integration.

### 5. Validate

Run:

```bash
python3 .agents/skills/topic-booklet/scripts/validate_topic_booklet.py \
  research/topics/<topic>
python3 scripts/validate_kb.py
git diff --check
```

Also parse modified YAML with an available safe parser. If the topic has an upstream tracking command, run it when network permission is available; otherwise report that it was not run.

Fix validation failures caused by the task. Preserve unrelated pre-existing failures and report them precisely.

## Boundaries

- Write booklet content in Markdown and capability data in YAML.
- Do not create PPTX, DOCX, PDF, or install tools.
- Do not delete raw evidence.
- Do not promote roadmap checkboxes or release-monitor keywords into verified product facts.
- Do not commit, push, publish, or perform external writes unless explicitly requested.
- Keep the booklet complete enough for a seminar while avoiding duplication of the Brief and raw notes.

## Return to the caller

Report:

- files created or refreshed;
- shared questions and key conclusions;
- dynamic, unverified, or blocked claims;
- downstream artifacts marked `needs-refresh`;
- validation commands and results;
- whether commit/push was intentionally not performed.
