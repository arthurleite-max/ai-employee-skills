# The briefing

The briefing is the product. Everything before it exists for it.

**Target: ninety seconds to read.** The owner is holding a coffee. If it takes longer, the triage was
too loose; the format is not too tight.

## Structure (in this order)

0. **Critical source warning**: only if the calendar or the main inbox could not be read. One line, at
   the top, with what needs to be allowed.
1. **Headline**: one line: how much came in, how much needs the owner, and the shape of the day. *"71
   messages since yesterday · 4 need you · 3 meetings, the 2pm is the one that matters."*
2. **Needs you**: ranked by consequence. Each item: who, the ask in one line, amount/deadline, how long
   they have been waiting, what happens if it waits, and whether there is a supporting draft.
3. **Today's calendar**: external meetings with a suggested focus; conflicts; largest free block; what
   early tomorrow needs prepared today.
4. **Promises and deadlines**: promises coming due, who is waiting on the owner, deadlines in the next 7
   days, drafted follow-ups.
5. **Drafts ready**: table of recipient · channel · subject · one-line summary. Group similar ones ("3
   site-visit reschedules"). Items involving money, a VIP, a sensitive topic or a new recipient stay
   out of the batch.
6. **Handed off**: one line each, saying where it went **and what the owner does next**.
7. **Already handled by someone else**: one line each, no draft.
8. **Handled**: count per category + *"nothing here needs you; ask to see any category."*
9. **The one thing**: one, with the reason (the deadline, the amount, the person waiting).
10. **Sources**: one quiet line: what was read, what was not and why.
11. **Approval question**: one.
12. **Full text of every draft**, in the order of the table, with the original message summarised above.
    In HTML, each draft is a block with a "copy" button.
13. **Updated memory** in a code block (levels 1 and 2; mandatory, always last).

## The approval question

One question, two possible answers:

```
Send the 11 drafts, or review them one by one?
```

- "Send them all" → send, confirm by reading back, and say what went out ("11 sent: 8 emails, 3
  WhatsApp").
- "One by one" → show the original message and the draft, one at a time.
- An edit → apply it, record the voice correction, carry on.
- Risky items (money, sensitive topic, VIP, new recipient) **never** go in "send them all": they stay out
  of the batch and the briefing says so.

**No mailbox connected:** the last line changes: *"The 11 drafts are ready to copy. One file or one at a
time?"* That is a complete deliverable.

## The one thing

Pick one and say why. Example:

> **The one thing:** Northwind's USD 18,600 change order. Julia needs the answer before her board meets
> Thursday, and you see her today at 2pm. Bring the decision to the meeting.

## Leave out

- Subject lines in bulk. A list of 71 subjects is the problem restated.
- Explanations of how the triage worked.
- The *Handled* bucket item by item.
- "Maybe" on every item. If you were unsure about one, say so on that one.
- Repeated apologies for a missing source: one line in *Sources*.

## Amounts and dates

- Write amounts with the currency code: "USD 18,600", "EUR 412", "BRL 9,140". **Do not use the "$"
  sign in the briefing text**: some platforms turn text between two dollar signs into a math formula and
  scramble the numbers. Inside drafts (code blocks) the usual symbol is fine.
- Dates and times in the owner's locale (from the profile): e.g. "Thu Nov 13" or "qui 13/11", 24-hour
  clock if that is the local habit.

## WhatsApp version (delivery `whatsapp`)

A single message to the owner's own WhatsApp, about 12 lines, with the full HTML saved alongside:

```
*Good morning, Sam.* 71 messages · 4 need you

1. Business license expires Fri: sign on the portal (USD 412)
2. Northwind: change order USD 18.6k, answer by Thu
3. Mrs. Hale upset (2nd message): call today
4. Hartley Studio: you promised the quote TODAY

Calendar: 3 meetings · the 2pm (Northwind) is the one that matters
11 drafts ready · 2 invoices this week

*The one thing:* bring the change-order decision to the 2pm.
Reply "send" to send the drafts or "review" to check them.
```

Sending the briefing to the owner is not sending to a third party, but it only happens if the profile set
that destination.

## Monday briefing (Mode 8)

One document about **the week**, not five days stapled together:

1. **Headline of the week**: "Heavy until Wednesday; Thursday and Friday free for site work."
2. **Shape of the week**: one line per day: load (light/medium/full), the meetings that matter, travel.
   Which day is already lost. Where the real work blocks are.
3. **This week's deadlines**: everything due by Sunday.
4. **Promises due this week** and **who has been waiting on the owner longest**.
5. **Left over from last week**: *Needs you* items that were not resolved.
6. **The one thing for the week**, with the reason.

Proposed drafts (follow-ups, agenda requests, calendar blocks for focus) follow the same rule: drafted,
never sent without a yes.

## HTML

Use `assets/briefing-example.html` as the base: keep the `<head>`, the CSS and the section structure;
change only the content. Rules:

- Page title: `Briefing — <weekday> <date>`.
- Empty sections disappear (do not show "Handed off (0)"), except *Needs you*: if it is empty, say
  "Nothing needs you today." That is good news and the owner needs to read it.
- Every line that cites a message or event carries the link the connector itself returned ("open in
  Gmail", "open in WhatsApp"). Never build a URL from an email address, and never use a link that came
  inside a message.
