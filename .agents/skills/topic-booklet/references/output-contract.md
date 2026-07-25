# Topic booklet output contract

## Directory

```text
research/topics/<topic>/outputs/booklet/
├── README.md
├── <topic>-topic-booklet.md
├── seminar-guide.md
├── reading-list.md
└── capability-matrix.yml
```

## `README.md`

Explain:

- who uses the directory;
- the responsibility of each file;
- stable body versus dynamic appendix;
- refresh order;
- that roadmap state does not prove release or local validation.

## `<topic>-topic-booklet.md`

Include frontmatter:

```yaml
title:
subtitle: "主题研究小册子"
status:
edition:
created:
verified:
topic:
applies_to:
source_ids: []
chapters: []
```

Include project metadata:

```text
Owner:
Purpose:
Status:
Applies to:
Evidence grade:
Verified date:
Assumptions:
Open questions:
Handoff:
```

Required sections:

1. How to use the booklet
2. Executive summary
3. Shared research questions
4. Minimal concept system
5. System or architecture model
6. Cross-source claims
7. Source correction map
8. Disagreements, counterexamples, and open questions
9. Tests and experiments
10. Production decision, canary, and rollback
11. Layered conclusions
12. Dynamic appendix
13. Seminar decision template

Link reusable topic figures instead of duplicating them.

## `seminar-guide.md`

Support a 60–90 minute seminar:

- objective and non-objective;
- participants and roles;
- mandatory and role-specific pre-reading;
- timed agenda;
- 3–7 core questions;
- red-team questions;
- decision/action record;
- completion checklist with owners and next review date.

## `reading-list.md`

Organize by research question or reading round:

- state the goal of each round;
- identify primary and comparison sources;
- tell the reader what to extract;
- specify the output produced by that round;
- include a minimal note format.

Do not make this a bare URL bibliography.

## `capability-matrix.yml`

Required top-level data:

```yaml
schema_version:
topic:
scope:
as_of:
target_release:
policy:
statuses:
capabilities:
```

Each representative capability should include:

```yaml
- id:
  layer:
  capability:
  roadmap_status:
  release_status:
  local_test_status:
  required_for: []
  chapters: []
  source_ids: []
```

Use layers such as `endpoint`, `parameter-model`, and `operations`. Add upstream timestamps or issue URLs for active roadmap topics.

## Deliverables integration

Add one deliverable:

```yaml
- id: <topic>-topic-booklet
  type: topic-booklet
  status: complete
  research_status: captured
  files:
    - booklet/README.md
    - booklet/<topic>-topic-booklet.md
    - booklet/seminar-guide.md
    - booklet/reading-list.md
    - booklet/capability-matrix.yml
```

Use `needs-refresh` plus `stale_reason` when the files exist but dynamic research has moved.
