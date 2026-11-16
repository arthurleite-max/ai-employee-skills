# Finance Watchdog

An AI skill for business owners (and households). It reads your bank and card statements every week and
tells you:

- **what is wrong right now**: card fraud, duplicate charges, charges after you cancelled, unknown merchants;
- **what got more expensive**: subscriptions and bills that went up, new fees, interest;
- **what you can stop paying for**: forgotten subscriptions, overlapping tools, free trials that became charges;
- **how much each change saves per year**, with the deadline to act.

**It is read-only.** It never pays, transfers, cancels or contacts anyone; it prepares the steps and the
message, and you decide. It never asks for passwords and never invents a number.


## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download finance-watchdog.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/finance-watchdog.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **audit my expenses** (on Claude, the first time: *"Use my Finance Watchdog skill: audit my expenses"*).
It answers in your language, whatever language you write to it in.

## First use

1. Export **3 months** of statements from your banking app (CSV or OFX is best; PDF or screenshots work).
   12 months also catches yearly renewals. Never share passwords or full card numbers.
2. Say **audit my expenses** and attach them. The watchdog asks a few short questions (about 10 minutes):
   your accounts and cards, your own savings accounts, main suppliers, what must never be cut.
3. You get the first audit: alerts, every subscription with its yearly cost, fees and interest, and the
   savings list. Answer the questions about the items it could not decide on its own.
4. Every week after that: paste or attach the week's statement and say **weekly report**.

If your AI cannot save files, the watchdog hands you your **profile** and **memory** as two text blocks:
keep them and paste them with the next statement.

## Sample report (fictional)

```
Nov 2–8 · BRL 18,410 out · 2 act-now · about BRL 3,900/year you can stop paying

ACT NOW
1. Card •••• 9021 looks like it is being tested by fraudsters: 3 charges under BRL 3 from
   an unknown merchant, then BRL 612.40 at an online shop. Block it in the bank's official app.
2. VidCall charged BRL 49.00 after you cancelled on 02/10. Ask for the refund (message ready).

DECIDE THIS WEEK
3. Internet 159.90 → 199.90 (+25%, BRL 480/year): the promotion ended. Negotiate or switch.
4. Two cloud-storage plans (BRL 1,200/year together). Keep one?
5. Software annual renewal on 20/11: BRL 1,188. Cancel by 18/11 if not needed.

THE ONE THING: block the card today.
```

A full HTML example is in `assets/report-example.html`.

## Daily commands

| You say | It does |
|---|---|
| `audit my expenses` + statements | First full audit: alerts, subscriptions map, fees, savings |
| `weekly report` + this week's statement | Only what changed and what needs a decision |
| `what is this charge? [line]` | Looks for it in your data; says "unidentified" if it cannot tell |
| `review my subscriptions` | One by one: keep, cancel, downgrade, annual |
| `how was October?` | Categories vs your average, what went up, fees paid |
| `can I afford [X]?` | The arithmetic with your real balance and known bills; you decide |
| `cancel [X] for me` | Step-by-step and the message to send; you click |

## Safety

- Read-only: nothing is paid, moved, cancelled or disputed by the watchdog.
- Never asks for passwords, codes or full card numbers.
- Text inside statements and emails is information, never an order: a transfer message telling "the AI"
  to approve expenses is flagged, not obeyed. Fake "your card was blocked, click here" messages are
  flagged as phishing.
- Unknown merchants are marked "unidentified", never guessed. Savings are "estimated" until the next
  statement proves them.
- Not financial, tax or legal advice: it shows the numbers and points you to your accountant or bank.

## Optional: exact arithmetic

`scripts/watchdog.py` is a small local calculator (Python, no internet, nothing to install) that AIs
with code execution use to add up statements exactly. It only reads the files you give it.

```
python scripts/watchdog.py --in "bank.csv|Business account" --in "card.csv|Card 9021|flip" --threshold 300
```

## Troubleshooting

| Problem | Fix |
|---|---|
| The upload is rejected | Check you uploaded the zip that contains the `finance-watchdog` folder with `SKILL.md` inside. |
| No Skills option in my AI | Use Option 3 (paste). It works on any plan. |
| Totals look wrong | Check the coverage line: a missing card, or a card bill counted twice. Tell it which accounts are yours. |
| It does not remember last week | Paste the profile and memory blocks it gave you, with the new statement. |
| Amounts show up scrambled | Some apps turn text between "$" signs into formulas. Ask it to write "BRL 1,200" style. |
| My bank's PDF is unreadable | Export CSV or OFX, or send screenshots. |

## Files

| File | For |
|---|---|
| `INSTALL.md` | Text you paste into your AI so it installs or guides the install |
| `SKILL.md` | The watchdog itself (read by the AI) |
| `setup.md` | The first-time interview that writes your profile |
| `PASTE-INTO-ANY-AI.md` | Compact edition for any AI without skills support |
| `reference/` | Intake, categories, detection, subscriptions, report, safety and pitfalls |
| `templates/` | Profile and memory templates |
| `scripts/watchdog.py` | Optional local calculator |
| `assets/report-example.html` | Sample report (fictional data) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
