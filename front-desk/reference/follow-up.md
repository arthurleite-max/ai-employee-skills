# Callbacks and follow-ups

## The call log (one row per call)

id · time · caller · phone · outcome · minutes since call (now − call time) · first callback − call time
(speed to lead) · callback late? · next attempt · flags.

Callback late = the call still needs an answer (missed, message, question, booking request), nobody has
called back yet, and minutes since call > target. A call already returned once is not late: plan its next attempt.

## Rules

- **Speed matters**: return missed calls, messages and open questions within the target in the profile.
- **One person, one callback**: several calls from the same number are one conversation.
- **Attempts**: at most the number in the profile (usually 2); the second one day after the first.
- **Quiet hours**: never call or text inside them; move the attempt to the next allowed time.
- **Do not contact**: anyone who asked to stop is never contacted again; tell the owner.
- **Spam and robocalls**: no callback.
- **Booked callers**: a confirmation, and a reminder the day before if the owner wants it.

## Callback script

"Hi [name], this is the AI assistant of [business], returning your call about [reason]. Is now a good
time?" Then the answer, or the booking flow. If voicemail: name, business, reason, number; no private
details.

## Text draft

"Hi [name], [business] here (AI assistant). You called about [reason] at [time]. Reply with a good time for
a call, or book at [link]. Reply STOP to opt out." Sent only from a tool the owner approved.
