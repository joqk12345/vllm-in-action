# vLLM Rust Frontend：架构与生产成熟度

目标：15–20 页、面向推理/平台工程师的决策型演示。

1. 封面 — 一条 Rust 路径，不是一套新 Engine
2. 结论先行 — 架构价值已清晰，生产替代仍需 capability contract
3. 为什么现在 — GPU 更快后，frontend ceiling 被放大
4. 改什么 / 不改什么 — frontend 与 engine 边界
5. 请求生命周期 — 从 HTTP/SSE 到 ZMQ/MessagePack
6. Workspace 分层 — 五层与每层变化落点
7. Stream-native — 一条增量路径支撑两种响应
8. Parser 难点 — chunk boundary 与 safe text
9. 接入方式 — Python-supervised drop-in 与待核验独立入口
10. Benchmark 设计 — 刻意构造 frontend-bound ceiling
11. Decode 结果 — 吞吐提升有限，TTFT 差异显著
12. Preprocess-hot 结果 — 单 Rust 接近/超过 32 Python 进程
13. 不可外推 — 结果不覆盖 GPU-bound 与功能成熟度
14. Feature parity — endpoint / parameter / operations 三层矩阵
15. Production gates — baseline、contract、ops、performance、canary
16. Rollout / rollback — model+endpoint allowlist 与触发器
17. 书稿 handoff — 第 3、6、9、14、15 章
18. 下一步 — 固定 release、建矩阵、做双 workload 复现

证据主线：RF-C01 → RF-C02/03/04 → RF-C06 → RF-C07/08。

不进入演示的 claim：RF-C09 只在 speaker notes 作为未来研究问题，不作为当前能力。
