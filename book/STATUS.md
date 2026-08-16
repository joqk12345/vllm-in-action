# 书籍生产状态

**最后更新：** 2026-08-16

**当前阶段：** 全书 alpha，可构建 book 与 website

**代码基线：** vLLM `fe1c317157d4478fdc0e02096447e61305b871e9`

## 已完成

- 16 章连续正文，覆盖基础心智模型、服务、KV/混合注意力、分布式、调度、热点注意力、算子/编译与生产运营；
- 源码研究地图、八个递进实验、扩展术语表与代码锚点；
- 每章固定 commit/日期标记，本地源码快照 A 级来源卡；
- 零依赖静态网站、全文搜索、响应式导航与单文件 Markdown book；
- 自动检查 16 章数量、版本标记、最低内容规模和网站产物。

## 里程碑

| 里程碑 | 状态 | 说明 |
|---|---|---|
| M0 知识库骨架 | complete | 规则、spine、模板、validator |
| M1 源码证据基线 | complete | 当前 commit 的关键代码/设计锚点 |
| M2 全书 alpha | complete | 16 章正文与附录均可阅读 |
| M3 Book/Website | complete | `npm run build` 生成静态站与合订本 |
| M4 硬件实验集 | pending | 需在目标 GPU/模型执行附录实验 |
| M5 技术审校版 | pending | 人工逐行审阅、模型 eval、冷读与许可证 |

## 章节状态

| Part | 章节 | 状态 | 后续审校重点 |
|---|---|---|---|
| I | 01–04 | draft | 图示、混合 cache 跨版本核对 |
| II | 05–08 | draft | 多平台与多节点实测 |
| III | 09–12 | draft | GPU profiler 数据与模型 eval |
| IV | 13–16 | draft | 事故案例与安全审阅 |

Alpha 表示内容与出版链端到端完整，不表示所有硬件性能结论已经复现。未执行的实验不得升级为性能事实。章节状态仍按 `brief → researching → draft → review → ready` 推进。