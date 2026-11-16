# Head of Marketing

An AI skill for business owners who spend on marketing but are not sure what works. It:

- **checks the numbers every morning** (ads, leads, real sales, website) and tells you what moved;
- **finds problems and opportunities**: broken tracking, costs creeping up, the channel that brings
  customers cheapest;
- **sends the report** on its own rhythm: a daily pulse that fits a phone screen, a weekly report and a
  monthly review;
- **recommends priorities and campaigns** with cost, expected range and how to measure them;
- **answers any question** about your marketing from your own data.

**It never changes your budgets or campaigns** and never sends anything without your yes. It uses your
real sales as the truth (never the sum of what each ad platform claims) and never promises results.

## Works with any AI

| AI | What it can use |
|---|---|
| Agents with read-only connectors (ads, analytics, CRM) | Pulls numbers every morning, runs `scripts/pulse.py`, delivers the pulse |
| Claude, ChatGPT, Gemini, Kimi (skill upload) | Exports you attach; code execution for exact maths |
| DeepSeek, Qwen, free ChatGPT, any chat (paste `PASTE-INTO-ANY-AI.md`) | Numbers you paste; maths shown step by step |

For exact numbers, prefer an AI that can run code (or the script): chat-only AIs sometimes miscalculate.

## Install

- **Option 1 (recommended):** paste the text below the line in `INSTALL.md` into your AI.
- **Option 2:** upload `downloads/head-of-marketing.zip` (from this repository) as a skill, or copy the folder to `~/.claude/skills/` or
  `~/.agents/skills/`. Maintainers build the zip with `sh build.sh`.
- **Option 3:** paste `PASTE-INTO-ANY-AI.md` as the first message of a new conversation.

## First use

Say **weekly marketing report**. It asks about your business, goals, channels, budget and where real
sales are recorded (about 10 minutes). Then paste or attach daily numbers per channel (spend,
impressions, clicks, leads) and real sales per channel from your CRM or sales system.

## Sample daily pulse (fictional)

```
Thu 04/06 · data to 03/06 · sources: Google Ads, Meta Ads, CRM (analytics not connected)
Yesterday: 9 leads (usual 11) · 2 sign-ups (usual 1.4) · spend 310 reais (on pace)
⚠ Meta: 0 leads for 3 days with 120 reais/day spent → possible tracking failure. Check the form today.
The one thing: test the Meta lead form before changing anything.
Ask me anything about these numbers.
```

## What you can ask

| You say | It does |
|---|---|
| `good morning` / `morning numbers` | The daily pulse |
| `weekly marketing report` | Channels, real sales, attribution check, anomalies, three priorities |
| `how was October?` | Monthly review vs goal |
| `where should I put my budget?` | Priorities from the data, with a small test first |
| `plan a campaign for…` | Goal, audience, offer (yours), budget range, dates, stop rule |
| `why did leads drop?` | The answer from your numbers, facts separated from hypotheses |

## Safety

- Read-only: budgets, campaigns, emails and reports to others only with your yes.
- Real sales are the truth; platform claims are never added together.
- A sudden zero is flagged as a possible tracking failure, not a disaster.
- No invented numbers, forecasts or benchmarks; small numbers called noise.
- Lead names and contacts never appear in reports. Messages telling "the AI" to change budgets or send
  leads are reported.

## Optional: the pulse calculator

```
python scripts/pulse.py daily.csv --today 2026-06-04
```

Reads a CSV (date, channel, spend, impressions, clicks, leads, sales, revenue, platform conversions; a
`TOTAL_CRM` channel for real totals) and prints the week-over-week table, anomalies and the attribution
check.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The head of marketing · first-time questions |
| `reference/` | Metrics, anomalies, attribution, campaigns, report, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/pulse.py` | Optional calculator |
| `assets/weekly-report-example.html` | Sample weekly report (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
