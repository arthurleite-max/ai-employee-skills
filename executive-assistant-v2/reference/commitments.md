# Commitments, deadlines and follow-ups

The most expensive thing in an inbox is not a new message: it is a promise buried in a thread already
read. The owner writes "I'll send the quote Wednesday" in the middle of a long thread, forgets by
Thursday, and the customer remembers. No unread counter catches that. This step does.

## The four lists

| List | What it is | Source |
|---|---|---|
| **The owner promised** | The owner committed to something, with or without a date | Sent messages (email and chat), minutes, memory |
| **Waiting on the owner** | Someone asked the owner for something and has no answer yet | Triage (including read threads) |
| **The owner is waiting on** | The owner asked for something and the other side has not replied | Unanswered sent messages, minutes, memory |
| **Deadlines** | A fixed external date: invoice, renewal, certificate, bid, delivery | Triage, calendar, memory |

## Finding promises

Scan the messages **sent by the owner** in the last 3 weeks for first-person commitments with an action
verb: "I'll send", "I'll check", "I'll get back to you", "I'll drop by", "I'll confirm", "I'll call you",
"tomorrow I'll", "by Friday" (and their equivalents in the owner's language). For each one:

- what was promised, to whom, in which conversation (with the connector's link);
- the date: an explicit one ("Wednesday") converted to an absolute date **counting from the date of the
  message, never from today** ("tomorrow" in yesterday's message is today); implicit ones ("next week")
  too; no date → `no_date`, due in 3 business days by default (adjustable in the profile);
- whether it was already delivered: did the owner send it later? an attachment? When unsure, keep it
  open and say you could not confirm.

A promise due today or overdue → *Needs you*, numbered (if it depends on the owner) or *Drafted* (if the
deliverable exists and only needs sending).

## Follow-ups for people who owe the owner a reply

An item in `waiting_on_others` with no reply for more than `follow_up.business_days` (default 3
business days) gets a drafted follow-up (see `drafting.md`). After two follow-ups with no reply, stop
drafting and bring it to the owner: "Carla has not answered twice about the floor plan; want to call?"

Weekends and national holidays are not business days. Local holidays only if the profile lists them.

## Deadlines

Invoices, taxes, renewals of licenses, permits or certificates, contract expiries, bid dates, deliveries
promised to customers. For each one: what, amount (if any), due date, verified sender and what happens if
it slips. Detailed bill handling belongs to a finance assistant if the owner has one; this assistant only
lists.

Lead time to appear in the briefing: due within 7 calendar days, or whatever the profile says. Overdue
items go first in *Deadlines*, highlighted.

## The memory (`memory.json`)

Structure in `templates/memory.example.md`. Rules:

- **Append, never overwrite.** A resolved item changes `status` to `resolved` with `resolved_at`; it is
  not deleted. Items resolved more than 90 days ago may move to `memory_archive/YYYY-MM.json`.
- **Every item has a source** (channel + conversation/message id + date). No source, no entry.
- **Update at the end of every run**, after approval: new promises, follow-ups sent (with the date, to
  count the next one), resolved items, `last_run`.
- In a scheduled run, the memory is updated only with what was **read and classified**; nothing is
  marked as sent.
- Never store sensitive data that is not needed (ID numbers, card numbers, passwords, health data). Keep
  the reference to the conversation, not its content.

## Output of Mode 7

```
YOU PROMISED (3)
• Hartley Design Studio: quote for the living-room panels · due TODAY · "I'll send the
  numbers on Tuesday" (WhatsApp, Nov 3) · draft ready if the quote is done
• Mrs. Hale: call about the wardrobe door · overdue since yesterday
• Julia (Northwind): answer on the change order · by Thu Nov 13

WAITING ON YOU (2)
• Fernando (accountant): asked for the October bank statement 4 days ago
• Anna (referred by Mark): asked for a site-visit time 1 day ago

YOU ARE WAITING ON (2)
• Carla: revised floor plan · 5 business days · 1 follow-up sent (Nov 6) · 2nd follow-up drafted
• Pinewood Timber: confirmation of order 4471 · 2 business days · still on time

DEADLINES (next 7 days)
• Fri Nov 14: business license renewal, USD 412, City Hall
• Mon Nov 17: Hartwell Hardware invoice, USD 3,280 (sender verified)
```
