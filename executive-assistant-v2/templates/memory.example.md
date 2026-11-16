# Executive Assistant memory: template

At level 3 the assistant keeps this as `memory.json` in its data folder. At levels 1 and 2 it hands the
same JSON back at the end of every briefing for the owner to keep and paste next time.

Rules: append, never overwrite history (a resolved item changes `status` and gets `resolved_at`). Every
item needs a `source`. Never store ID numbers, bank details, passwords or health data: store the
reference to the conversation instead. The data below is fictional.

```json
{
  "version": 1,
  "last_run": "2026-11-10T07:00:00-05:00",
  "promises": [
    {
      "id": "p-0007",
      "what": "Send the quote for the living-room panels",
      "to": "Ben, Hartley Design Studio",
      "due": "2026-11-11",
      "explicit_date": true,
      "source": {"channel": "whatsapp", "conversation": "<connector id>", "date": "2026-11-03", "quote": "I'll send the numbers on Tuesday"},
      "status": "open",
      "resolved_at": null
    }
  ],
  "waiting_on_owner": [
    {
      "id": "a-0012",
      "who": "Fernando (accountant)",
      "ask": "October bank statement",
      "since": "2026-11-07",
      "source": {"channel": "email", "conversation": "<connector id>", "date": "2026-11-07"},
      "status": "open",
      "resolved_at": null
    }
  ],
  "waiting_on_others": [
    {
      "id": "t-0004",
      "who": "Carla Mendes",
      "ask": "Revised floor plan of the apartment",
      "since": "2026-11-04",
      "follow_ups": ["2026-11-06"],
      "source": {"channel": "email", "conversation": "<connector id>", "date": "2026-11-04"},
      "status": "open",
      "resolved_at": null
    }
  ],
  "deadlines": [
    {
      "id": "z-0003",
      "what": "Business license renewal",
      "amount": "USD 412",
      "due": "2026-11-14",
      "sender_verified": true,
      "source": {"channel": "email", "conversation": "<connector id>", "date": "2026-11-05"},
      "status": "open",
      "resolved_at": null
    }
  ],
  "senders": {
    "known_suppliers": {"Pinewood Timber": "billing@pinewoodtimber.example (usual beneficiary: Pinewood Timber LLC)"},
    "cold_pitches": ["sales@fleet.example"],
    "automatic": {"receipts@bank.example": "receipts"}
  },
  "voice_corrections": [
    {"date": "2026-11-10", "rule": "Do not write 'Sorry for the delay' in routine replies", "owner_said": "I wasn't late, don't say I was."}
  ],
  "declined_offers": [],
  "stats": {
    "runs": 1,
    "messages_triaged": 71,
    "drafts_created": 11,
    "drafts_approved_unchanged": 9,
    "drafts_edited": 2,
    "needs_you_items": 4
  }
}
```
