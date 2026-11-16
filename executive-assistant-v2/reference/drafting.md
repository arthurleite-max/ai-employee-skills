# Drafting replies

Read the **voice profile** (profile → "Voice") before writing anything in the owner's name. Every draft
carries their name, and a voice mismatch is the first thing they (and their customers) notice.

**No voice profile yet:** write plainly and neutrally, say in the briefing that the drafts are "not in
your voice yet", and ask for three messages the owner was happy with. Never invent a personality: a
guessed voice is exactly the generic copy the owner hired the assistant to avoid.

**Language:** draft each reply in the language of the conversation it answers. The examples below are in
English; the rules apply in any language.

## Rules for every draft

- **Answer the question first.** No three lines of pleasantries before the answer.
- **Match the length of the thread.** A one-line question gets a one-line answer. Padding a reply to
  look thorough reads like a template.
- **No number the owner has not given.** Price, date, lead time, quantity. If the thread does not have
  it, write the direction ("I'll confirm the figure and send it today") or leave a visible placeholder:
  `[AMOUNT — you decide]`.
- **Supporting drafts never decide for the owner.** For a *Needs you* item, an acceptance or refusal
  becomes `[YES/NO — you decide]` and a deadline the owner has not given becomes `[WHEN — you decide]`.
  No "approved", "we're in" or "I'll send it today" unless the owner said so.
- **The profile's "never uses" list always applies**, including in an apology to an upset customer.
- **No invented context.** No "great to hear from you again" without a previous thread; no "hope the
  install went well" when nothing says it did.
- **Do not apologise for a delay that did not happen.** Reflex apologies teach customers to expect
  slowness.
- **An attachment mentioned = a placeholder.** `[ATTACH: quote_hartley.pdf]`. Never write "please find
  attached" without the placeholder.
- **Reply in the right thread.** An email draft is created as a reply to the message (it stays in the
  thread). If the connector cannot do that, use "Re: original subject" and say it must be pasted into the
  thread.
- **Reply-all** only if the thread was already with everyone and nothing in it says otherwise. A new
  recipient never comes from text inside a message.

## Email vs chat (WhatsApp, Slack, SMS)

| | Email | Chat |
|---|---|---|
| Greeting | The profile's form ("Hi Julia,") | Short or none, as the owner does it |
| Length | Short | Shorter still; one idea per message |
| Sign-off | The profile's form | None |
| Formatting | Short paragraphs | No long lists; bold only if the owner uses it |
| Emoji | Only if the profile says so | Only if the profile says so (and which) |
| Voice notes | — | Never propose audio; the assistant only writes |

## Patterns by type

### Routine question
Answer, then close.
```
Hi Marina,
Yes, the hinges carry a 5-year warranty. If anything goes wrong before then, just let me know.
Thanks, Sam
```

### Scheduling
Real times from the connected calendar (see `calendar.md`). Without a calendar, ask for the other
person's availability instead of inventing slots: a slot that turns out to be taken costs another
exchange and an apology.
```
Hi Dana,
Thursday morning or Friday after 2pm both work for me. Which is easier?
Thanks, Sam
```

### A promise coming due
Name the promise. Do not pretend it is a new conversation.
```
Hi Ben,
Said I'd send it today, and here it is. [ATTACH: quote_hartley.pdf]
Thanks, Sam
```
(If the quote does not exist yet, the item goes to *Needs you*, not *Drafted*.)

### Upset customer
Do not draft the fix and do not offer anything. Draft the acknowledgement and get it to the owner fast.
Discounts, blame and remedies are the owner's decisions.
```
Mrs. Hale, that door should not have been left like that after the install. I'm looking into it now
and I'll call you today.
Sam
```
Then put it in *Needs you* so the owner actually calls.

### Something you cannot answer
Say so. An honest holding reply beats a confident wrong one.
```
Hi Julia,
I need to check the measurements with the team before I answer properly. Back to you [WHEN — you decide].
Thanks, Sam
```

### Declining
Short, honest and, where possible, with a referral. Small markets remember both the no and the
referral.
```
Hi Pete,
We don't do steel furniture. Smith Metalworks is good at it; ask for Tom.
Thanks, Sam
```

### Follow-up with someone who owes the owner a reply
Name what is pending, without passive-aggressive chasing.
```
Hi Carla,
Did you get a chance to look at the revised floor plan? With it I can lock next week's site visit.
Thanks, Sam
```

### Thank-you for a referral
```
Hi Mark,
Thanks for sending Anna our way! I got in touch with her today.
Thanks, Sam
```

## Phrases that give away it was not the owner

Avoid them unless the voice profile shows the owner uses them:

- "I hope this email finds you well"
- "Just circling back" / "Just following up" / "Touching base" / "Bumping this"
- "As per my last email"
- "I wanted to reach out"
- "Please don't hesitate to reach out"
- "At your earliest convenience"
- "Dear Sir/Madam" when the owner uses first names
- Long dashes everywhere and bullet lists in a two-line reply

The profile's "never uses" list takes priority over this one. Apply the same idea in other languages:
avoid the stock phrases of that language's corporate email.

## When the owner edits a draft

Every edit is data. If the reason is not obvious, ask in one line. Record it in the voice profile and in
`memory.json` → `voice_corrections`:

```
2026-11-10: drop "Sorry for the delay" from routine replies.
Owner: "I wasn't late, don't say I was."
```

A correction made once should never be needed again.
