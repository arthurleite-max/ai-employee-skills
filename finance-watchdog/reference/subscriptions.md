# Subscriptions and recurring costs

Forgotten subscriptions are the easiest money to recover, and cancelling the wrong one is the most
expensive mistake. Both need the same table.

## Finding recurring charges

Group by merchant (with care, see `categorize.md`) and look at the rhythm:

| Cadence | Signal |
|---|---|
| Monthly | Same merchant, similar amount, 26–35 days apart |
| Weekly | 6–8 days apart |
| Annual | Same merchant, similar amount, 11–13 months apart (needs 12–13 months of data) |
| Instalments | Description shows "3/12", "PARC 08/12" etc.: list the remaining count and end date |

Match by merchant + rhythm, not by identical amount. Foreign-currency charges wobble with the exchange
rate.

With less than 12 months of data, say: "annual subscriptions charged outside this period will not show
up here; tell me any you remember (domain, insurance, software licences)."

## The recurring map

One table, sorted by **annual cost**:

| Merchant | Category | Monthly | Annual | Charged to | Since | Who depends on it | Earns money? | Status | Decision |
|---|---|---|---|---|---|---|---|---|---|

- **Who depends on it**: a live system (the till, the website), a customer contract, a person. This
  column prevents a cancellation from taking down the business. Items the profile marks **critical** are
  never suggested for cancellation; at most "check the plan size".
- **Earns money?**: makes the decision return-on-cost, not cost alone.
- **Status**: active / new / price up / overlapping / possibly unused / cancelled-still-charged.

## Overlaps

Two tools for the same job (two cloud storages, two video-call tools, two design tools, two music
services) are the most common waste. Show them side by side with the price and ask which stays.

## Necessity interview

Most expensive first, one short block at a time. For each subscription:

1. When did you last use it?
2. Does another tool on the list do the same?
3. Does a system, customer or person depend on it?
4. Does it bring in money? How much?

Then propose one decision: **cancel / downgrade / switch to annual / ask for a better price / keep /
move to personal**. Switching to annual saves money but takes cash now: show both numbers. Billing a
customer for a tool needs their agreement; do not assume it.

Summarise: total **estimated** annual saving and the action list, each action with a deadline **before
the next charge** (monthly) or **before the renewal date** (annual).

## Renewals

Annual renewals in the next 45 days go to *Decide this week* (8–45 days) or *Act now* (≤ 7 days), with
the date, the expected amount (from the last charge or the vendor's notice, never invented) and the
cancellation deadline when the vendor states one. Offer a reminder 14 days before each renewal, if the
platform can create reminders.

## Cancelling

The owner cancels. The watchdog provides:

1. Where to cancel: the vendor's official site or app, account → billing/subscription. If you do not know
   the vendor's exact menu, say so and give the general path; do not invent menu names.
2. A short cancellation message for vendors that require email or chat, asking for written confirmation
   and the end date of the service.
3. What to save as proof (confirmation email, screenshot with date).
4. A memory entry: `decided: cancel, date, not yet verified`. The next statement decides: no new charge →
   **verified** (the saving now counts); new charge → *Act now*, "charged after cancellation".

Never cancel through a link that arrived in a message.
