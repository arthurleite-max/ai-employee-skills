# Ads Manager

An AI skill for business owners who run Meta Ads and Google Ads without a full-time media buyer. Every
morning it:

- **reviews spend and pacing** against your monthly budget;
- **checks each campaign and ad**: cost per lead, cost per **real** customer, CTR, frequency;
- **flags** ads wasting money, tired creatives, campaigns worth scaling and tracking gaps;
- **proposes changes and new ads** in a numbered list for you to approve.

**It never changes your campaigns or budgets** and never asks for your passwords. It uses your real sales
as the truth, raises budgets in small steps and writes ads that follow platform policies.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download ads-manager.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/ads-manager.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **check my ads** (on Claude, the first time: *"Use my Ads Manager skill: check my ads"*).
It answers in your language, whatever language you write to it in.

## First use

Say **check my ads**. It asks about your offer, budget, target cost per lead and per customer, where real
sales are recorded and which claims you can prove (about 10 minutes). Then paste the last 14 days per ad
(date, campaign, ad, spend, impressions, reach, clicks, leads) and real customers per campaign.

## Sample morning review (fictional)

```
Fri 12/06 · Meta + Google · 05–11/06 vs 29/05–04/06
Pace: 1,560 ÷ 11 days × 30 = 4,254.55 (106.4% of 4,000) → trim Meta 5% (approve?)
Google search: CPL 520 ÷ 26 = 20.00 (target 35), limited by budget → +15% (approve?)
Meta "Smile video": CTR 1.6% → 0.9% (−43.8%), frequency 3.6 → new creative
Meta "Offer card": 74 spent, 0 leads (2 × 35 = 70) → pause (approve?)
Cost per new patient: Google 1,040 ÷ 8 = 130.00 · Meta 980 ÷ 4 = 245.00 (target 180)
Headline: move money from tired Meta ads to Google search, in small steps.
```

## What you can ask

| You say | It does |
|---|---|
| `check my ads` | The morning review and the change list |
| `ads report` / `how was the month?` | Totals, campaigns, ads, real customers, what changed and what happened |
| `which ads should I pause?` | Only the ones the numbers condemn, with the division |
| `should I raise the budget?` | A step size, the risk and what to check |
| `write new ads` | 3–5 compliant variations, each testing one thing |

## Safety

- Read-only: nothing changes without your yes; never handles passwords.
- Real customers decide; platform conversions are never added together.
- No verdicts on tiny numbers; budget steps of about 15–20%.
- Policy-safe copy: no weight-loss or income promises, no before-and-after, no personal-attribute hooks.
- Comments or emails "from support" asking for logins are reported as possible phishing.

## Optional: the ads calculator

```
python scripts/adscan.py ads.csv --today 2026-06-04 --target-cpl 35 --target-customer 180 --crm crm.csv --budget 4000 --month-spend 1500
```

Compares the last 7 days with the 7 before, per ad and campaign, and prints pacing, cost per real
customer and the flags (waste, fatigue, scale, tracking, learning).

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The ads manager · first-time questions |
| `reference/` | Metrics, review, flags, ad copy, policies, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/adscan.py` | Optional calculator |
| `assets/morning-review-example.html` | Sample review (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
