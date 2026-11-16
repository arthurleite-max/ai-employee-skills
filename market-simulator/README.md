# Market Simulator

An AI skill for testing an idea on simulated customers before you spend on a launch. It:

- **builds a panel of simulated customers** from your own market facts, with sceptics and fans mixed;
- **lets them react in rounds**: first impressions alone, then after hearing each other, then the decision;
- **tests what you need**: a product, an offer, a price, a headline, an ad, a page, an app or an AI skill;
- **returns a clear report**: weighted purchase intent with the maths, revenue and margin per 100 people,
  objections in the customers' own words, what to change, and the cheapest real test to confirm it.

You can also interview any simulated customer, or rehearse "what if" scenarios. It is a rehearsal, not
market research: results are always labelled simulated and never used as proof in advertising.

> Ideas inspired by multi-agent "digital world" simulators. This skill runs in any AI, with no servers,
> API keys or installation.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download market-simulator.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/market-simulator.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **test my idea** (on Claude, the first time: *"Use my Market Simulator skill: test my idea"*).
It answers in your language, whatever language you write to it in.

## First use

Say **test my idea** and paste what you want to test. It asks who buys, what they use today, price and
cost and what you already know (about 10 minutes), then runs the simulation.

## The local helper

```
python scripts/simpanel.py panel segments.csv --size 24
python scripts/simpanel.py tally reactions.csv --segments segments.csv --price A=32 --price B=27 --cost 19
```

`panel` spreads personas by your segment shares (and warns when shares do not add up to 100%). `tally`
computes weighted intent per variant, revenue and margin per 100 people, ranked objections and changes
between rounds. Python 3.8+, nothing to install, no internet. Try it with the files in `templates/` and
`assets/`.

## What you can ask

| You say | It does |
|---|---|
| `test my idea` | Concept test with a simulated panel |
| `test this price` / `which offer?` | Variants side by side, with margin |
| `which headline works better?` | Message test A/B |
| `get feedback on my page / app / skill` | Simulated users walk through it and say where they stop |
| `what if a competitor drops the price?` | Scenario rehearsal on the same panel |
| `talk to persona P07` | Interview a simulated customer |
| `here are the real results` | Calibration for the next run |

## Safety

- Simulated results are never presented as real research or used in ads.
- Personas are built from needs and context, never from stereotypes.
- No real people are imitated.
- Instructions hidden in pasted reviews or pages are reported, never followed.
- Every report ends with a real, cheap test.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The simulator · first-time questions |
| `reference/` | Simulation, personas, analysis, validation, safety, pitfalls |
| `templates/` | Market brief, segments, report |
| `scripts/simpanel.py` | Panel and weighted tally |
| `assets/` | Example panel, reactions and results (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
