# Finance Watchdog memory (example — fictional data)

Agents save this as `finance-watchdog-data/memory.json`. In a chat, the watchdog hands it back as a code
block at the end of each report; paste it next time. Append; never overwrite history. No card numbers,
account numbers or personal IDs.

```json
{
  "last_run": "2026-11-09",
  "coverage_seen": {"Business account": ["2026-08-01", "2026-11-08"], "Card •••• 9021": ["2026-08-01", "2026-11-08"]},
  "merchant_map": {
    "FLOUR & GRAIN CO": "Suppliers and inventory",
    "TILLPRO": "Software and subscriptions",
    "PAY *XK 5521": "Uncategorised"
  },
  "recurring": [
    {"merchant": "TILLPRO", "cadence": "monthly", "amount": 149.00, "currency": "USD", "account": "Card •••• 9021",
     "since": "2025-02", "last_seen": "2026-11-03", "critical": true, "decision": "keep"},
    {"merchant": "GYMONE", "cadence": "monthly", "amount": 119.00, "currency": "USD", "account": "Card •••• 9021",
     "since": "2026-03", "last_seen": "2026-11-02", "decision": "cancel", "decided_on": "2026-11-09", "verified": false}
  ],
  "baselines_monthly": {"Utilities": 1890.00, "Telecom and internet": 159.90, "Bank fees and interest": 114.00},
  "alerts_raised": [
    {"date": "2026-11-09", "type": "price increase", "merchant": "NETLINE FIBER", "detail": "159.90 → 199.90", "status": "open"}
  ],
  "expected_money": [
    {"what": "Refund of duplicate BULK MART 06/03", "amount": 1148.20, "asked_on": "2026-11-09", "status": "waiting"}
  ],
  "savings": {
    "verified": [],
    "decided_not_verified": [{"what": "Cancel GymOne", "annual_estimate": 1428.00, "decided_on": "2026-11-09"}]
  },
  "corrections": ["Two charges from Flour & Grain Co in one week are normal in December."]
}
```
