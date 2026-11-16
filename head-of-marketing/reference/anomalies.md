# Anomalies: problems and opportunities

## What counts as unusual

For each channel and metric, compare the latest day (or week) with the trailing 14 days:
- **Mean and spread**: a value more than ~2.5 standard deviations away, or a change above ~40% when the
  numbers are large enough, is worth a line.
- **Weekday effects**: Mondays and weekends often differ; compare like with like when possible.

## The usual suspects

| Pattern | Most likely | Check first |
|---|---|---|
| Leads or sales drop to 0 (or halve) overnight, spend continues | Tracking or form broken, pixel removed, landing page down, payment error | Submit a test lead (with the owner's yes), check the form, the pixel/tag, the page, the CRM integration |
| Spend jumps, results flat | Budget change, bid strategy learning, broad audience | Change history in the ad account |
| CPL rises steadily over 2+ weeks | Ad fatigue, more competition (seasonal), audience exhausted | Frequency, CTR trend, auction insights |
| Clicks fine, leads down | Landing page or offer problem | Page speed, form, message match |
| Leads fine, sales down | Lead quality or sales follow-up | Response time, qualification notes |
| A channel converts far better per real sale | Opportunity | Can it scale? (referrals, past customers, search) |

## How to write it

"Meta Ads: 0 leads on 03–05/06 while spending 360 reais. Possible tracking failure (form or pixel), not
necessarily a channel problem. Check: submit a test lead; look at the form; check the CRM integration.
Until then, these days are *unknown*, not zero."

Never act on an anomaly (pause, change budget) without the owner's yes.
