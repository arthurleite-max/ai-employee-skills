# Booking without double-booking

A start time is free only if all of these hold:

1. The business is open that day, and **start + service length ≤ closing time**.
2. **start ≥ now + minimum notice**.
3. For every existing booking: **start ≥ booking end + buffer** or **start + length + buffer ≤ booking
   start**.

Show the check for any time the caller asks for:
"Fri 10:30 + 50 min + 10 min buffer = 11:30, but a booking starts at 11:00 → not possible."

## Flow

1. Service, preferred day and part of the day.
2. Offer two or three free times (not the whole list).
3. Read the chosen one back with weekday and date; wait for "yes".
4. Re-check it is still free (another booking may have arrived); then book.
5. Confirmation: what, when, where, preparation, how to cancel.

## Never

- Book into a closed day, past closing time or inside the buffer.
- Hold a slot "for later" without the owner's rule allowing it.
- Promise a specific staff member, price or result that is not in the services sheet.
