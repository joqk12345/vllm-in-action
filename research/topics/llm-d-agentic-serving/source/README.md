# 来源清单

Verified date: 2026-07-26

| Source ID | 文件或地址 | 类型 | 等级 | 主要用途 |
|---|---|---|---|---|
| `SRC-vllm-office-hours-53-llm-d` | [`talks/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.pdf`](talks/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.pdf) | vLLM Office Hours 幻灯片 | C | 发现 llm-d、agentic workloads、prefix routing、KV tiering、PD、Wide EP 和 benchmark 线索 |
| `SRC-vllm-office-hours-53-llm-d-transcript` | [`transcripts/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.en.srt`](transcripts/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.en.srt) | YouTube 自动字幕 | D | 抽取 QA、术语和待核查问题 |
| `SRC-llm-d-repository` | <https://github.com/llm-d/llm-d> | 上游仓库，待核查 | B | 后续固定 commit 后验证 router、EPP、deployment 示例和文档 |
| `SRC-vllm-repository` | <https://github.com/vllm-project/vllm> | 上游仓库，待核查 | A/B | 后续固定 release/commit 后验证 PD、KV connector、Wide EP、DP attention 与测试 |
| `SRC-inferencex-agentx` | <https://github.com/SemiAnalysisAI/InferenceX> | benchmark 项目，待核查 | B/C | 后续核查 AgentX/InferenceX trace、配置和提交结果 |

## 文件校验

```text
a9d10a24c6ed02be4f38f830ab60dfe1e94c3f9046ced068a79cfb4b9da2e6c9  talks/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.pdf
4effdbcde7e9247263c1bdcd4463619193560e888eeb744bbe746210f72168ca  transcripts/2026-07-09-vllm-office-hours-53-llm-d-wide-ep.en.srt
```

## 权利与引用边界

- PDF 与字幕来自公开 Office Hours 资料，但再分发授权状态尚未核对；当前只作为仓库内部研究素材。
- 自动字幕存在大量识别错误，例如 `VLM`/`BLM` 应核对为 `vLLM`，`LMD`/`LLMD` 应核对为 `llm-d`。
- 演讲中的性能和成本数字只可作为 C/D 级线索，不能直接支撑正文。
- 进入正文前必须回查 llm-d/vLLM 上游 release/tag/commit、源码、测试、PR、官方文档或本仓实验。

## 版本边界

- Office Hours：#53，日期 2026-07-09。
- llm-d/vLLM：尚未固定 commit 或 release。
- InferenceX/AgentX：尚未固定 commit、trace 和 benchmark 配置。