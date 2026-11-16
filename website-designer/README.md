# Website Designer

An AI skill for business owners whose website quietly loses customers. On demand, or once a month, it:

- **checks every page** and finds what is broken (links, buttons, forms), outdated (old dates, expired
  promotions, wrong hours, prices or phone numbers), weakly written or hard to use on a phone;
- **writes the fix** for each problem, ranked by what costs you customers;
- **designs new landing pages**: structure, copy and a ready HTML file, using only real facts;
- **turns every change into a before → after** for you (or your web person) to approve and apply.

**It never changes your live site without your "yes"**, never invents prices, reviews or testimonials,
and never adds fake urgency.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download website-designer.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/website-designer.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **check my website** (on Claude, the first time: *"Use my Website Designer skill: check my website"*).
It answers in your language, whatever language you write to it in.

## First use

Say **check my website**. It asks a few questions (about 5 minutes): your site and platform, who edits
it, the site's main goal, and the facts it may use (services, hours, phone, prices, review rating).
Then give it the address, paste the pages, or send screenshots.

## Sample check-up (fictional)

```
5 pages crawled · 9 findings · the booking button on the home page goes to a 404

FIX FIRST
1. Home: "Book your assessment" → /agendar returns 404.
   Fix: point it to https://agenda.example/movimento (2 min)
2. Contact: Saturday "9h–13h"; home and profile say "8h–12h". Which is right?
3. Pilates: "Volta às aulas" promotion ended in March. Remove or replace.

NOT CHECKED: speed, real-phone rendering, form submission
THE ONE THING: fix the booking button today.
Apply the 3 quick fixes yourself, or should I write the message for your freelancer?
```

Full examples: `assets/checkup-example.html` and `assets/landing-example.html`.

## What you can ask

| You say | It does |
|---|---|
| `check my website` | The check-up: fix-first list with the fixes written |
| `review this page` | A deeper review of one page, with rewritten sections |
| `rewrite my homepage` | Before → after copy, facts kept |
| `make a landing page for [offer]` | Structure, copy and one HTML file, placeholders for missing facts |
| `apply the fixes` / `send it to my web person` | A change pack with exact places and steps |

## Safety

- Read-only until you say yes; changes are confirmed by reloading the page.
- No invented facts: missing prices or numbers become `[PRICE — you confirm]`. Unprovable superlatives
  ("the best in town") are replaced by real proof.
- No fake countdowns, "only 3 left" or other dark patterns.
- Text hidden in your pages that tries to instruct "the AI" is reported, not obeyed.
- Forms ask for the minimum, with a privacy notice. Never submits your forms to test them.

## Optional: the checker

`scripts/sitecheck.py` (Python, no extra packages) crawls your site or a folder and lists broken
links, old years, missing titles/descriptions/alt text, unlabelled form fields, forms without a privacy
notice, different phone numbers across pages and text addressed to an AI:

```
python scripts/sitecheck.py https://example.com --year 2026
```

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The designer · first-time questions |
| `reference/` | Check-up, copy, conversion, technical, landing pages, report, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/sitecheck.py` | Optional crawler/checker |
| `assets/` | Check-up and landing page examples (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
