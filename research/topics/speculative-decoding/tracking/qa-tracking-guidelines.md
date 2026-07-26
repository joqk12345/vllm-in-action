# QA Tracking Best Practices

Owner:
Purpose: 规范从访谈、直播、字幕和讨论中捕获 QA，并将其转化为可验证 claim、实验或章节素材。
Status: active
Applies to: `research/topics/speculative-decoding/tracking/*.yml`
Evidence grade: process guidance
Verified date: 2026-07-25
Assumptions: QA tracker 是“线索 → 证据 → claim → 正文”的中间层，不是正文事实源。
Open questions: 是否需要后续纳入 `scripts/validate_kb.py` 自动校验。
Handoff: topic booklet、claim spine、benchmark/experiment records、chapter handoff

## 1. 核心原则

1. **一条 QA 只追踪一个可验证问题。** 如果一个问题同时涉及支持状态、性能数字和兼容性，应拆成多条。
2. **区分现场回答与项目结论。** `speaker_answer` 只是线索；`project_conclusion` 必须由源码、测试、release 文档、论文或本仓实验支撑。
3. **状态反映证据进度。** 不用“感觉差不多”推进状态；只有证据满足条件才能进入 `verified` 或 `answered`。
4. **每条都要有下一步。** `next_action` 不能写“继续关注”，必须指向具体 URL、源码路径、实验或决策。
5. **版本敏感问题必须固定版本。** 涉及 vLLM/speculators 支持状态、默认值、配置和性能时，结论必须绑定 release/tag/commit 或实验环境。

## 2. 推荐字段

```yaml
- id: QA-dspark-talk-012
  time: "00:43:36"
  category: dspark-mechanism
  question: "vLLM 当前 release 是否支持 D-Spark confidence head inference？"
  speaker_answer: "分享现场说法。"
  project_conclusion: ""
  status: needs-source
  priority: high
  evidence_grade: D
  verification_type: source+experiment
  review_cadence: per-vllm-release
  blocking: true
  needs_verification:
    - "核查 vLLM release tag 对应源码、测试和文档。"
  upstream_refs: []
  related_claims: []
  impacts:
    chapters: []
    claims: []
    experiments: []
  risk_if_wrong: "可能错误描述 D-Spark 生产可用性。"
  done_criteria:
    - "找到固定 vLLM/speculators 版本或 commit。"
    - "确认 Markov head 与 confidence head 的推理支持状态。"
    - "写入 claims.yml 或标记 wont-track。"
  owner: ""
  last_checked: "2026-07-25"
  next_action: "检查 vLLM speculative decoding docs、tests 和相关 PR。"
```

## 3. 状态与进入条件

| 状态 | 使用条件 |
|---|---|
| `captured` | 已从字幕/讨论捕获，但尚未判断是否值得追踪。 |
| `needs-source` | 值得追踪，但还缺上游源码、测试、文档、论文或实验。 |
| `verifying` | 正在核查一手来源或运行实验。 |
| `verified` | 已有足够证据，但尚未整理成稳定项目结论。 |
| `answered` | 已形成项目结论，并已写入 claim、来源卡片、实验记录或章节素材。 |
| `stale` | 上游版本变化可能让旧结论失效。 |
| `wont-track` | 非技术、低价值、无法验证或无章节用途。 |

推荐流转：

```text
captured → needs-source → verifying → verified → answered
                         ↘ stale
                         ↘ wont-track
```

## 4. 优先级 criteria

| priority | Criteria |
|---|---|
| `high` | 影响正文结论、生产建议、性能数字、版本边界、用户配置或章节 ready 状态。 |
| `medium` | 影响研究理解或后续实验设计，但短期不直接进入正文。 |
| `low` | 背景信息、社区动态、可选扩展。 |
| `none` | 不追踪，通常配合 `wont-track`。 |

优先追踪的问题类型：

- 影响版本边界：例如某功能从哪个 vLLM/speculators 版本开始支持。
- 影响生产建议：例如高并发时是否应关闭 speculative decoding。
- 影响性能数字：例如 3–5 倍加速的模型、硬件、负载和测量方法。
- 影响复现实验：例如训练数据量、max model length、draft length 对接受率的影响。
- 影响 claim 风险：例如 D-Spark Markov head 和 confidence head 的贡献拆分。

不建议追踪：

- 纯闲聊或会务问题；
- 无法验证的主观评价；
- 没有章节用途的问题；
- 没有明确上游证据路径的问题。

## 5. Verification type

| verification_type | 含义 |
|---|---|
| `source` | 通过源码、测试、release note、官方文档、论文或 PR 验证。 |
| `experiment` | 必须通过本仓实验验证。 |
| `source+experiment` | 既需要上游证据，也需要本仓复现或 benchmark。 |
| `discussion` | 只能作为访谈/讨论线索，不能单独支撑正文。 |

## 6. Review cadence

| review_cadence | 适用场景 |
|---|---|
| `per-vllm-release` | vLLM 支持状态、配置、默认值、测试覆盖。 |
| `per-speculators-release` | speculators 训练、转换、checkpoint config、数据流程。 |
| `on-related-pr` | 正在等待某个 PR/branch 合并。 |
| `monthly` | 论文、roadmap、社区模型等中速变化。 |
| `quarterly` | 背景性问题或低优先级调研。 |
| `before-chapter-freeze` | 章节定稿前必须重查。 |

## 7. 关闭 criteria

一条 QA 从 `verified` 进入 `answered`，至少应满足：

1. 有固定版本、release tag、commit、论文版本或实验环境；
2. 有稳定 URL、源码路径、测试路径或本仓实验记录；
3. 明确适用范围：模型、硬件、精度、部署拓扑、负载；
4. 明确限制、反例或失效边界；
5. 已写入以下至少一处：
   - `claims.yml`
   - source ledger
   - benchmark/experiment record
   - topic booklet / chapter handoff
   - 或明确标记为 `wont-track`

## 8. D-Spark 字幕 QA 的高优先级追踪项

当前 `tracking/2026-07-22-dspark-talk-qa.yml` 中建议优先推进：

| ID | 主题 | 原因 |
|---|---|---|
| QA-dspark-talk-004 | RL 集成 | 影响训练/推理闭环和 draft-target 漂移判断。 |
| QA-dspark-talk-006 | 训练数据来源 | 影响可复现训练流程。 |
| QA-dspark-talk-008 | 加速范围 | 影响性能结论，必须实验或固定 benchmark 条件。 |
| QA-dspark-talk-010 | 接受长度 vs speedup | 防止把 acceptance length 误写成端到端 speedup。 |
| QA-dspark-talk-011 | LoRA 兼容 | 影响生产部署建议。 |
| QA-dspark-talk-012 | D-Spark 支持状态 | 版本漂移风险最高，需绑定 vLLM/speculators commit。 |
| QA-dspark-talk-013 | hidden states connector | 影响在线训练架构与可扩展性。 |
| QA-dspark-talk-016 | 数据量 | 影响训练成本和实验设计。 |
| QA-dspark-talk-017 | fine-tuning / conversion | 影响复用已有 drafter 的工程路径。 |
| QA-dspark-talk-020 | long context | 影响 max model length 和长上下文部署边界。 |

## 9. 建议最小维护流程

1. 捕获 QA 后写入 tracker，初始状态为 `captured` 或 `needs-source`。
2. 对 `high` 项补充 `verification_type`、`review_cadence`、`done_criteria`、`risk_if_wrong`。
3. 找到一手来源后填 `upstream_refs`，状态改为 `verifying` 或 `verified`。
4. 若需要本仓实验，建立 benchmark/experiment record，并在 `impacts.experiments` 中绑定。
5. 形成稳定结论后写入 `project_conclusion`，绑定 `related_claims`，状态改为 `answered`。
6. 每次 vLLM/speculators release 后，重查 `review_cadence` 为 `per-vllm-release` 或 `per-speculators-release` 的条目。
