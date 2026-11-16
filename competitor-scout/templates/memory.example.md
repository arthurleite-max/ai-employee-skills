# Competitor Scout memory (example — fictional data)

Agents keep `competitor-scout-data/memory.json` and `snapshots/YYYY-MM-DD.csv`. In a chat, the scout
hands back the snapshot and the memory as code blocks; paste them next week.

```
SNAPSHOT 2026-06-02
competitor;item;kind;value;source;date
Bella Forneria;Margherita large;price;79.90;site/menu;2026-06-02
Bella Forneria;Combo 2 pizzas;offer;99.90 until 30/06;Meta Ad Library;2026-06-02
Bella Forneria;Google rating;rating;4.6 (812);Google;2026-06-02
Pizza Já;Margherita large;price;59.90;delivery app;2026-06-02
Casa Napoli;Margherita large;price;98.00;site;2026-06-02
```

```json
{
  "last_report": "2026-06-02",
  "moves": [
    {"date": "2026-06-02", "move": "Show delivery temperature (thermal bags)", "status": "approved", "measure": "delivery orders/week, baseline 41"}
  ],
  "notes": ["Pizza Já competes on price only; do not follow below our margin"]
}
```
