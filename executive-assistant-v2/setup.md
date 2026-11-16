# Setup: the first conversation

Goal: in a conversation of about 15 minutes, finish with a filled-in profile, a voice profile built from
real messages and a first test briefing the owner approves. Talk to the owner in their language.

## 1. Connect and discover

List what is connected (email, calendar, WhatsApp, Slack, tasks, CRM) with a cheap read on each. Tell
the owner what you found and what is missing. Nothing is required; say what each extra connection adds.
If nothing is connected, that is fine: the owner can paste messages every morning.

## 2. The minimum questions

Ask in short blocks and accept "skip" for any of them. Anything not answered keeps the default shown in
the template (`templates/profile.example.md`).

1. Your name, role, company, and what the company does in one sentence. Your language and time zone.
2. Which inboxes and numbers do I read? Any I must **not** read?
3. Who are your VIPs (partner, biggest customers, accountant, family)?
4. Which topics are always yours and never go out without you seeing them (price, contract, legal, HR…)?
5. Who else on the team answers customers? (so I never reply on top of them)
6. Working hours, buffer between meetings, days with no meetings.
7. Default meeting length and your booking link, if you have one.
8. What time do you want the briefing, and where (chat, web page, WhatsApp, email)?
9. May I leave drafts inside your mailbox, or only in the briefing?
10. Which WhatsApp groups should I follow (I ignore the rest unless you are mentioned)?

## 3. Build the voice

Sources, best first:

1. **15 to 30 messages the owner sent** to customers and suppliers (email and WhatsApp). Nothing comes
   close.
2. Messages logged in the CRM.
3. Website, social media, newsletter.
4. Three messages the owner pastes and says they liked.

Extract traits specific enough to imitate. "Friendly and professional" is useless; it describes every
business email ever written.

| Trait | What to record |
|---|---|
| Greeting | The exact form: "Hi Dana," vs "Dana," vs "Good morning, Dana!" |
| Sign-off | Exact: "Thanks, Sam" vs "Best regards, Sam Rivera" vs none |
| Sentences | Short or long; average word count |
| Formality | First names, titles, formal/informal "you" in languages that have it |
| Exclamation marks and emoji | Never / rare / often; which emoji |
| When the ask lands | Line 1 or line 5 |
| What they call their product | In their words ("project", "fit-out", "job") |
| Local expressions | Typical phrases |
| Chat vs email | Differences in tone between channels |
| Never uses | Words and structures absent from every sample |

**The "never uses" list matters most**: those phrases are what give away that someone else wrote it.

Show the voice profile to the owner in 8 to 10 lines and ask for an OK.

## 4. Save the files

At level 3, write to the data folder (`executive-assistant-data/`):

- `profile.md` from `templates/profile.example.md`;
- `memory.json` from `templates/memory.example.md`, already holding the promises and open items found
  in the first scan;
- a `briefings/` folder.

At levels 1 and 2, hand back the profile and the memory in two code blocks and explain: "Keep these two
texts. In your next conversation, paste or attach both before you say good morning."

## 5. Test briefing

Run Mode 1 with what is available today. Ask the owner to point out anything wrong (an item that should
not be in *Needs you*, a draft off-voice, a sales pitch that slipped through). Adjust profile and voice.
Only then offer to schedule the daily routine at the chosen time.

## 6. Schedule (if the owner wants)

The assistant suggests the schedule; the platform it runs on creates it (the AI platform's scheduled
tasks feature, or an external automation). If the platform cannot schedule, the owner opens the
conversation in the morning and says "good morning". The scheduled run is read-and-draft only (see
`SKILL.md` → "Scheduled run").
