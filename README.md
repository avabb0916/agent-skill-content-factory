# content-factory · 长文内容工厂技能

**简体中文** | [English](README.en.md)

一套**与运行时无关**的长文生产流程：从选题到发布的 10 个阶段、写作硬规范、配图规范、质检清单、发布风险清单。
把它装进你的 Agent（Claude Code / Codex / Cursor / Grok bot / 自建 agent），它就知道该怎么写、怎么查、什么时候该拦住你。

> 不依赖任何平台 SDK，不写死任何本机路径。`scripts/` 里的检查器只用标准库。

## 为什么需要一套"流程技能"

大多数 Agent 写长文的问题是：**写得很顺，但结构会崩**。

- 多写了一个 `#`，读者以为文章结束了
- 用了表格和代码块，发到 X 上被整段丢弃
- 「不是X，是Y」写了九遍，读起来像 AI
- 配图路径写错，草稿里少了两张
- 结尾没有提问，读者看完就走

这些**肉眼检查很容易漏**，但清单一条条过就不会漏。这个技能就是把"该怎么检查"固化下来。

## 内容

| 文件 | 作用 |
|---|---|
| `SKILL.md` | **主入口**：10 阶段流程 + 写作/配图规范 + 质检清单 + 风险清单 |
| `bot-prompt.md` | 一屏可粘贴的紧凑版（给对话式 Agent 用） |
| `scripts/qc_article.py` | 质检自动版（17 条规则，只依赖标准库） |
| `scripts/publish_checklist.py` | 发布风险词检查 |
| `tests/` | unittest 用例（3 个，跑 `python3 -m unittest discover -s tests`） |

> 脚本只依赖标准库，Python 3.10+ 即可（CI 覆盖 3.10/3.11/3.12）。
| `examples/` | 一篇合格示例 + 示例图 |

## 怎么用

### 方式一：装成 Skill

支持 Skills 的 Agent（Claude Code、Codex、DSH 等）：把整个目录放进 skills 目录，入口是 `SKILL.md`。

### 方式二：粘成提示词

任意对话式 Agent（Grok bot、ChatGPT、网页版）：

```
把 bot-prompt.md 全文粘进系统提示词或首条消息
```

之后你只需要说「写一篇关于 X 的长文」，它就会按这套流程走：先给 takeaway 和大纲，确认后出全文，最后给质检结果。

### 方式三：只当清单用

不装任何东西，直接把 `SKILL.md` 的第 2 节（质检清单）复制到你的写作笔记里，每次发稿前过一遍。

### 方式四：跑脚本

```bash
python3 scripts/qc_article.py article.md
python3 scripts/publish_checklist.py article.md
python3 -m unittest discover -s tests
```

退出码：`0` 通过 / `1` 有 error / `2` 执行失败。

## 规则速览

| 类别 | 检查项 | 级别 |
|---|---|---|
| 结构 | 必须有标题、只允许 1 个 H1、H2 ≥5、**不允许 H3** | error/warn |
| 平台 | 不允许表格、代码块（会被丢弃） | warn |
| 配图 | 5–9 张、文件必须存在、封面 5:2 | error/warn |
| 写作 | 「不是X，是Y」≤3、每段 ≤220 字、结尾有提问 | warn |
| 合规 | 内部黑话、绝对化（error）；敏感词面、效果数字（warn） | error/warn |

## 配套工具

| 项目 | 作用 |
|---|---|
| [x-article-factory](https://github.com/avabb0916/x-article-factory) | 同一套规则的 JS 实现 + 本地配图生成（`xaf check`） |
| [x-md-publisher](https://github.com/avabb0916/x-md-publisher) | 把 Markdown 发成 X 文章草稿（`xpub`） |
| [x-article-template](https://github.com/avabb0916/x-article-template) | 开箱即用的内容仓库模板（含 CI 检查） |

串起来：

```bash
xaf check article.md && xpub article.md
```

## 设计原则

1. **清单优先于脚本** —— 没有脚本也能照做，脚本只是把检查变成断言
2. **每条规则都有事故来源** —— 不是凭空设计的规范
3. **运行时无关** —— 不绑定平台、不写死路径

## License

MIT
