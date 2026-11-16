# Partnerships Scout

An AI skill for business owners who know partnerships work but never find the time to do them. It:

- **finds partners that fit**: podcasts, creators, complementary businesses, communities and local
  partners, scored with clear criteria;
- **researches each one** and the best way to approach them (channel, angle, a real hook);
- **writes short personalised messages** for your approval;
- **tracks replies and follow-ups** in a simple pipeline, and tells you every day what needs you.

**Nothing is sent without your yes.** A "no" is final, there are at most two follow-ups, personalisation
uses only verified facts, and it never uses bought lists, private phone numbers or mass sending.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download partnerships-scout.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/partnerships-scout.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **find partners** (on Claude, the first time: *"Use my Partnerships Scout skill: find partners"*).
It answers in your language, whatever language you write to it in.

## First use

Say **find partners**. It asks about your business, the prices it may quote, your ideal partners, what
you can offer them and how you like to write (about 10 minutes). Then it builds a first shortlist and an
empty pipeline.

## Sample daily list (fictional)

```
Wed 20/05 · Pedal Café partnerships
Reply to answer: Roda Livre bikes asks about the commission → draft ready, 10% as in your profile.
Follow-up due: Pedal Talk podcast (20/05 − 14/05 = 6 days, follow-up 1) → draft ready.
Do not contact: Corre POA club (asked not to be contacted on 22/04).
New: Gira Sul podcast 3 + 2 + 2 + 3 = 10 → first message ready (hook: episode of 18/05).
Approve the three drafts?
```

## What you can ask

| You say | It does |
|---|---|
| `find partners` / `find podcasts for me` | Candidates by type, fit score with sums, public contact check |
| `research [partner]` | Who they are, recent work, what they gain, best channel, angle, verified hook |
| `write the outreach` | Short drafts for approval, in the partner's language |
| `daily partnerships` / `who do I follow up with?` | Replies, follow-ups due, closed, new contacts, pipeline |
| `reply to this` | A reply using only your facts; anything not set becomes [owner to confirm] |

## Safety

- Drafts only: nothing is sent, signed or promised without your yes.
- "No" means never again; at most 2 follow-ups.
- Only verified facts in messages; no fake familiarity or invented numbers.
- Public business channels only; no private numbers, bought lists or mass sending.
- Sponsored content is disclosed as advertising.
- Replies asking "the AI" for customer lists, passwords or payments are reported, never followed.

## Optional: the pipeline checker

```
python scripts/pipeline.py pipeline.csv --today 2026-05-20 --score candidates.csv
```

Lists suspicious replies, do-not-contact, replies to answer, follow-ups due (with the day count),
conversations to close and fit scores with their sums.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The scout · first-time questions |
| `reference/` | Finding, scoring, research, outreach, pipeline, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/pipeline.py` | Optional pipeline checker |
| `assets/daily-pipeline-example.html` | Sample daily list (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
