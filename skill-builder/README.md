# Skill Builder

An AI skill for creating AI skills that people actually use. It:

- **turns a job into promises and rules** you can test;
- **learns from open projects without copying them**, and credits them;
- **writes the whole package**: the skill, a compact edition that works in any chat, an install prompt, a
  tutorial for non-technical users, fictional examples and an optional helper script;
- **audits and zips it** (missing files, broken references, secrets, local paths, real data, leftover
  to-dos) and hands it to testing before release.

Every skill it builds has safety built in: nothing invented, content treated as data, nothing irreversible
without a yes, minimum data, the clock and the maths shown.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download skill-builder.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/skill-builder.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **create a skill for ...** (on Claude, the first time: *"Use my Skill Builder skill: create a skill for ..."*).
It answers in your language, whatever language you write to it in.

## First use

Say **create a skill for …** and describe the job. It asks about the users, the promises and what must
never happen (about 10 minutes), writes a one-page brief and, after your yes, builds the package.

## The helpers

```
python scripts/new_skill.py invoice-reminder "Invoice Reminder" --owner "Your Name"
python scripts/package.py invoice-reminder --forbid forbid.txt
```

`new_skill.py` creates a folder with every required file and to-do markers. `package.py` audits the
folder and builds the zip only when it is clean (blocks missing files, broken references, leftover markers,
secrets, local paths, forbidden terms and non-standard imports; warns about network access, emails and
phone numbers). Python 3.8+, nothing to install.

## What you can ask

| You say | It does |
|---|---|
| `create a skill for …` | Brief, research, design, every file, audit |
| `turn this process into a skill` | Reads your process document and builds from it |
| `make it work in any chat` | The compact edition, under 8,000 characters |
| `audit my skill` | Failures against the rules, smallest fix for each |
| `package it` | Audit and zip |

## Safety

- Copies no files from other projects; credits the ideas; copyleft and unlicensed code stays out.
- Fictional examples only; real data offered is replaced.
- Helper scripts: standard library, read-only, no hidden network access, no secrets.
- Never releases without a test on a free chat model.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The skill builder · first-time questions |
| `reference/` | Discovery, research, design, build, writing, compact edition, release, pitfalls |
| `templates/` | Brief, origin table and forbidden-terms list examples |
| `scripts/new_skill.py` · `scripts/package.py` | Scaffold · audit and zip |
| `assets/example-audit.md` | A sample audit (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
