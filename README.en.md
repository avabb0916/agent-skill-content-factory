# content-factory · a runtime-agnostic long-form writing skill

[简体中文](README.md) | **English**

A complete long-form production workflow for agents: 10 stages from topic to publishing, hard writing rules, figure rules, a QA checklist and a publish-risk checklist.
Drop it into your agent (Claude Code, Codex, Cursor, Grok bot, custom agents) and it knows how to write, how to check, and when to stop you.

> No platform SDK, no hard-coded local paths. The scripts under `scripts/` use the standard library only.

## Why a "process skill"

Agents write smoothly but their structure breaks:

- an extra `#` makes readers think the article ended
- tables and code fences get dropped on X
- “not X, but Y” nine times reads like AI
- a wrong image path silently drops two figures
- no closing question, so readers leave

These are easy to miss by eye and impossible to miss with a checklist.

## What's inside

| File | Purpose |
|---|---|
| `SKILL.md` | **Main entry**: 10 stages + writing/figure rules + QA checklist + risk checklist |
| `bot-prompt.md` | One-screen compact version for chat agents |
| `scripts/qc_article.py` | Automated QA (17 rules, stdlib only) |
| `scripts/publish_checklist.py` | Publish-risk word scan |
| `tests/` | 3 unittest cases |

> Scripts use the standard library only; Python 3.10+ (CI covers 3.10/3.11/3.12).
| `examples/` | A passing sample article and images |

## Usage

**As a skill** — put the directory into your agent's skills folder; entry point is `SKILL.md`.

**As a prompt** — paste `bot-prompt.md` into the system prompt / first message of any chat agent.

**As a checklist** — copy section 2 of `SKILL.md` into your notes and run through it before publishing.

**As scripts**

```bash
python3 scripts/qc_article.py article.md
python3 scripts/publish_checklist.py article.md
python3 -m unittest discover -s tests
```

Exit codes: `0` pass / `1` has errors / `2` execution failure.

## Companion tools

- [x-article-factory](https://github.com/avabb0916/x-article-factory) — the same rules in JS, plus local figure generation (`xaf check`)
- [x-md-publisher](https://github.com/avabb0916/x-md-publisher) — Markdown → X Article drafts (`xpub`)
- [x-article-template](https://github.com/avabb0916/x-article-template) — ready-to-use content repo template with CI checks

## License

MIT
