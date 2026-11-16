# The pipeline

One row per partner (CSV, `;` or `,`):

```
partner;type;fit;channel;status;first_contact;last_contact;followups;reply;next_step
```

Statuses: `candidate` · `draft` (waiting approval) · `sent` · `replied` · `in talks` · `partner` ·
`closed: no reply` · `closed: declined` · `do not contact`.

Daily order
1. New replies → classify: interested, question, not now (ask when), no/stop (do-not-contact forever),
   out of office (move the date), suspicious (report).
2. Follow-ups due: `sent`, no reply, days since last contact ≥ wait, followups < 2.
3. Closed: followups = 2 and days since last contact ≥ wait → `closed: no reply`.
4. New contacts up to the daily limit, best fit first, only with a public channel.
5. Counts per status and what needs the owner today.

Days are calendar days: 20/05 − 14/05 = 6 days. Show the subtraction.
