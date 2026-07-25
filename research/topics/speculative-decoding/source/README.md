# 来源清单

Verified date: 2026-07-25

| Source ID | 文件或地址 | 类型 | 等级 | 主要用途 |
|---|---|---|---|---|
| `SRC-dspark-paper-v1` | [`papers/2026-07-06-dspark-paper-v1.pdf`](papers/2026-07-06-dspark-paper-v1.pdf) | 作者论文，arXiv v1 | B | DSpark 架构、训练目标、实验设置、作者报告的结果与限制 |
| `SRC-dspark-talk-2026-07-22` | [`talks/2026-07-22-dspark-speculative-decoding-talk.pptx`](talks/2026-07-22-dspark-speculative-decoding-talk.pptx) | 公开演讲幻灯片 | C | Speculators、vLLM 和训练/部署流程的研究线索 |
| `SRC-dspark-talk-transcript-2026-07-22` | [`transcripts/2026-07-22-dspark-speculative-decoding-talk.zh.srt`](transcripts/2026-07-22-dspark-speculative-decoding-talk.zh.srt) | 未清洗 ASR 字幕 | D | 发现术语、Q&A 和待核对问题 |
| `SRC-speculators-main` | <https://github.com/vllm-project/speculators> | 上游仓库浮动 `main` | B | 发现当前算法、训练和 vLLM 集成能力；进入正文前必须固定 commit |
| `SRC-vllm-spec-decode` | <https://docs.vllm.ai/en/latest/features/spec_decode/> | vLLM 官方浮动文档 | B | 发现当前 speculative decoding 配置和限制；进入正文前固定 release |

## 文件校验

```text
522036b0cc16ad4678bd7c278dd0a0ab4da31170af7b97c2041067cc09a8289a  papers/2026-07-06-dspark-paper-v1.pdf
32f0eff81a7075b7f8a51d514fc75d2e3982b6dc761dcc4d9994005760ce08e7  talks/2026-07-22-dspark-speculative-decoding-talk.pptx
073754f3f33438cae60f8676e2f9f386993889695738b432af372d470844d923  transcripts/2026-07-22-dspark-speculative-decoding-talk.zh.srt
```

## 权利与引用边界

- DSpark arXiv v1 页面标注为 CC BY 4.0；引用时保留作者、标题、版本和原始地址。
- Speculators 源码采用 Apache-2.0，但该许可不自动覆盖演讲 PPT 和字幕。
- PPT 与字幕的再分发授权状态尚未核对；当前只作为仓库内部研究素材，公开发布前必须确认权利状态。
- 字幕存在 `vLLM`、`DFlash`、`DSpark`、`EAGLE` 等术语的 ASR 错误，不得直接引用为事实。

## 版本边界

- 论文：`arXiv:2607.05147v1`，提交于 2026-07-06。
- PPT：标题页日期 2026-07-22。
- Speculators/vLLM：当前只记录核对日期 2026-07-25；尚未固定 commit 或 release。
