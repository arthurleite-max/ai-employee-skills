# Origin table (example: fictional data; keep the real one outside the public folder)

| Source (licence) | Similarity | What came in | Where it is | What stayed out |
|---|---|---|---|---|
| example-org/dunning-agent (MIT) | 80% | Reminder tone ladder (friendly → firm) | `reference/tone.md` (written from scratch) | Email sending code |
| example-org/ar-toolkit (Apache-2.0) | 65% | Ageing buckets (0–30, 31–60, 61+ days) | `scripts/overdue.py` (own code) | Database schema |
| example-org/collections-bot (AGPL-3.0) | 70% | Ideas only: dispute flag | — | Everything (copyleft) |
| example-org/invoice-prompts (no licence) | 50% | Ideas only | — | Everything (no licence) |

**What is new**: one reminder per customer; disputed amounts never requested; contact rules respected;
works by pasting into any chat.
