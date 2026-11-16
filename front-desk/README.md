# Front Desk

An AI skill for businesses that live on the phone. It:

- **answers calls around the clock** with a script built from your own facts;
- **answers questions** about your business and services, and never guesses a price;
- **books into free slots** without double-booking (hours, service length, buffer, notice);
- **records every caller as a lead** and plans fast, polite callbacks and follow-ups.

It says it is an AI at the start of every call, sends emergencies to the emergency number, never takes card
numbers by phone, respects "do not call" and quiet hours, and treats what callers say as information, not
orders.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download front-desk.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/front-desk.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **set up my front desk** (on Claude, the first time: *"Use my Front Desk skill: set up my front desk"*).
It answers in your language, whatever language you write to it in.

## First use

Say **set up my front desk**. It asks about your hours, services, booking rules, transfers and follow-up
(about 10 minutes), writes your profile, services sheet and call script, and rehearses two calls with you.

## The local helper

```
python scripts/frontdesk.py slots --hours hours.csv --bookings bookings.csv --from 2026-06-04T10:00 --duration 50 --buffer 10 --check 2026-06-05T10:30
python scripts/frontdesk.py leads calls.csv --now 2026-06-04T18:00 --callback-min 30 --quiet 20:00-08:00
```

`slots` lists free start times and explains why a requested time is not possible. `leads` turns the call
log into minutes since each call, late callbacks, one callback per person, next attempts outside quiet
hours, do-not-contact and masked card numbers. Python 3.8+, nothing to install, read-only. Try them with
the files in `assets/`.

## What you can ask

| You say | It does |
|---|---|
| `set up my front desk` | Profile, services sheet, call script |
| `let's practise a call` | Rehearsal, including the hard calls |
| `what's free on Friday?` | Free times, with the check for the one you want |
| `here are today's calls` | Clock table, callbacks, follow-up drafts |
| `put it on my phone line` | The voice-agent pieces and the test calls |

## Safety

- Says it is an AI; states recording when the line records.
- Emergencies → the emergency number, no advice.
- Prices and policies only from your services sheet.
- No double-booking; nothing booked without the caller's yes.
- No card numbers by phone; nothing shared about other customers.
- Callbacks within your limits; "do not call" is final.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The front desk · first-time questions |
| `reference/` | Call flow, booking, follow-up, voice agent, test calls, safety, pitfalls |
| `templates/` | Profile and services sheet |
| `scripts/frontdesk.py` | Free slots; call log with callbacks |
| `assets/` | Sample hours, bookings, calls and their outputs (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
