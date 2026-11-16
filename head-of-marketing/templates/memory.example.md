# Head of Marketing memory (example — fictional data)

```json
{
  "last_report": "2026-06-04",
  "baselines_daily_14d": {"Google Ads": {"spend": 95, "leads": 3.1}, "Meta Ads": {"spend": 120, "leads": 4.2}},
  "alerts": [
    {"date": "2026-06-03", "channel": "Meta Ads", "type": "possible tracking failure", "detail": "0 leads 3 days",
     "outcome": "form integration broken, fixed 2026-06-04"}
  ],
  "decisions": [
    {"date": "2026-06-04", "what": "Test referral benefit for 2 weeks", "owner_yes": true, "review_on": "2026-06-18"}
  ],
  "tests_running": [{"name": "referral benefit", "metric": "referral leads/week", "baseline": 1.8, "until": "2026-06-18"}],
  "tracking_gaps": ["Instagram organic leads not tagged in the scheduling system"]
}
```
