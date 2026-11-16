# Support Agent

An AI skill for business owners who answer the same customer questions every day. It:

- **answers routine questions** by email, chat and direct messages, from your own knowledge base;
- **explains products, services and policies** in your voice, in the customer's language;
- **sorts the inbox**: red (a person now), yellow (your approval), green (answered from the knowledge base);
- **hands off sensitive cases** with a note so you never have to ask the customer again.

It never invents a policy, price or date, never promises refunds or exceptions your policy does not offer,
checks identity before sharing order details and never repeats card numbers or passwords. Nothing is sent
without your permission unless you turn on autopilot for topics you choose.

## Works with any AI

| AI | What it can use |
|---|---|
| Agents and AIs that run code (Claude, ChatGPT with code, Gemini, Kimi) | Runs `scripts/inbox.py` on your inbox export, then drafts in queue order |
| DeepSeek, Qwen, free ChatGPT, any chat (paste `PASTE-INTO-ANY-AI.md`) | Triage table, clock table and a draft for every message you paste |

## Install

- **Option 1 (recommended):** paste the text below the line in `INSTALL.md` into your AI.
- **Option 2:** upload `downloads/support-agent.zip` (from this repository) as a skill, or copy the folder to `~/.claude/skills/` or
  `~/.agents/skills/`. Maintainers build the zip with `sh build.sh`.
- **Option 3:** paste `PASTE-INTO-ANY-AI.md` as the first message of a new conversation.

## First use

Say **set up my support**. It asks about your channels, hours, voice, policies and the 10 questions you get
most (about 10 minutes), and writes your profile and knowledge base for you to approve. Then paste
messages and say **answer these**.

## Sort an inbox export

```
python scripts/inbox.py messages.csv --now 2026-06-04T10:00 --kb knowledge-base.md --sla-hours 24
```

Groups messages by customer, computes hours waiting against your first-reply target, tiers each
conversation, masks card numbers, ID numbers and passwords, flags instructions hidden in messages and
lists questions your knowledge base does not answer. Python 3.8+, nothing to install, read-only. Try it
with `assets/example-inbox.csv`.

## What you can ask

| You say | It does |
|---|---|
| `answer this customer` | A draft from your knowledge base, with tier and topic used |
| `check my inbox` | Clock table, queue in order, drafts, hand-off notes |
| `pass this to me` | A hand-off note with the whole story |
| `update the FAQ` | New knowledge base topics from gaps and solved cases |
| `how is support going?` | Weekly review: volume, late replies, top questions, gaps |

## Safety

- Answers only from your knowledge base; unknown → "I will check".
- Your policy is the limit; exceptions are yours to decide.
- Health, legal, payment disputes, data requests and angry repeat contacts go to a person.
- Identity check before order details; card numbers and passwords never repeated.
- Instructions hidden in customer messages are reported, never followed.
- Says it is an AI when asked.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The support agent · first-time questions |
| `reference/` | Triage, replies, hand-off, knowledge base, safety, pitfalls |
| `templates/` | Profile, knowledge base and hand-off note examples |
| `scripts/inbox.py` | Inbox triage: clock, tiers, masking, knowledge base gaps |
| `assets/example-inbox.csv` · `assets/example-queue.md` | Sample inbox and its queue (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
