# 投机解码专题正文落点建议

Owner: 未指定
Purpose: 记录投机解码与 DSpark 专题进入正文的候选位置、内容边界和暂缓项
Status: proposal — awaiting decision
Applies to: 当前 `book/toc.yml`、章节 brief 与 2026-07-25 的专题材料
Evidence grade: editorial judgment；技术 claim 仍以 `claims.yml` 为准
Verified date: 2026-07-25
Assumptions: 不为投机解码新增独立章节；维持当前 16 章结构
Open questions: 是否采用本建议，以及各章为投机解码分配多少篇幅
Handoff: 第 9、10、11、12、15 章

## 决策状态

本文件只保存编辑建议，不表示已经批准进入正文。

- 未修改 `book/chapter-briefs/`；
- 未修改 `book/chapters/`；
- 未将论文 benchmark 升级为本书结论；
- 未决定是否把 Mooncake/隐藏状态训练链路纳入正文。

## 建议结论

投机解码的主落点是第 11 章“优化 TTFT 与 ITL”。DSpark 不单独成章，而是作为半自回归 drafter 与负载感知验证的案例。调度、benchmark、吞吐和上线内容分别由第 10、9、12、15 章承接。

| 专题内容                                        | 建议位置   | 正文职责                  |
| ------------------------------------------- | ------ | --------------------- |
| 投机解码循环、lossless 边界、延迟模型                     | 第 11 章 | 建立基本机制和适用条件           |
| DSpark 半自回归 drafter                         | 第 11 章 | 展示 drafter 延迟与接受长度的折中 |
| confidence scheduling、动态验证长度、batch capacity | 第 10 章 | 展示负载如何改变验证预算          |
| 接受长度与端到端加速比的区别                              | 第 9 章  | 作为 benchmark 指标误用的反例  |
| 高并发验证浪费、吞吐 Pareto 前沿                        | 第 12 章 | 连接吞吐、利用率、goodput 与成本  |
| Speculators/vLLM 兼容、启用、canary 和回退           | 第 15 章 | 形成版本化生产采用清单           |
| Mooncake、隐藏状态提取、跨节点训练                       | 暂留专题   | 尚不属于本书 serving 主线     |

## 第 11 章：主叙事

建议新增一节：

```text
投机解码：用额外计算换取更低 ITL

1. Draft → Verify → Accept/Reject
2. “无损”保持的是 target distribution
3. 性能模型：
   L = (T_draft + T_verify) / τ
4. Drafter 的三类取舍
   - 自回归 drafter
   - 并行 drafter
   - 半自回归 drafter
5. DSpark：半自回归生成案例
6. 什么时候投机解码反而更慢
7. 启用前的实验矩阵
```

这一节应围绕诊断和选择，而不是算法排行榜。耐久主体是：

- drafter 必须足够便宜；
- target 必须能从批量验证中获益；
- 接受长度必须足以摊薄 draft、verify、调度和通信成本；
- workload、采样、并发和硬件变化后需要重新测量。

## 第 10 章：验证预算也是调度问题

只承接 DSpark 的系统调度部分：

```text
固定 proposal length
  → 按 token confidence 裁剪
  → 按当前负载分配 verification budget
  → 避免低预期收益 token 占用 batch capacity
```

建议形成的稳定判断：

> 验证更多候选 token 在低负载时可能近乎免费，在高并发时却会挤占其他请求的批处理容量。

DSpark 的 hardware-aware prefix scheduler 是该判断的案例，不应写成所有 vLLM 版本已经具备的默认能力。

## 第 9 章：Benchmark 反例

用本专题说明三个指标不能混写：

```text
acceptance length
  ≠ per-user generation speed
  ≠ aggregate throughput/goodput
```

实验至少应同时记录：

- target model 与 drafter/checkpoint；
- vLLM、Speculators 版本或 commit；
- 硬件、精度和并行配置；
- prompt/output 长度分布、请求域和采样参数；
- 并发、到达模型和 batch 行为；
- `T_draft`、`T_verify`、接受长度、TTFT、ITL、吞吐和 goodput；
- 关闭投机解码的同条件基线。

## 第 12 章：高并发与单位成本

论文中 DeepSeek-V4 的线上结果适合作为“作者报告的生产案例”，用于讨论：

- 接受更多 token 为什么可能降低系统吞吐；
- verification waste 如何消耗批处理容量；
- latency—throughput Pareto frontier；
- 为什么应在 SLO 约束内比较有效吞吐。

这些数字不能直接外推到 vLLM、其他模型或本书目标硬件。进入正文前应优先使用本仓库实验替代外推。

## 第 15 章：生产采用与回退

只纳入版本敏感的操作框架，不提前固化浮动命令：

1. 固定 vLLM、Speculators 和 checkpoint 组合；
2. 验证 config、sampler、模型加载和 fallback；
3. 用代表性 workload 做 canary；
4. 同时观察质量、ITL、吞吐、显存和错误；
5. 收益不成立或兼容性失败时回退普通自回归解码。

## 暂不进入正文

- “DSpark 是当下最强投机解码”；
- 动态 checkpoint 数量；
- 未固定版本的 PPT 命令和配置；
- 将论文 acceptance length 直接解释为 vLLM 加速比；
- DeepSeek-V4 内部结果对其他模型和 serving 栈的直接外推；
- Mooncake、隐藏状态在线提取和跨节点 drafter 训练细节；
- 未清洗字幕中的术语、数字和 Q\&A 判断。

## 若批准后的执行顺序

1. 更新第 9、10、11、12、15 章 brief 的必须包含项和证据缺口；
2. 固定目标 vLLM/Speculators 版本并补来源卡；
3. 设计关闭/启用投机解码的实验矩阵；
4. 形成第 11 章主段落；
5. 将调度、benchmark、吞吐和升级内容拆到对应章节；
6. 技术复核通过后再进入正式正文。
