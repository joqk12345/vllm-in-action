# 附录 B：八个递进实验

所有实验先填写 `templates/experiment.md`，不要预填结果。

## Lab 1：请求生命周期

单请求流式生成，记录客户端 TTFT/ITL、server metrics 和进程日志，画出 API—EngineCore—worker 时序。目标是统一时间定义。

## Lab 2：分页缓存容量

固定模型与输出，扫描 input length/concurrency；记录启动 blocks、KV usage、preemption 和 goodput。用第 4 章公式估算，再解释误差。

## Lab 3：连续批处理前沿

扫描 `max_num_seqs` 与 token budget，分别回放短聊天和长短混合 trace。画 TTFT/ITL/goodput Pareto 前沿。

## Lab 4：前缀缓存

比较无共享、90% 共享、共享但 template 有微差三组 prompt；报告命中 token 而非仅 request hit，验证路由局部性。

## Lab 5：注意力与 graph

对目标平台比较实际选择的 backend 与 eager/graph 路径；分 prefill/decode shape，保留 profiler timeline、显存和 correctness。

## Lab 6：并行拓扑

在同一节点扫 TP，跨节点比较 TP/PP；先跑 collective benchmark。报告每 rank timeline 和扩展效率，找出互联边界。

## Lab 7：量化与推测解码

以 BF16 为质量/性能基线，分别加入 quant 和 speculative decoding；在低并发、高并发及两个任务上报告 acceptance、质量、显存和 goodput。

## Lab 8：生产故障演练

开放到达压到 SLO 边界，依次注入慢客户端、worker kill、存储延迟和突发长 prompt。验证 admission、abort、drain、告警、回滚与恢复时间。

## 实验完成标准

每个 Lab 必须包含 immutable revisions、完整命令、workload hash、warm-up、至少三次重复、逐请求原始数据、失败样本、机制证据、适用边界和回退线。没有 GPU 的环境可完成实验设计与数据 schema，但不得声称性能结果。