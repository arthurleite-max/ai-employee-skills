# Website Designer memory (example — fictional data)

Agents keep `website-designer-data/memory.json`; in a chat, the designer hands it back as a code block
at the end of each delivery. Append; never rewrite history.

```json
{
  "last_checkup": "2026-11-02",
  "pages_seen": ["/", "/pilates", "/fisioterapia", "/contato", "/blog"],
  "findings": [
    {"id": "F1", "page": "/", "what": "Booking button points to a 404 (/agendar)", "status": "fixed", "fixed_on": "2026-11-04"},
    {"id": "F2", "page": "/contato", "what": "Saturday hours say 9h–13h; profile says 8h–12h", "status": "approved, waiting for freelancer"},
    {"id": "F3", "page": "/pilates", "what": "Promotion 'Volta às aulas 2026' expired in March", "status": "open"}
  ],
  "changes_applied": [
    {"date": "2026-11-04", "page": "/", "change": "Booking button → https://agenda.example/movimento", "confirmed_by_loading": true}
  ],
  "pages_built": [
    {"date": "2026-11-05", "name": "landing-pilates-gestantes.html", "status": "draft, 2 placeholders (price, start date)"}
  ],
  "owner_rules": ["Never show prices on the home page", "Always use the booking link, not the form"]
}
```
