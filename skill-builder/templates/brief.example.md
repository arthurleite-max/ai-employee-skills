# Skill brief (example: fictional data)

- **Name**: invoice-reminder · "Invoice Reminder" · MIT · published in the owner's public repository
- **Job**: chase unpaid invoices politely and on time
- **User**: owner of a small wholesale bakery (crumb.example), not technical, uses a free chat app on the
  phone and sometimes a laptop
- **Promises**: (1) finds what is overdue and by how many days; (2) one clear reminder per customer;
  (3) respects disputes and contact rules; (4) lists what needs the owner today
- **Must never happen**: asking for a disputed amount; emailing someone who asked not to be emailed;
  sending anything without approval; inventing an amount or a date
- **Inputs**: invoice list (pasted or CSV), today's date, contact rules
- **Outputs**: overdue table with days and totals, one draft per customer, owner's list
- **Levels**: chat (paste) · code (`scripts/overdue.py` reads the CSV) · agent (accounting export folder)
- **Frequency**: every Monday
