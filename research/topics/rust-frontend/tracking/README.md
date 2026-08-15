# Rust Frontend 持续跟踪

Owner: release tracker
Purpose: 把 Issue #44280 的能力变化与 vLLM release 变化持续转成可复核的研究任务
Status: active
Applies to: vLLM Rust Frontend，研究阶段跟踪 `main`，正文结论固定到 release tag/commit
Evidence grade: discovery only；接受结论时回到 vLLM 上游 A/B 级证据
Verified date: 2026-08-15
Assumptions: Version Monitor 负责 release intelligence，不负责证明 Issue 条目已经进入 release
Open questions: 第一个满足本书最小生产就绪门槛的 release
Handoff: 第 3、6、9、13、14、15 章

## 双信号模型

| 信号 | 负责发现 | 不能单独证明 |
|---|---|---|
| [Issue #44280](https://github.com/vllm-project/vllm/issues/44280) | roadmap 文本、checkbox、评论和关联工作发生变化 | 某项能力已进入稳定 release |
| [vllm-version-monitor](https://github.com/joqk12345/vllm-version-monitor) | 新 release、release note 分类和报告构建状态 | Rust Frontend 在该版本中的真实契约与行为 |
| vLLM release/tag/commit/test | 最终版本边界与实现证据 | 本仓库目标 workload 已验证通过 |
| 本仓库 capability test/experiment | 目标模型和部署条件下的可用性 | 其他模型、硬件和拓扑同样成立 |

## 自动漂移检查

从仓库根目录执行：

```bash
python3 scripts/check_rust_frontend_tracking.py
```

脚本比较：

- Issue 状态、正文 SHA-256、评论数和 checklist 数量；
- vLLM 官方最新 release；
- Version Monitor 已提交 manifest 的最新 stable 与构建提交；
- Version Monitor 最近一次成功工作流，仅用于确认发现管线仍在运行。

无变化返回 `0`，网络或数据错误返回 `1`，发现漂移返回 `2`。定时 CI 因漂移失败是一种人工复核提醒，不代表上游回归。

## 人工复核协议

检测到变化后按以下顺序处理：

1. 阅读 Issue diff 和新评论，提取新增、完成、撤销或重新设计的条目。
2. 打开关联 PR，记录 PR URL、merge commit、测试和目标分支。
3. 检查 Version Monitor 的新 release 报告，定位可能相关的 release note。
4. 回到对应 vLLM tag，核对源码、CLI、测试和文档；roadmap checkbox 不作为发布证明。
5. 先更新 `outputs/booklet/capability-matrix.yml`，再更新 `feature-parity-roadmap.md`、来源卡和受影响 claim；需要时创建 release impact。
6. 检查小册子动态附录、Brief、图和 PPT，将过时产物标为 `needs-refresh`，重新生成后再恢复为 current。
7. 完成人工复核后接受新基线：

```bash
python3 scripts/check_rust_frontend_tracking.py --accept
```

`--accept` 只表示“这次上游状态已完成分诊”，不表示所有新能力已验证或可进入正文。

## 更新日志规则

每次接受基线时，在 [`change-log.md`](change-log.md) 追加一条记录，至少包含：

- 捕获日期和上游 `updated_at`；
- checkbox 或状态变化；
- 关联 PR、merge commit 和首个包含它的 release；
- 受影响的 RF claim、章节和输出；
- 结论状态：`observed`、`merged`、`released`、`tested` 或 `integrated`。
