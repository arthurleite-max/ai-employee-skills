# Research: learn from open work, copy nothing

1. Search public code hosts and skill lists for the job and its parts (for example "invoice reminder
   skill", "accounts receivable agent", "dunning email").
2. For each candidate: what it does well, what is missing for a non-technical user, the licence, how close
   it is to the job (a similarity score helps choose).
3. Licences:

| Licence | What you may take |
|---|---|
| MIT, BSD, Apache-2.0 | Ideas freely; if you ever reuse text or code, keep the notice (prefer writing your own) |
| GPL, AGPL, LGPL (copyleft) | Ideas only; nothing included |
| No licence | Ideas only; nothing included |

4. Write two tables:
   - **Origin** (internal, `templates/origin.example.md`): source · licence · similarity · what came in ·
     where it is · what stayed out.
   - **Credits** (public, `CREDITS.md`): project · licence · idea used.
5. Say what is new in this skill (what none of the sources does).

Never name a company, product or person in a way that suggests they endorse the skill.
