# Partnerships Scout memory (example — fictional data)

Agents keep `partnerships-scout-data/pipeline.csv` and `memory.json`. In a chat, the scout hands them
back as code blocks; paste them next time.

```
partner;type;fit;channel;status;first_contact;last_contact;followups;reply;next_step
Pedal Talk podcast;podcast;11;guest form;sent;2026-05-04;2026-05-04;0;;follow-up 1 on 09/05
Roda Livre bikes;business;9;business email;replied;2026-04-28;2026-05-02;1;interested;owner to confirm commission
Corre POA club;community;8;official profile;do not contact;2026-04-20;2026-04-22;0;asked not to be contacted;-
```

```json
{
  "do_not_contact": ["Corre POA club"],
  "what_worked": ["Guest idea tied to a dated episode got a reply in 2 days"],
  "last_run": "2026-05-04"
}
```
