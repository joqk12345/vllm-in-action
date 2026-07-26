# 投机解码专题阅读路径

Owner:
Purpose: 按共同研究问题组织阅读轮次，指导读者从算法事实、工程状态、QA 线索和实验计划中提取可验证结论。
Status: captured
Applies to: research/topics/speculative-decoding
Evidence grade: B/C/D 混合
Verified date: 2026-07-25
Assumptions: 阅读输出必须回写到 `claims.yml`、`tracking/`、`capability-matrix.yml` 或实验记录。
Open questions: vLLM/Speculators commit 尚未固定。
Handoff: topic booklet、seminar、chapter handoff

## Round 0：建立证据门禁

目标：先理解哪些材料能支撑正文，哪些只能作为线索。

主要材料：

- `AGENTS.md`
- `source/README.md`
- `tracking/qa-tracking-guidelines.md`

提取内容：

- 证据等级；
- release/tag/commit 固定要求；
- QA tracker 状态和关闭条件。

输出：

- 给每个待引用结论标注证据等级和版本缺口。

## Round 1：算法正确性与性能模型

目标：回答“为什么投机解码可以 lossless，以及 acceptance length 为什么不是 speedup”。

主要材料：

- `claims.yml`：SD-C01、SD-C02、SD-C08
- `vocabulary.md`
- `source/papers/2026-07-06-dspark-paper-v1.pdf`

对比材料：

- 后续需补充经典 speculative sampling 原始论文和 vLLM 采样测试。

提取内容：

- target distribution 保持所需假设；
- rejection/correction 的角色；
- `T_draft`、`T_verify`、acceptance length 的关系；
- 低接受率或 drafter 成本过高的反例。

输出：

- 一个最小性能模型；
- 需要 benchmark 采集的指标清单。

## Round 2：DSpark 设计与消融问题

目标：理解 DSpark 的并行 backbone、顺序 head、confidence 和 hardware-aware prefix scheduler 分别解决什么问题。

主要材料：

- `source/papers/2026-07-06-dspark-paper-v1.pdf`
- `claims.yml`：SD-C03、SD-C04、SD-C05

对比材料：

- DFlash、EAGLE-3、MTP、PEEGO 的论文/源码，待补。

提取内容：

- 并行 drafter 的后缀质量问题；
- Markov/RNN head 的额外 latency 与 acceptance 收益；
- confidence 校准和 prefix survival probability；
- 论文 benchmark 的模型、数据、温度、baseline 和指标。

输出：

- DSpark vs DFlash/EAGLE/MTP 能力表；
- 消融实验候选：head 类型、proposal length、confidence 裁剪。

## Round 3：vLLM 与 Speculators 支持状态

目标：把“公开描述支持”拆成 implemented、tested、released、locally tested。

主要材料：

- `claims.yml`：SD-C06、SD-C07
- `tracking/README.md`
- `outputs/booklet/capability-matrix.yml`
- Speculators 上游仓库固定 commit，待选
- vLLM speculative decoding 文档与 release tag，待选

提取内容：

- DSpark Markov head 与 confidence head 支持状态；
- checkpoint config、hidden states 层选择、转换和部署路径；
- vLLM scheduler/model runner/sampler 对 speculation 的限制；
- LoRA、多模态、长上下文、动态 speculation 的测试覆盖。

输出：

- 更新 capability matrix；
- 对 high priority QA 补 `upstream_refs`、`review_cadence` 和 `done_criteria`。

## Round 4：训练数据与 hidden states 链路

目标：回答 drafter 训练如何复现，尤其是数据、target response regeneration、loss mask 和 hidden states 传输。

主要材料：

- `outputs/2026-07-22-dspark-speculative-decoding-talk-qa-analysis.md`
- `tracking/2026-07-22-dspark-talk-qa.yml`：QA-006、013、014、016、017、018、020
- Speculators tutorial/source，待固定 commit

提取内容：

- 支持的数据集和数据格式；
- target response regeneration 是否有脚本支持；
- hidden states 离线写盘 vs 在线传输；
- Mooncake/KVConnector 的传输后端、分片、eviction、容错；
- fine-tuning/from_pretrained/DFlash→DSpark conversion 路径。

输出：

- 训练 pipeline 图或文字步骤；
- 在线 hidden states 训练的 failure drill；
- 数据量 ablation 计划。

## Round 5：生产采用、canary 与 rollback

目标：将研究结论转成生产启用、限流、动态裁剪和回退决策。

主要材料：

- `outputs/booklet/speculative-decoding-topic-booklet.md`：第 9、10、11 节
- `tracking/2026-07-22-dspark-talk-qa.yml`：QA-008、010、011、012、020
- 后续本仓 benchmark records

提取内容：

- 低并发 latency 与高并发 throughput/goodput 的差异；
- compute-bound 时关闭 speculation 的阈值；
- LoRA、长上下文、低接受率、target 更新的 canary；
- fallback 配置和观测信号。

输出：

- 生产决策模板填写结果；
- benchmark completion criteria；
- rollback drill。

## 最小阅读笔记格式

```text
Source:
Question answered:
Claim/proposition:
Evidence grade:
Version/commit:
Applies to:
Does not prove:
Counterexample:
Follow-up action:
Related QA/claim:
```
