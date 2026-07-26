# 来源清单

Verified date: 2026-07-26

| Source ID | 文件或地址 | 类型 | 等级 | 主要用途 |
|---|---|---|---|---|
| `SRC-glm5-paper-v2` | [`papers/2026-02-24-glm-5-paper-v2.pdf`](papers/2026-02-24-glm-5-paper-v2.pdf) | 作者论文，arXiv v2 | B | GLM-5 的 DSA、MLA、长上下文训练、efficient attention 消融、DP-aware routing 线索 |
| `SRC-efficient-attention-seed-list` | [`notes/seed-papers.txt`](notes/seed-papers.txt) | 人工种子列表 | D | 发现 NSA、MoBA、Lightning Attention 等后续来源；不能支撑正文 |
| `SRC-kimi-linear-paper-v2` | [`papers/2025-11-01-kimi-linear-paper-v2.pdf`](papers/2025-11-01-kimi-linear-paper-v2.pdf) | 作者论文，arXiv v2 | B | Kimi Linear/KDA 架构、3:1 hybrid ratio、KDA kernel/vLLM integration 声明、作者报告 benchmark |
| `SRC-minimax-m1-paper-v1` | [`papers/2025-06-16-minimax-m1-paper-v1.pdf`](papers/2025-06-16-minimax-m1-paper-v1.pdf) | 作者论文，arXiv v1 | B | MiniMax-M1 Lightning Attention、1M context、40K/80K thinking budget、作者报告 benchmark |
| `SRC-minimax-m2-series-paper-v1` | [`papers/2026-05-26-minimax-m2-series-paper-v1.pdf`](papers/2026-05-26-minimax-m2-series-paper-v1.pdf) | 作者论文，arXiv v1 | B | MiniMax-M2 full attention 选择、hybrid/SWA 反例、agentic serving/RL 系统线索 |
| `SRC-gated-deltanet-paper-v3` | [`papers/2024-12-09-gated-delta-networks-paper-v1.pdf`](papers/2024-12-09-gated-delta-networks-paper-v1.pdf) | 作者论文，arXiv v3 / ICLR 2025 | B | Gated DeltaNet/GDN 机制、gated delta rule、chunkwise parallel algorithm、hybrid GDN 架构 |
| `SRC-deltanet-explained-part-ii` | [`articles/2024-12-03-deltanet-explained-part-ii.html`](articles/2024-12-03-deltanet-explained-part-ii.html) | 技术博客 | C | DeltaNet chunkwise/WY 算法背景解释；辅助理解 GDN/KDA |
| `SRC-kimi-linear-repository` | <https://github.com/MoonshotAI/Kimi-Linear/tree/8c1d85eb6b5f8fcefb15758691b0ce50b0827ce3> | 固定 commit 源码/README | A | 模型链接、依赖和 vLLM serve 示例；不能替代 vLLM release 验证 |
| `SRC-kimi-linear-hf-config-2026-07-26` | [`configs/2026-07-26-kimi-linear-48b-a3b-instruct-config.json`](configs/2026-07-26-kimi-linear-48b-a3b-instruct-config.json) | HF model config | A | Kimi Linear Instruct 的 `linear_attn_config`、KDA/MLA 层分布和 state shape 推导 |
| `SRC-qwen3-next-hf-config-2026-07-26` | [`configs/2026-07-26-qwen3-next-80b-a3b-instruct-config.json`](configs/2026-07-26-qwen3-next-80b-a3b-instruct-config.json) | HF model config | A | Qwen3-Next 的 full-attention interval、linear/GDN 参数和 3:1 层分布推导 |
| `SRC-flash-linear-attention-kda` | <https://github.com/fla-org/flash-linear-attention/tree/0a9b9f222e86b9a895c2447767e9b4cce6c8d530/fla/ops/kda> | 固定 commit 源码 | A | KDA chunk/recurrent/gate operator 实现线索 |
| `SRC-vllm-kimi-linear-support-v0-11-1` | <https://github.com/vllm-project/vllm/tree/v0.11.1> | vLLM release tag 源码/文档 | A | 首个已观察到 KimiLinearForCausalLM 支持入口的稳定 tag；Kimi Linear/KDA release 边界 |
| `SRC-vllm-kimi-linear-support-v0-25-1` | <https://github.com/vllm-project/vllm/tree/v0.25.1> | vLLM release tag 源码/文档 | A | 当前应优先验证的 vLLM release 基线；KimiLinearForCausalLM 与 KDA path |
| `SRC-vllm-qwen3-next-gdn-support-v0-25-1` | <https://github.com/vllm-project/vllm/tree/v0.25.1> | vLLM release tag 源码/文档 | A | Qwen3-Next/Qwen3.5 GDN path、QwenGatedDeltaNetAttention、GDN backend 线索 |
| `SRC-vllm-kimi-linear-support-2026-07-26` | <https://github.com/vllm-project/vllm/tree/1240c74c0a47473449cf0c3a9c2d87a1e159f73b> | 固定 commit 源码/文档 | A | 研究阶段核查 vLLM KimiLinearForCausalLM、KDA ops 和 kernel tests；路径已较 v0.25.1 继续重构 |
| `SRC-kimi-linear-yang-songlin-interview` | [`transcripts/2026-kimi-linear-yang-songlin-interview.zh.txt`](transcripts/2026-kimi-linear-yang-songlin-interview.zh.txt) | 中文访谈转写，来源待核对 | D | 发现 Kimi Linear/KDA、hybrid linear attention、sparse vs linear、benchmark 反例和硬件亲和线索 |
| `SRC-qwen-gdn-zhihu-2026` | <https://zhuanlan.zhihu.com/p/2007937984738129405> | 知乎链接，正文未捕获 | D | 用户补充的 Qwen/GDN 线索；当前抓取被 anti-bot shell 阻断，不能支撑 claim |
| `SRC-deepseek-native-sparse-attention` | <https://arxiv.org/pdf/2502.11089> | 待抓取论文 | B? | Native Sparse Attention 算法与训练/硬件边界，待核查 |
| `SRC-kimi-moba` | <https://arxiv.org/pdf/2502.13189> | 待抓取论文 | B? | Mixture of Block Attention 机制与长上下文 benchmark，待核查 |
| `SRC-minimax-lightning-attention` | <https://arxiv.org/pdf/2501.08313> | 待抓取论文 | B? | Lightning Attention / MiniMax-01 长上下文架构，待核查 |

## 文件校验

```text
e20742ff36e08dc361de6973f7f72ad38e107edf8fd92d2a777a8428fc9b8f0e  papers/2026-02-24-glm-5-paper-v2.pdf
e2e23a449fc9bb27e34e783d20b2e6cd0f1ac67d58efdc0479c03c54db956a17  papers/2025-11-01-kimi-linear-paper-v2.pdf
d355a6a41a26b85ca145aec5154650f4d39733c92f54775ae7f5851ecbedf600  papers/2025-06-16-minimax-m1-paper-v1.pdf
4c090a07b73dade56ed3e90f7fdf56a183601c12d2f2d1f81eb46f24cff311fd  papers/2026-05-26-minimax-m2-series-paper-v1.pdf
55f84f2ae9c4e52ff494bfa699499867f5e9e17514994ac71de43888363a5fb9  papers/2024-12-09-gated-delta-networks-paper-v1.pdf
32cc54d6363b43760d018ce6a4708e611706567c1208df160a321a39b5f1d88b  articles/2024-12-03-deltanet-explained-part-ii.html
328e09549432350b25698adb59a360acc4ff75582a769e37f76a615998e2448b  notes/seed-papers.txt
83d9017b7e03f187c3bfe9f9a511131478d3d007d180d2abbf352ef99dcc5048  transcripts/2026-kimi-linear-yang-songlin-interview.zh.txt
a6ac3c2c4b5aa72370f9727f49ffa4432715d20061889acdb37c688be853096e  configs/2026-07-26-kimi-linear-48b-a3b-instruct-config.json
2d483c7cabad7c8704478ed4038fa7e7b2eff840bc00a118eccbe38e2b488303  configs/2026-07-26-qwen3-next-80b-a3b-instruct-config.json
```

## 权利与引用边界

- GLM-5、Kimi Linear、MiniMax-M1/M2、Gated DeltaNet PDF 来自 arXiv，本仓当前只作为内部研究素材；引用正文前需保留标题、作者、arXiv version 和 URL。
- `seed-papers.txt` 只是待办线索，不是来源证据。
- `2026-kimi-linear-yang-songlin-interview.zh.txt` 是访谈转写/口述材料，原始 URL、发布日期和授权尚未核对，只能作为 D 级线索。
- 知乎链接当前未抓取到正文，只能作为 D 级发现线索。
- 论文报告的长上下文质量和效率结果属于作者报告；生产 serving 结论必须通过 vLLM 支持状态和本仓实验验证。
- HF config 当前从 model repository `main` 下载；进入正文或实验记录前应固定 HF revision。
- GitHub source cards 固定到 commit；不要在正文中引用浮动 `main` 或 `latest vllm` 作为永久事实。

## 版本边界

- GLM-5：`arXiv:2602.15763v2`，PDF metadata 日期 2026-02-24。
- Kimi Linear：`arXiv:2510.26692v2`，PDF metadata 日期 2025-11-01。
- MiniMax-M1：`arXiv:2506.13585v1`，PDF metadata 日期 2025-06-16。
- MiniMax-M2：`arXiv:2605.26494v1`，PDF metadata 日期 2026-05-26。
- Gated DeltaNet：`arXiv:2412.06464v3` / ICLR 2025，PDF metadata 日期 2025-03-07；本地文件名保留首次捕获日期。
- Kimi Linear repo：`MoonshotAI/Kimi-Linear@8c1d85eb6b5f8fcefb15758691b0ce50b0827ce3`。
- Flash Linear Attention KDA：`fla-org/flash-linear-attention@0a9b9f222e86b9a895c2447767e9b4cce6c8d530`。
- vLLM Kimi Linear stable release boundary：`v0.11.1` (`439368496db48d8f992ba8c606a0c0b1eebbfa69`) 是当前已观察到的首个包含 `KimiLinearForCausalLM` 支持入口的稳定 tag；`v0.11.1rc5` 是当前已观察到的首个 RC，`v0.11.0` 未观察到该入口。
- vLLM current verification baseline：`v0.25.1` (`752a3a504485790a2e8491cacbb35c137339ad34`) 已观察到 `KimiLinearForCausalLM`、`kimi_gdn_linear_attn.py`、vendored `fla/ops/kda.py` 和 `tests/kernels/test_kda.py`；后续 smoke test/benchmark 应优先基于该 tag。
- vLLM Kimi Linear support snapshot：`vllm-project/vllm@1240c74c0a47473449cf0c3a9c2d87a1e159f73b`，研究阶段使用；路径已较 `v0.25.1` 继续重构。
- NSA/MoBA/MiniMax-01：仅记录 URL，尚未下载、校验或建 source card。