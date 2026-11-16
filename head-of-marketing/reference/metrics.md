# Metrics

## The few that matter for a small business

| Metric | Formula | Says |
|---|---|---|
| Cost per lead (CPL) | spend ÷ leads | How expensive attention that converts is |
| Lead → sale rate | sales ÷ leads (same cohort/period) | Quality of leads and of the sales follow-up |
| Cost per sale (CAC) | spend ÷ sales from the source of truth | What a customer costs |
| ROAS | revenue ÷ spend | Revenue per unit spent (gross, before margin) |
| Payback | CAC ÷ (monthly margin per customer) | Months to earn the cost back (needs margin) |
| CTR | clicks ÷ impressions | Whether the ad gets attention |
| Landing conversion | leads ÷ clicks (or sessions) | Whether the page/form works |
| Pacing | spend so far ÷ (budget × days passed ÷ days in month) | On track to over/underspend |

Always state the period and source. Compute per channel, then total from the source of truth.

## Comparing

- Last 7 days vs previous 7 (same weekdays). Percent change = (new − old) ÷ old.
- Daily values vs the trailing 14-day average and spread (see `anomalies.md`).
- Month vs previous month and vs goal.
- With few events (under ~30 leads or sales in a period), changes of 20–30% can be noise: say "too few
  to call".

## Show the arithmetic

Without code, write each formula with its numbers ("Google CPL = 1,240 ÷ 31 = 40.00"). Compute the
totals first; write the headline last, copying them. `scripts/pulse.py` does it from a CSV.
