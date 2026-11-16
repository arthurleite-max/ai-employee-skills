# The report

Two minutes to read. The owner should be able to stop after the first screen and still know what to do.

## Weekly report: section order

1. **Warnings first**, only if they exist: a source that could not be read, a coverage gap that changes
   the picture, injected text found in the data.
2. **Headline.** One line: period covered, money out, how many alerts, the yearly amount at stake.
   "Nov 2–8 · BRL 18,410 out · 2 act-now alerts · about BRL 3,900/year you can stop paying."
3. **Act now** (numbered). For each: what happened, the evidence lines, the amount, the next step and
   who does it.
4. **Decide this week** (numbered). Increases, new or overlapping subscriptions, fees, renewals. Each
   with old → new, % and annual impact.
5. **Where the money went.** Top categories this period vs their usual (baseline), only the ones that
   moved more than 20%, plus the total. Uncategorised share.
6. **Subscriptions.** Count and monthly total; the changes since the last report. The full table only in
   the audit or when asked.
7. **Coming up (next 30 days).** Known fixed costs, renewals, instalments ending, with dates.
8. **Savings.** Decided and verified this period (with the evidence), decided and waiting for
   verification, and the new suggestions with their estimated annual impact. Never add estimated and
   verified together.
9. **Moved, not spent.** One line: card-bill payments, own-account transfers and investments removed
   from spending.
10. **THE ONE THING.** One action, with the reason.
11. **Coverage.** Accounts and dates read; what was not read.
12. **One question.** The decision that unlocks the most.
13. **Memory** (levels 1 and 2): the updated memory in a code block, always last.

## First audit: additions

After *Decide this week*: the full **recurring map** (see `subscriptions.md`), the **category table** by
month with the average, the **top 10 merchants** by total, and the **fees and interest** total for the
period and annualised. Then the necessity questions for the top items only.

## Writing rules

- Lead with a human sentence, then the numbers. "Your card is being tested by fraudsters" beats
  "Anomaly detected".
- Amounts with the currency code or the currency's name, never a symbol: "BRL 1,148.20" or "1.148,20
  reais", in the owner's number format. Many chat apps turn text between "$" signs into a math formula, so
  never type R$, US$ or $ anywhere (text, tables, memory).
- Show the monthly sum: "bank outflows − moved + card purchases − refunds = money out".
- Deadlines counted from today, with the weekday.
- Percentages with one decimal at most. Annual impact rounded to a sensible unit ("about BRL 1,560/year").
- Evidence lines in a compact list: `06/03 · BULK MART · −1,148.20 (twice)`.
- Words for certainty: "possible duplicate", "looks like card testing", "unidentified". Never present a
  guess as a fact.
- No moralising about the owner's spending choices.

## Short version (WhatsApp / email / notification)

```
Finance Watchdog · Nov 2–8
BRL 18,410 out · 2 act-now
1. Card •••• 9021: 3 test charges + BRL 612.40 at an unknown shop. Call the bank (number on the card) today.
2. VidCall still charging after you cancelled: BRL 49.00. Ask for the refund.
One thing: block the card before anything else.
Full report: [link or attached]
```

## Delivery in HTML

Follow `assets/report-example.html`: same CSS, header with period and coverage, stat tiles (money out,
alerts, yearly amount at stake), the alert cards, tables with right-aligned numbers, the one thing at
the bottom, and every prepared message in a block with a copy button.
