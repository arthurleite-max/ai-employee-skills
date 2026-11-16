# Partnerships Scout

An AI skill for business owners who know partnerships work but never find the time to do them. It:

- **finds partners that fit**: podcasts, creators, complementary businesses, communities and local
  partners, scored with clear criteria;
- **researches each one** and the best way to approach them (channel, angle, a real hook);
- **writes short personalised messages** for your approval;
- **tracks replies and follow-ups** in a simple pipeline, and tells you every day what needs you.

**Nothing is sent without your yes.** A "no" is final, there are at most two follow-ups, personalisation
uses only verified facts, and it never uses bought lists, private phone numbers or mass sending.

## Works with any AI

| AI | What it can use |
|---|---|
| Agents with browsing, email drafts and schedules | Researches public pages daily, keeps `pipeline.csv`, creates drafts (never sends), runs `scripts/pipeline.py` |
| Claude, ChatGPT, Gemini, Kimi (skill upload, browsing) | Public pages it can open, files you attach |
| DeepSeek, Qwen, free ChatGPT, any chat (paste `PASTE-INTO-ANY-AI.md`) | Candidates, replies and the pipeline you paste |

## Install

- **Option 1 (recommended):** paste the text below the line in `INSTALL.md` into your AI.
- **Option 2:** upload `downloads/partnerships-scout.zip` (from this repository) as a skill, or copy the folder to `~/.claude/skills/` or
  `~/.agents/skills/`. Maintainers build the zip with `sh build.sh`.
- **Option 3:** paste `PASTE-INTO-ANY-AI.md` as the first message of a new conversation.

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
