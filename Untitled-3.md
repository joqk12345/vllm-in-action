



[https\://github.com/xiaolai/ai-cli-kickstarter](https://github.com/xiaolai/ai-cli-kickstarter)



> 给完全不懂计算机的人安装第一个 AI CLI，然后由这个 AI 接管后续指导。



只读检查完成，结果很清楚：

- 这是 Apple 芯片的 macOS 15.5，默认 Shell 是 zsh。
- Homebrew 已安装，这是 macOS 上最合适的包管理器，不需要再
  装。
- Node.js、npm、pnpm、Python、Git、jq、wget、tmux 已有；不应
  重复安装。
- 当前缺少：uv（Python 项目/虚拟环境工具）、fd（更好用的文件
  查找）、fzf（交互式搜索）、Shell 提示符工具。
- \~/.zshrc 已存在，后续若要加入配置必须先备份；目前没有动它。

我再做一次只读检查，确认已有的 Shell 提示符、Homebrew 软件包
和 .zshrc 中相关配置，避免重复或冲突。





检查显示你已经有 Oh My Zsh + Powerlevel10k（Shell 提示符），
所以不需要再安装 Starship，避免两套提示符冲突；也已有 GitHub
CLI。\~/.zprofile 里还存在 Homebrew 镜像地址和一个被隐藏的 API
环境变量，我不会改动它们。

推荐的最简补充方案是：

- uv：管理 Python 版本、虚拟环境和依赖，AI 项目最有价值。
- fd：比系统 find 更易用，很多开发工具会调用它。
- fzf：在终端快速搜索文件、历史命令。
- bat：更易读地查看代码和配置。

暂不安装 Docker、额外 Python/Node 版本管理器、Starship 或字
体：你已有 Node/Python，当前提示符已配置；Docker 只有在你明确
使用容器时才需要，字体也应先确认现有终端是否显示正常。

安装这 4 个 Homebrew 工具会联网下载软件，部分步骤可能弹出管理
员密码；不会删除文件，也不会修改配置文件。预计 2–5 分钟。是否
同意安装这 4 个工具？







领域       推荐工具          当前状态      理由
━━━━━━━━━  ━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━
编程       Visual Studio     未安装        免费、生态成熟，
Code                            适合连接 Codex/
Claude Code；官
方提供 Apple 芯
片版本，并持续增
强 Agent 能力。
官方说明
(https\://
code.visualstudi
o.com/)
─────────  ────────────────  ────────────  ──────────────────
写作       Obsidian          已安装        本地 Markdown 笔
记，适合长期知识
库和 AI 辅助写作
─────────  ────────────────  ────────────  ──────────────────
研究       Zotero            未安装        管理论文、PDF、
引用和浏览器收
藏；当前最新版为
Zotero 9。官方下
载 (https\://
[www\.zotero.org/](http://www.zotero.org/)
download/)
─────────  ────────────────  ────────────  ──────────────────
终端       iTerm2 +          已具备        你已有 iTerm2、
Powerlevel10k                   Shell 提示符和核
\+ uv/fd/fzf/                    心命令行工具，不
bat                             再重复安装
─────────  ────────────────  ────────────  ──────────────────
浏览器     Google Chrome     已安装        AI 网站、开发者
工具和扩展兼容性
最好；macOS 15.5
满足要求。官方说
明 (https\://
support.google.c
om/chrome/
answer/16737628?
hl=en)
─────────  ────────────────  ────────────  ──────────────────
AI         Codex CLI +       已安装命令    当前已经有 Codex
Agent      Claude Code +                   CLI、Claude Code
Ollama                          和 Ollama，不需
要重复安装





- 写作：Obsidian
  - 研究：Zotero + Zotero Connector
  - 终端：iTerm2、Powerlevel10k、uv、fd、fzf、bat
  - 浏览器：Chrome
  - AI Agent：Codex CLI、Claude Code、Ollama





