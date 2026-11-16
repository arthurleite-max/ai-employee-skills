# Data intake: from statements to clean transactions

Bad intake ruins everything after it. Most wrong totals come from double counting, a misread decimal
separator or a sign flipped between bank and card exports.

## Accepted inputs

| Input | How to read it |
|---|---|
| CSV / XLSX export | Detect the columns by header (date, description, amount, or separate debit/credit columns). Do not assume a fixed layout; banks change exports often. Show the mapping when unsure. |
| OFX / QFX | Each `<STMTTRN>` has `DTPOSTED`, `TRNAMT` (signed) and `NAME`/`MEMO`. |
| PDF statement | Read the transaction table. If the text is garbled, ask for the CSV export or screenshots. |
| Screenshot | Read every visible line; say how many lines you read and ask whether the list continues. |
| Pasted text | Same as CSV; confirm the date format if it is ambiguous (03/04 = March 4 or April 3?). |
| Connector (open banking, accounting software, payment platform) | Read-only. Record which accounts and dates it returned. |

## Normalise every line

One record per transaction: `date` (ISO), `description` (as printed), `amount` (money **out negative**,
money in positive), `currency`, `account` (masked alias, e.g. "Business account", "Card •••• 9021"),
`source` (file and line).

- **Decimal separators.** `1.148,20` (comma decimal) and `1,148.20` (dot decimal) are the same amount.
  Decide per file from the pattern, never per line.
- **Signs.** Bank exports usually show debits negative; card statements often show purchases
  **positive** and refunds negative. Flip card statements so purchases are negative before merging.
  Check with one known purchase.
- **Separate debit/credit columns** become one signed amount.
- **Foreign currency.** Use the amount actually charged in the account currency. Keep the original
  currency in the description; never convert with a rate you made up.
- **Pending vs posted.** Count a charge once. If both appear, keep the posted one.
- **Balance lines** ("previous balance", "balance on…") are not transactions; keep them only as the
  sourced balance with their date.

## What is not spending

Remove these from spending totals and list them in a "moved, not spent" line so the owner sees nothing
vanished:

| Line | Why |
|---|---|
| Card-bill payment in the bank account ("card payment", "credit card bill") | The card purchases are the spending. Count the bill payment only if the card's purchases are **not** in the data, and then call it "card bill (details not provided)". |
| Transfer between the owner's own accounts, savings, investments | Money moved, not spent. |
| Loan principal received | Not income. Loan repayments: interest is a cost; the principal is "debt repayment", shown separately. |
| Refund / chargeback / reversal | Reduces spending in its category. Never count it as income. |
| Owner's withdrawals / owner's pay (business) | Shown separately as "paid to owner", not as an operating cost. |

If you are not sure a transfer goes to the owner's own account, ask once; do not decide silently.

## Coverage

Before any total, write the coverage line: which accounts and cards, from which date to which date, and
the gaps ("card •••• 9021: August to October; business account: August to October; no data for the
personal card"). A missing month is a gap, never zero spending. If the card bill paid in August belongs
to July purchases that are not in the data, say so.

## Quality checks before the report

1. Count the lines read per file and compare with what the owner sent (screenshots especially).
2. Sum of money in − sum of money out ≈ closing balance − opening balance, when both balances are
   present. If it does not match, say by how much; something is missing or duplicated.
3. Sum of the categories = total spending. If not, find the line that is missing.
4. Every amount quoted in the report can be pointed to a line or a sum of lines.
