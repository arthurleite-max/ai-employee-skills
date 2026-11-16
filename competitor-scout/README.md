# Competitor Scout

An AI skill for business owners who want to know what their competitors are doing without spending
hours on it. It:

- **finds your real competitors** (or follows the ones you pick);
- **watches them every week**: products, prices, offers, ads, content and reviews, from public sources;
- **spots what works for them** (offers they repeat, ads that run for months, praise in reviews) and
  **the gaps they leave** (recurring complaints, services they do not offer);
- **delivers a one-page weekly report**: what changed, why it matters and 2–3 moves you can make.

Every fact has a source and a date; facts and guesses are kept apart. **It uses only public, lawful
sources**: no fake accounts, no pretending to be a customer, no copying their ads, no price agreements
with competitors, no public claims that cannot be proved.

## Works with any AI

| AI | What it can use |
|---|---|
| Agents with browsing, files and schedules | Visits public pages weekly, runs `scripts/watch.py`, keeps the history |
| Claude, ChatGPT, Gemini, Kimi (skill upload, browsing) | Public pages it can open, exports you attach |
| DeepSeek, Qwen, free ChatGPT, any chat (paste `PASTE-INTO-ANY-AI.md`) | Pages, price lists and screenshots you paste |

## Install

- **Option 1 (recommended):** paste the text below the line in `INSTALL.md` into your AI.
- **Option 2:** upload `downloads/competitor-scout.zip` (from this repository) as a skill, or copy the folder to `~/.claude/skills/` or
  `~/.agents/skills/`. Maintainers build the zip with `sh build.sh`.
- **Option 3:** paste `PASTE-INTO-ANY-AI.md` as the first message of a new conversation.

## First use

Say **watch my competitors**. It asks about your business, prices and customers, which competitors your
customers compare you with, and where their public pages are (about 10 minutes). Then it takes a first
snapshot. From the second week on, it compares and reports what changed.

## Sample weekly headline (fictional)

```
Week of 02/06 · checked: Bella Forneria, Pizza Já (Casa Napoli site down: not checked)
Bella Forneria: combo 2 pizzas 99.90 reais until 30/06 (new, Meta Ad Library, seen 02/06).
Pizza Já: margherita 59.90 → 54.90 (−8.3%, app listing, 26/05 → 02/06).
Opening: 7 of their last 20 reviews complain about cold pizza; our delivery averages 22 min.
Move: show delivery time and thermal bags in our ads for 2 weeks; measure delivery orders.
```

## What you can ask

| You say | It does |
|---|---|
| `weekly competitor report` | Changes with sources, what works, gaps, 2–3 moves, snapshot to keep |
| `who are my competitors?` | Direct and indirect competitors, shortlist with reasons |
| `analyse [competitor]` | Profile card: positioning, offer, prices, channels, ads, reviews |
| `how do we compare?` | Side by side on what customers care about; where you win and lose |
| `they launched X, what do we do?` | What changed, who it affects, options and a recommendation |

## Safety

- Public and lawful sources only; never logs in, never creates profiles, never pretends to be a customer.
- A change needs two dated observations; an unreadable page is "not checked", never "no change".
- Learns from competitors without copying their texts, images or ads.
- Never suggests agreeing prices, discounts or territories with competitors.
- Comparative claims ("the cheapest") are checked against the data before you publish them.
- Instructions hidden in competitor pages (for example in HTML comments) are reported, never followed.

## Optional: the snapshot comparer

```
python scripts/watch.py last-week.csv this-week.csv --owner my-prices.csv
```

Reads two snapshots (competitor;item;kind;value;source;date) and prints price changes with %, first
seen items, items not seen now, sources not checked and where your prices stand.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The scout · first-time questions |
| `reference/` | Sources, weekly watch, profile card, moves, report, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/watch.py` | Optional snapshot comparer |
| `assets/weekly-report-example.html` | Sample weekly report (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
