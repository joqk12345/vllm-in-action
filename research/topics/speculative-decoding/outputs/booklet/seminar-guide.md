# 投机解码专题研讨指南

Owner:
Purpose: 支持 60–90 分钟研讨，围绕 DSpark、vLLM/speculators 支持状态和生产采用决策形成可执行结论。
Status: captured
Applies to: research/topics/speculative-decoding
Evidence grade: B/C/D 混合；研讨中不得把 D 级 ASR QA 当作事实。
Verified date: 2026-07-25
Assumptions: 参与者已读 `claims.yml`、小册子执行摘要和 QA tracker 高优先级条目。
Open questions: 是否已有固定 vLLM/speculators commit 与本仓 benchmark。
Handoff: 研讨结论应回写 `claims.yml`、`tracking/` 和实验计划。

## 1. 目标与非目标

### 目标

- 对齐投机解码的正确性、性能模型和生产边界。
- 判断 DSpark 哪些 claim 可进入章节研究，哪些只能保留为线索。
- 将 QA tracker 中 high priority 项转成源码核查、capability matrix 更新或实验任务。
- 明确下一轮 benchmark 的模型、硬件、指标和完成条件。

### 非目标

- 不决定正式章节正文。
- 不把论文或演讲中的数字直接当作生产建议。
- 不讨论与 vLLM/speculators 无关的扩散式语言模型细节，除非影响反例。

## 2. 参与角色

| 角色 | 责任 |
|---|---|
| Facilitator | 控制议程，确保问题驱动而非逐页复述。 |
| Algorithm reviewer | 检查 lossless 条件、DSpark 设计和反例。 |
| vLLM implementation reviewer | 核查 vLLM release、测试、配置和 scheduler/model runner 影响。 |
| Training pipeline reviewer | 核查 speculators、hidden states 抽取、数据和 checkpoint 转换。 |
| Benchmark owner | 定义实验矩阵、指标和原始结果保存位置。 |
| Red team | 专门提出错误泛化、低接受率反例和生产失败路径。 |

## 3. 会前必读

- `outputs/booklet/speculative-decoding-topic-booklet.md`：第 2、3、8、9、10、11 节。
- `claims.yml`：SD-C01 至 SD-C08。
- `tracking/2026-07-22-dspark-talk-qa.yml`：priority 为 high 的条目。
- `tracking/qa-tracking-guidelines.md`：状态、优先级和关闭 criteria。
- `source/README.md`：来源等级与权利边界。

## 4. 90 分钟议程

| 时间 | 主题 | 输出 |
|---|---|---|
| 0–10 分钟 | 目标、证据等级和禁止泛化 | 共同接受的证据门禁 |
| 10–25 分钟 | Q1：lossless 条件与验证规则 | 需要补充的经典来源/测试 |
| 25–40 分钟 | Q2：acceptance length 到 speedup 的性能模型 | benchmark 必须记录的指标 |
| 40–55 分钟 | Q3：DSpark 设计与 DFlash/EAGLE/MTP 对比 | 可接受 claim 与待验证假设 |
| 55–70 分钟 | Q4：vLLM/speculators 支持状态 | capability matrix 更新项 |
| 70–82 分钟 | Q5/Q6：生产决策、训练数据和 hidden states 链路 | canary/rollback/实验任务 |
| 82–90 分钟 | 决策记录与 owner 分配 | action list 与 review date |

60 分钟压缩版：合并 Q1/Q2，跳过低优先级 QA，仅处理 QA-004、006、008、010、011、012、013、016、017、020。

## 5. 核心研讨问题

1. 哪些投机解码实现可以宣称保持 target distribution？证据在哪里？
2. 哪些指标可以证明 production speedup？acceptance length 何时会误导？
3. DSpark 的 Markov head、confidence head 和 hardware-aware prefix scheduler 各自解决什么问题？
4. 当前目标 vLLM/speculators 版本中，哪些能力是 roadmap、哪些已 release、哪些本地测试通过？
5. 高并发 compute-bound、低接受率、LoRA、长上下文和 target 权重更新分别如何触发回退？
6. 训练 drafter 时，数据、response regeneration、loss mask 和 hidden states 链路如何复现？

## 6. Red-team questions

- 如果 acceptance length 提高但 ITL 变差，哪个指标暴露问题？
- 如果 target 开了 LoRA，drafter 没更新，输出分布和接受率会发生什么？
- 如果 confidence 失准，动态裁剪会不会拒绝本应验证的高价值前缀？
- 如果 vLLM README 说支持，但目标 release 测试没有覆盖，能否进入正文？
- 如果在线 hidden states producer 掉线，consumer 如何处理 backlog、eviction 和训练一致性？
- 如果 workload 从短对话切到长上下文数学推理，原 benchmark 是否仍有效？

## 7. 决策/action record

```text
Decision:
Accepted claims:
Claims blocked:
Target vLLM release/commit:
Target speculators commit:
Benchmark owner:
Source verification owner:
Capability matrix changes:
New experiments:
Rollback/canary requirement:
Next review date:
```

## 8. 完成 checklist

- [ ] 每个 accepted claim 绑定 Source ID、版本或 commit。
- [ ] 每个 high priority QA 有 owner、next_action 和 done_criteria。
- [ ] capability matrix 已更新 roadmap/release/local-test 三类状态。
- [ ] benchmark 任务记录模型、硬件、精度、并发、请求分布和指标。
- [ ] 低接受率、compute-bound、LoRA、长上下文至少各有一个反例或测试。
- [ ] 需要刷新的 handoff、brief、slides 或 figures 已标记 `needs-refresh`。
