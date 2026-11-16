# YouTube Strategist

An AI skill for business owners and creators who want their YouTube channel to grow and bring
customers. Once a week it delivers one page with:

- **what is working in your niche**: videos that beat their own channel's normal views, with the
  numbers to prove it;
- **three topics with room to win**, scored with evidence and matched to your business;
- **10 titles** checked for length, clarity and honesty, top 3 marked;
- **10 thumbnail ideas** paired with the titles, ready to review and test;
- **your own channel's health** and the next video plan.

**It never changes your channel**, never invents views, endorsements or results, and never copies other
creators' titles or thumbnails.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download youtube-strategist.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/youtube-strategist.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **weekly YouTube plan** (on Claude, the first time: *"Use my YouTube Strategist skill: weekly YouTube plan"*).
It answers in your language, whatever language you write to it in.

## First use

Say **weekly YouTube plan**. It asks about your channel, audience, business, formats, voice and
thumbnail style, and 3–5 channels in your niche (about 10 minutes). Then paste your last 20 videos with
views (YouTube Studio → Content) and, for each niche channel, its subscribers and last 10–15 videos with
views and dates.

## Sample (fictional)

```
Your channel: median 1,800 views (12 videos); last 5: 1,050 (−42%).
"Unclog a sink without chemicals" got 14,500 (8.1×) and was never followed up.

Niche outliers:
- "Dripping tap? Fix it in 5 minutes" · Simple Repairs (85k) · 410,000 · 20.5× its median
- "Shower element burned out?" · Electrician Joe (40k) · 260,000 · 32.5×

Topic with room: single-handle tap repair — 2 channels, small-channel proof, few recent videos.
Top pair: "Tap still dripping after a new washer? Here's why" + thumbnail "WRONG PART" (close-up)
Which topic, and which title + thumbnail pair do you want to test?
```

## What you can ask

| You say | It does |
|---|---|
| `weekly YouTube plan` | The full one-page report |
| `what works in my niche?` + video list | Outliers and patterns, with evidence |
| `why isn't my channel growing?` + Studio numbers | Channel audit and next tests |
| `next video ideas` | Three topics with room |
| `10 titles for [video]` / `thumbnail ideas` | Packaging, checked and paired |
| `plan the video about [topic]` | Promise, first 30 seconds, structure, payoff |

## Safety

- Nothing on your channel changes without your yes.
- No invented numbers, endorsements, view counts or results in titles and thumbnails.
- Patterns from other creators, never their titles, thumbnails or scripts.
- No other brands' logos or other people's faces without permission.
- A comment asking "the AI" to rename a video or add a link is reported, not obeyed.

## Optional: the helper

```
python scripts/ytlint.py outliers videos.csv --today 2026-11-11     # medians, ratios, outliers
python scripts/ytlint.py titles titles.txt --thumb "WRONG PART"     # title checks
```

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The strategist · first-time questions |
| `reference/` | Research, channel audit, topics, titles, thumbnails, report, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/ytlint.py` | Optional helper (outliers and title checks) |
| `assets/weekly-report-example.html` | Sample weekly report (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
