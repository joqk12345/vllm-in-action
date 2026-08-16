# 第 16 章 端到端生产 Playbook

<!-- verified: fe1c317157d4478fdc0e02096447e61305b871e9, 2026-08-16 -->

本章把全书压缩成可执行路径。每一阶段都有产物和退出条件。

## 16.1 阶段 A：契约

产物：workload trace/schema、SLO、质量 eval、安全等级、成本上限。按 input/output/prefix/模态/租户分桶，决定交互与批处理是否隔离。退出条件：团队对 goodput 定义一致。

## 16.2 阶段 B：单卡正确基线

固定 vLLM/model/image revision，以 BF16/FP16 或可信精度运行功能矩阵。记录 resolved config、启动显存、单请求 TTFT/ITL、输出质量。退出条件：干净环境可复建，错误可解释。

## 16.3 阶段 C：容量与并行

先估权重和 KV，选择最小可行 TP；跨慢边界优先考虑 PP/DP，MoE 再评 EP，长 context 才评 CP/P-D。验证 collective 与拓扑。退出条件：单 replica 在开放到达测试中有稳定 goodput 曲线。

## 16.4 阶段 D：逐项优化

按瓶颈选择，不按热点列表全开：

- 重复长前缀：APC + prefix-aware routing；
- 长 prefill 干扰：chunk、隔离、PCP/P-D；
- 低并发 decode：graph、量化、spec decode；
- 高并发吞吐：batch/token budget、kernel/compile；
- MoE：EP balance、All-to-All 与 grouped GEMM；
- KV 压力：长度/admission、KV dtype、混合 cache 策略。

每项经过 correctness → micro/engine → serving → cost，保留回退条件。

## 16.5 阶段 E：生产封装

入口增加 TLS/auth、quota、输入上限、SSRF 防护、有界队列与 timeout；readiness 反映模型可服务，断连传播 abort。建立 SLO/cache/scheduler/device dashboard，日志脱敏。预留一个副本/节点故障与升级容量。

## 16.6 阶段 F：上线与运营

shadow 验证协议和质量，canary 观察 SLO/错误/显存/preemption，再分批扩流。发布后运行 soak 和峰值演练。每个 release 重做 impact triage；模型/模板/量化变化走同样流程。

## 16.7 快速决策表

| 现象 | 首查 | 不要先做 |
|---|---|---|
| p99 TTFT 突升 | queue、prompt、prefix、prefill | 随机换 attention backend |
| ITL 周期尖峰 | preemption、graph、collective、GC | 只增 batch |
| OOM | 启动阶段与显存账本 | 只降 max model len |
| 多卡不扩展 | 拓扑、collective、straggler | 继续加 TP |
| APC 无收益 | 命中 token、路由、模板 | 只看 request hit |
| MoE 抖动 | 每 rank expert load/A2A | 只优化 GEMM |

## 16.8 上线清单

- [ ] immutable commit/model/image/config/workload；
- [ ] API、质量、长上下文和目标模型特性通过；
- [ ] SLO 下 goodput、成本和故障冗余已知；
- [ ] admission、timeout、abort、drain 已演练；
- [ ] dashboard/alert/runbook 能定位层级；
- [ ] 安全、隐私、供应链审查完成；
- [ ] canary 与一键回滚可用；
- [ ] 所有非默认优化有证据和 owner。

## 16.9 继续研究源码

遇到新热点，沿五层检查：模型语义 → cache/state → scheduler → backend metadata → kernel；再沿生产链验证 API、distributed、metrics 与 failure。这样面对新的 linear attention、稀疏 MLA、elastic EP 或 KV connector，也能用稳定框架判断，而不是追逐名称。

> **最终原则**：最快的服务不是 benchmark 数字最大的服务，而是在正确性、安全和故障预算内，持续交付最多合格 token 的系统。
