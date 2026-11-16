# Putting it on a phone line

The skill does not provide a phone line. Voice-agent platforms do (hosted ones, or open-source frameworks
with a phone provider). The pieces below work on any of them.

## 1. System prompt

Rules 1–8 of `SKILL.md` + the profile + the services sheet + the call flow. Keep it under one page: voice
models follow short prompts better.

## 2. First message

"Thank you for calling [business]. This is [business]'s AI assistant[, and this call is recorded]. How can
I help?"

## 3. Tools (names are suggestions)

| Tool | Input | Returns |
|---|---|---|
| `check_slots` | service, day range | free start times (same rules as the slots check in `scripts/frontdesk.py`) |
| `book` | name, phone, service, start | confirmation id, or "no longer free" |
| `take_message` | name, phone, reason, best time, consent | message id |
| `transfer` | reason | connects to the transfer number in the profile (only in transfer hours) |
| `end_call_summary` | — | caller, phone, reason, outcome, promised callback, flags |

## 4. Settings to check on the platform

Recording notice on/off matches the profile · voicemail detection · maximum call length · silence timeout ·
language detection · the transfer number · the calendar connected is the real one · logs exported daily.

## 5. Before going live

Run every call in `reference/test-calls.md` on the real number. Go live only when all of them pass. Review
the call log daily for the first two weeks.
