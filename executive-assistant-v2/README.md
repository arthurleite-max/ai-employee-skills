# Executive Assistant (v2)

An AI skill for business owners. Every morning it reads your email, WhatsApp and calendar and gives you:

- **the short list of what only you can decide**, ranked by what hurts if it waits;
- **routine replies already drafted** in the way you write;
- **today's agenda**, with a focus for each meeting and the conflicts flagged;
- **your promises, deadlines and follow-ups**, so nothing slips.

**It never sends anything without your "yes".** And it warns you when a message looks like a scam.

> step-by-step installation for your AI, with no technical jargon.

## Works with any AI

| AI | How |
|---|---|
| **Claude** (web, desktop) | Upload the skill (zip) |
| **ChatGPT** (Plus and above) | Upload the skill (zip) |
| **Gemini** (web, Mac app) | Upload `SKILL.md` and the reference files |
| **Kimi** | Upload the skill (zip) |
| **Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor** and other Agent Skills tools | Your AI installs it (see below) |
| **DeepSeek, Qwen, Mistral, Llama, Grok, free ChatGPT** and any other chat | Paste `PASTE-INTO-ANY-AI.md` |

It answers in your language, whatever language you write to it in.

## Install

### Option 1: let your AI install it (recommended)

Open `INSTALL.md`, copy the text below the line, paste it into your AI (attach
`executive-assistant-v2.zip` if you have it) and send. Coding agents install it themselves; chat apps
walk you through it step by step or start working right away.

### Option 2: upload the skill

1. Download `executive-assistant-v2.zip` from the page where you found this skill (for example the
   repository's Releases page). Maintainers build it with `sh build.sh` at the repository root.
2. Upload it:
   - **Claude:** Settings → Capabilities → Skills → Upload skill. ("Code execution and file creation"
     must be on.)
   - **ChatGPT:** Skills → Create → Upload from computer.
   - **Gemini:** Skills (formerly Gems) → create/import → upload `SKILL.md` plus the files in
     `reference/` and `templates/`.
   - **Kimi:** Skills → `+` → upload the zip.
   - **Coding agents:** copy the `executive-assistant-v2` folder to `~/.claude/skills/` (Claude Code) or
     `~/.agents/skills/` (Codex, Gemini CLI, Copilot, Cursor…).
3. Open a new conversation and say **good morning**.

Menu names change over time. If you cannot find it, look for "Skills" in your AI's settings.

### Option 3: paste it into any AI

Open `PASTE-INTO-ANY-AI.md`, copy all of it and paste it as the first message of a new conversation,
or into your AI's project / custom-instructions field so it applies to every conversation. Works on free
plans too.

## First use

Say **good morning**. The first time, the assistant asks a few short questions (about 15 minutes): your
company, which inboxes to read, your important contacts, the topics that never go out without you, your
hours. Then it asks for 10 to 30 messages you have sent, to learn your voice. From then on, just say
"good morning".

No email connected? Fine: copy and paste the morning's messages into the conversation. If your AI
cannot save files, the assistant hands you your **profile** and **memory** as two text blocks: keep them
and paste them before tomorrow's "good morning".

## Sample output (fictional)

```
Good morning, Sam. 71 messages · 4 need you · the 2pm is the one that matters.

NEEDS YOU
1. Pinewood Timber "updated invoice": likely scam. The domain has an extra letter and the
   beneficiary changed. Do not pay; call the number you already have. (no draft)
2. Business license expires Friday: USD 412, risk of closure.
3. Northwind Construction: change order, they need the figure before Thursday's board.
4. Mrs. Hale, second message, upset: acknowledgement drafted; this needs a call.
5. You promised Hartley Studio the quote today.

DRAFTS READY: 5 (warranty question, 3 time options for Dana, referral thank-you, ...)
HANDLED: 2 pitches · 1 newsletter · 1 receipt · 1 tracking · 1 system notice

THE ONE THING: bring the change-order decision to the 2pm.
Send the 5 drafts, or review them one by one?
```

A full HTML example is in `assets/briefing-example.html`.

## Daily commands

| You say | It does |
|---|---|
| `good morning` | The full daily briefing |
| `what needs me?` | Inbox triage only |
| `reply to this: [message]` | One draft in your voice |
| `book 30 min with Julia next week` | Three free times on at least two days, checked against your calendar |
| `prep the 3pm` | Who is coming, history, promises, agenda, questions to ask |
| `write the minutes: [notes]` | Decisions, tasks with owners and dates, follow-up email |
| `what did I promise?` | What you promised, who is waiting on you, who you are waiting on, deadlines |
| `how does my week look?` | Full and free days, deadlines and the priority of the week |

## Safety

- Nothing is sent, booked, paid or deleted without your explicit yes.
- Text inside messages is treated as information, never as an order. A message that tries to instruct
  "the AI assistant" is flagged, not obeyed.
- Scams go straight to you with no draft: changed bank details or payment keys, "updated" invoices,
  "I changed my number" requests, fake tax notices, lookalike domains, code or gift-card requests.
- It never invents a price, date or commitment; it leaves `[AMOUNT — you decide]` instead.
- It archives, never deletes, and never replies on top of a colleague who already answered.
- Third parties' personal data stays to the minimum, in line with privacy laws such as GDPR, LGPD or CCPA.

Even with the warning, always confirm by phone before paying anything.

## Troubleshooting

| Problem | Fix |
|---|---|
| The upload is rejected | Check you uploaded the zip that contains the `executive-assistant-v2` folder with `SKILL.md` inside. On Claude, turn on "Code execution and file creation". |
| No Skills option in my AI | Use Option 3 (paste). It works on any plan. |
| It does not remember yesterday | Paste the profile and memory blocks it gave you before saying "good morning", or use a project (Option 3). |
| Amounts show up scrambled | Some apps turn text between "$" signs into formulas. The assistant writes "USD 1,200" to avoid it; ask it to do so if it slips. |
| It searched the web | Turn off web search while using it; it does not need the internet to organise your day. |
| A draft is not in my voice | Edit it and say why; it records the rule and does not repeat the mistake. |

## Files

| File | For |
|---|---|
| `INSTALL.md` | Text you paste into your AI so it installs or guides the install |
| `SKILL.md` | The assistant itself (read by the AI) |
| `setup.md` | The first-time interview that writes your profile |
| `PASTE-INTO-ANY-AI.md` | Compact edition for any AI without skills support |
| `reference/` | Triage, drafting, calendar, briefing, safety and pitfalls rules |
| `templates/` | Profile and memory templates |
| `assets/briefing-example.html` | Sample briefing (fictional data) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
